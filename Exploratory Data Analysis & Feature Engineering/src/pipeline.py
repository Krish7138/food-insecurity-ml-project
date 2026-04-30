import argparse
import json
import re
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from xgboost import XGBClassifier


def ensure_columns(df: pd.DataFrame, columns: list[str], default: int = 0) -> pd.DataFrame:
    for col in columns:
        if col not in df.columns:
            df[col] = default
    return df


def find_first_existing(df: pd.DataFrame, candidates: list[str]) -> str | None:
    for col in candidates:
        if col in df.columns:
            return col
    return None


def save_plot(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    plt.tight_layout()
    plt.savefig(path, dpi=300, bbox_inches="tight")
    plt.close()


def sanitize_filename(value: str) -> str:
    sanitized = re.sub(r'[<>:"/\\|?*\x00-\x1F]', "_", str(value))
    sanitized = re.sub(r"\s+", "_", sanitized).strip(" ._")
    return sanitized or "plot"


def build_engineered_features(df: pd.DataFrame) -> pd.DataFrame:
    income_col = "What is your annual household income before tax?"
    low_income_groups = ["Less than £10,000", "£10,000 - £19,999"]
    if income_col in df.columns:
        df["income_risk_group"] = df[income_col].isin(low_income_groups).astype(int)
    else:
        df["income_risk_group"] = 0

    employment_cols = [
        "Working full-time",
        "Working part-time",
        "Unemployed",
        "Retired",
        "Student",
    ]
    df = ensure_columns(df, employment_cols, default=0)
    binary_map = {"Yes": 1, "No": 0, "Selected": 1, "Not Selected": 0, True: 1, False: 0}
    for col in employment_cols:
        df[col] = pd.to_numeric(df[col].replace(binary_map), errors="coerce").fillna(0)
    df["employment_risk"] = (
        df["Unemployed"] * 3
        + df["Student"] * 1
        + df["Working part-time"] * 1
        + df["Retired"] * 1
        - df["Working full-time"] * 2
    )

    support_cols = [
        "Foodbank",
        "Community or faith group",
        "Close family or friends",
        "Neighbours",
    ]
    df = ensure_columns(df, support_cols, default=0)
    for col in support_cols:
        df[col] = pd.to_numeric(df[col].replace(binary_map), errors="coerce").fillna(0)
        df[col] = (df[col] > 0).astype(int)
    df["social_support_score"] = df[support_cols].sum(axis=1).astype(int)

    isolation_col = "How often do you feel isolated from others or left out?"
    iso_map = {"Never": 0, "Rarely": 1, "Sometimes": 2, "Often": 3, "Always": 4}
    if isolation_col in df.columns:
        df["isolation_score"] = df[isolation_col].map(iso_map).fillna(0)
    else:
        df["isolation_score"] = 0

    health_col = find_first_existing(
        df,
        [
            "Do you have any physical or mental health conditions or illnesses that are limiting your day to day activities?",
            "Do you have any physical or mental health conditions or illnesses that are limiting your day to day activities",
        ],
    )
    if health_col:
        df["health_risk"] = df[health_col].map({"Yes": 1, "No": 0}).fillna(0)
    else:
        df["health_risk"] = 0

    prepay_col = "Do you use a prepayment or pay-as-you-go meter to pay for your energy usage?"
    if prepay_col in df.columns:
        df["prepay_meter_risk"] = df[prepay_col].map({"Yes": 1, "No": 0}).fillna(0)
    else:
        df["prepay_meter_risk"] = 0

    df["fuel_vulnerability_score"] = (
        df["income_risk_group"] + df["health_risk"] + df["prepay_meter_risk"]
    )
    df["income_unemployed_interaction"] = df["income_risk_group"] * df["Unemployed"]
    df["medical_heat_risk"] = df["health_risk"] * df["prepay_meter_risk"]
    return df


def get_valid_features(df: pd.DataFrame, feature_list: list[str]) -> list[str]:
    return [col for col in feature_list if col in df.columns]


def select_features_xgb(
    df: pd.DataFrame,
    feature_list: list[str],
    target_col: str,
    threshold: float,
    module_name: str,
    top_n: int,
    plots_dir: Path,
) -> tuple[list[str], pd.DataFrame]:
    valid_features = [c for c in feature_list if c in df.columns]
    if not valid_features:
        raise ValueError(f"No valid features found for {module_name}.")
    if target_col not in df.columns:
        raise ValueError(f"Target column '{target_col}' not found.")

    X = df[valid_features].copy()
    y = df[target_col].copy()
    mask = y.notna()
    X = X.loc[mask].copy()
    y = y.loc[mask].astype(str)

    le = LabelEncoder()
    y_enc = le.fit_transform(y)
    y_series = pd.Series(y_enc)

    num_cols = X.select_dtypes(include=[np.number, "bool"]).columns.tolist()
    cat_cols = [c for c in X.columns if c not in num_cols]

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", "passthrough", num_cols),
            ("cat", OneHotEncoder(handle_unknown="ignore"), cat_cols),
        ],
        remainder="drop",
        verbose_feature_names_out=False,
    )

    can_stratify = (y_series.nunique() > 1) and (y_series.value_counts().min() >= 2)
    stratify_y = y_enc if can_stratify else None

    X_train_raw, X_test_raw, y_train, _ = train_test_split(
        X, y_enc, test_size=0.25, random_state=42, stratify=stratify_y
    )

    X_train = preprocessor.fit_transform(X_train_raw)
    _ = preprocessor.transform(X_test_raw)

    n_classes = y_series.nunique()
    model = XGBClassifier(
        n_estimators=200,
        max_depth=4,
        learning_rate=0.05,
        subsample=0.8,
        colsample_bytree=0.8,
        random_state=42,
        eval_metric="mlogloss" if n_classes > 2 else "logloss",
    )
    model.fit(X_train, y_train)

    feature_names = preprocessor.get_feature_names_out()
    importance_df = pd.DataFrame(
        {"Feature": feature_names, "Importance": model.feature_importances_}
    ).sort_values(by="Importance", ascending=False)

    selected_encoded = importance_df.loc[
        importance_df["Importance"] >= threshold, "Feature"
    ].tolist()
    original_selected = []
    for col in valid_features:
        if (col in selected_encoded) or any(f.startswith(f"{col}_") for f in selected_encoded):
            original_selected.append(col)

    plot_df = importance_df.head(top_n)
    plt.figure(figsize=(10, max(4, int(top_n * 0.35))))
    sns.barplot(data=plot_df, x="Importance", y="Feature", orient="h")
    plt.title(f"{module_name} - Top {top_n} Feature Importances (XGBoost)")
    save_plot(plots_dir / f"{sanitize_filename(module_name.lower())}_feature_importance.png")

    return original_selected, importance_df


def run_pipeline(input_csv: Path, result_dir: Path) -> None:
    plots_dir = result_dir / "plots"
    data_dir = result_dir / "data"
    result_dir.mkdir(parents=True, exist_ok=True)
    plots_dir.mkdir(parents=True, exist_ok=True)
    data_dir.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(input_csv)

    targets = ["food_security_label", "fuel_security_label", "child_security_label"]
    for col in targets:
        if col in df.columns:
            plt.figure(figsize=(7, 4))
            sns.countplot(data=df, x=col)
            plt.title(f"{' '.join(col.split('_')).title()} Distribution")
            save_plot(plots_dir / f"{sanitize_filename(col)}_distribution.png")

    score_cols = ["food_security_score", "child_security_score", "fuel_security_score"]
    for col in score_cols:
        if col in df.columns:
            plt.figure(figsize=(8, 4))
            sns.histplot(df[col], bins=10)
            plt.title(f"{' '.join(col.split('_')).title()} Distribution")
            save_plot(plots_dir / f"{sanitize_filename(col)}_hist.png")

    income_col = "What is your annual household income before tax?"
    if income_col in df.columns and "food_security_score" in df.columns:
        plt.figure(figsize=(12, 5))
        sns.boxplot(x=income_col, y="food_security_score", data=df)
        plt.xticks(rotation=45, ha="right")
        plt.title("Income vs Food Security Score")
        save_plot(plots_dir / "income_vs_food_security_score_boxplot.png")

    eda_cols = [
        "What range best describes your age group?",
        "How would you describe your gender?",
        "Which of the following best describes your household?",
        income_col,
    ]
    for col in eda_cols:
        if col in df.columns:
            plt.figure(figsize=(10, 5))
            sns.countplot(data=df, y=col, order=df[col].value_counts().index)
            plt.title(col)
            save_plot(plots_dir / f"{sanitize_filename(col)}_countplot.png")

    df = build_engineered_features(df)

    food_features = get_valid_features(
        df,
        ["Working full-time", "Working part-time", "Unemployed", "Retired", "incentivised"]
        + [
            income_col,
            "Which of the following best describes your household?",
            "What range best describes your age group?",
            "How would you describe your gender?",
            "In general, how satisfied are you with your life?",
            "Do you have any physical or mental health conditions or illnesses that are limiting your day to day activities?",
            "How often do you feel isolated from others or left out?",
        ]
        + [
            "income_risk_group",
            "employment_risk",
            "social_support_score",
            "isolation_score",
            "health_risk",
        ],
    )

    fuel_features = get_valid_features(
        df,
        ["Working full-time", "Working part-time", "Unemployed", "Retired", "incentivised"]
        + [
            income_col,
            "Which of the following best describes the house you currently live in?",
            "Do you know the Energy Performance Certificate (EPC) rating for the house you currently live in?",
            "Do you use a prepayment or pay-as-you-go meter to pay for your energy usage?",
            "Which of the following best describes your household?",
            "What range best describes your age group?",
            "Consider your grocery shopping habits in the past 12 months. How often have you avoided food that requires cooking to reduce energy usage?",
        ]
        + [
            "income_risk_group",
            "employment_risk",
            "health_risk",
            "prepay_meter_risk",
            "fuel_vulnerability_score",
            "medical_heat_risk",
        ],
    )

    child_features = get_valid_features(
        df,
        [
            "Working full-time",
            "Working part-time",
            "Unemployed",
            "Retired",
            "Student",
            "incentivised",
        ]
        + [
            income_col,
            "Which of the following best describes your household?",
            "What range best describes your age group?",
            "How would you describe your gender?",
        ]
        + [
            "income_risk_group",
            "employment_risk",
            "social_support_score",
            "health_risk",
            "income_unemployed_interaction",
        ],
    )

    food_selected, food_imp = select_features_xgb(
        df=df,
        feature_list=food_features,
        target_col="food_security_label",
        threshold=0.02,
        module_name="Food Security",
        top_n=50,
        plots_dir=plots_dir,
    )
    fuel_selected, fuel_imp = select_features_xgb(
        df=df,
        feature_list=fuel_features,
        target_col="fuel_security_label",
        threshold=0.02,
        module_name="Fuel Security",
        top_n=30,
        plots_dir=plots_dir,
    )
    child_selected, child_imp = select_features_xgb(
        df=df,
        feature_list=child_features,
        target_col="child_security_label",
        threshold=0.01,
        module_name="Child Security",
        top_n=30,
        plots_dir=plots_dir,
    )

    (data_dir / "food_features.json").write_text(json.dumps(food_selected, indent=2), encoding="utf-8")
    (data_dir / "fuel_features.json").write_text(json.dumps(fuel_selected, indent=2), encoding="utf-8")
    (data_dir / "child_features.json").write_text(json.dumps(child_selected, indent=2), encoding="utf-8")
    df.to_csv(data_dir / "feature_engineered_data.csv", index=False)
    food_imp.to_csv(data_dir / "food_feature_importance.csv", index=False)
    fuel_imp.to_csv(data_dir / "fuel_feature_importance.csv", index=False)
    child_imp.to_csv(data_dir / "child_feature_importance.csv", index=False)

    summary = {
        "input_csv": str(input_csv),
        "rows": int(df.shape[0]),
        "columns_after_engineering": int(df.shape[1]),
        "selected_counts": {
            "food_features": len(food_selected),
            "fuel_features": len(fuel_selected),
            "child_features": len(child_selected),
        },
        "result_dir": str(result_dir),
    }
    (result_dir / "pipeline_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description="EDA + feature engineering pipeline from main.ipynb")
    parser.add_argument(
        "--input",
        type=Path,
        default=root / "cleaned_dataset_role01.csv",
        help="Path to input CSV file.",
    )
    parser.add_argument(
        "--result-dir",
        type=Path,
        default=Path(__file__).resolve().parent / "result",
        help="Directory to save plots and outputs.",
    )
    args = parser.parse_args()
    run_pipeline(input_csv=args.input, result_dir=args.result_dir)


if __name__ == "__main__":
    main()
