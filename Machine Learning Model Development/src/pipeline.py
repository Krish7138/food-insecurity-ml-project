import json
import warnings
from pathlib import Path

import joblib
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from imblearn.over_sampling import SMOTE
from imblearn.pipeline import Pipeline as ImbPipeline
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.metrics import accuracy_score, f1_score
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import LabelEncoder, OneHotEncoder, StandardScaler
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from xgboost import XGBClassifier

warnings.filterwarnings("ignore")

ROOT_DIR = Path(__file__).resolve().parents[1]
DATASET_DIR = ROOT_DIR / "dataset"
RESULT_DIR = ROOT_DIR / "src" / "results"
MODEL_DIR = RESULT_DIR / "models"


def ensure_dirs() -> None:
    RESULT_DIR.mkdir(parents=True, exist_ok=True)
    for domain in ("food", "fuel", "child"):
        (MODEL_DIR / domain).mkdir(parents=True, exist_ok=True)


def load_inputs() -> tuple[pd.DataFrame, dict]:
    df = pd.read_csv(DATASET_DIR / "feature_engineered_data.csv")

    with open(DATASET_DIR / "food_features.json", "r", encoding="utf-8") as f:
        food_features = json.load(f)
    with open(DATASET_DIR / "fuel_features.json", "r", encoding="utf-8") as f:
        fuel_features = json.load(f)
    with open(DATASET_DIR / "child_features.json", "r", encoding="utf-8") as f:
        child_features = json.load(f)

    domain_map = {
        "food": {"X_cols": food_features, "y_col": "food_security_label"},
        "fuel": {"X_cols": fuel_features, "y_col": "fuel_security_label"},
        "child": {"X_cols": child_features, "y_col": "child_security_label"},
    }

    return df, domain_map


def define_models() -> dict:
    return {
        "SVM": (
            SVC(),
            {
                "model__C": [1, 3, 5],
                "model__kernel": ["rbf"],
                "model__gamma": ["scale"],
                "model__class_weight": [None, "balanced"],
            },
        ),
        "RandomForest": (
            RandomForestClassifier(random_state=42),
            {
                "model__n_estimators": [200, 400],
                "model__max_depth": [None, 5, 10],
                "model__min_samples_split": [2, 5],
                "model__min_samples_leaf": [1, 2],
                "model__class_weight": [None, "balanced"],
            },
        ),
        "DecisionTree": (
            DecisionTreeClassifier(random_state=42),
            {
                "model__max_depth": [3, 5, 8],
                "model__min_samples_split": [2, 5, 10],
                "model__min_samples_leaf": [1, 2],
                "model__class_weight": [None, "balanced"],
            },
        ),
        "XGBoost": (
            XGBClassifier(random_state=42, eval_metric="mlogloss"),
            {
                "model__n_estimators": [100, 200],
                "model__max_depth": [3, 5],
                "model__learning_rate": [0.05, 0.1],
                "model__subsample": [0.8, 1.0],
                "model__colsample_bytree": [0.8, 1.0],
            },
        ),
    }


def prepare_domain_data(df: pd.DataFrame, cfg: dict):
    X = df[cfg["X_cols"]].copy()
    y = df[cfg["y_col"]].copy()

    mask = y.notna()
    X = X.loc[mask]
    y = y.loc[mask]

    le = LabelEncoder()
    y = le.fit_transform(y.astype(str))

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42, stratify=y
    )
    return X_train, X_test, y_train, y_test


def build_preprocessor(X_train: pd.DataFrame) -> ColumnTransformer:
    cat_cols = X_train.select_dtypes(include=["object", "category"]).columns.tolist()
    num_cols = X_train.select_dtypes(exclude=["object", "category"]).columns.tolist()

    return ColumnTransformer(
        [
            (
                "num",
                Pipeline(
                    [
                        ("imputer", SimpleImputer(strategy="median")),
                        ("scaler", StandardScaler()),
                    ]
                ),
                num_cols,
            ),
            (
                "cat",
                Pipeline(
                    [
                        ("imputer", SimpleImputer(strategy="most_frequent")),
                        ("onehot", OneHotEncoder(handle_unknown="ignore")),
                    ]
                ),
                cat_cols,
            ),
        ]
    )


def train_one_model(
    domain: str,
    model_name: str,
    model,
    param_grid: dict,
    X_train: pd.DataFrame,
    X_test: pd.DataFrame,
    y_train,
    y_test,
    preprocessor: ColumnTransformer,
) -> dict:
    pipe = ImbPipeline(
        [("prep", preprocessor), ("smote", SMOTE(random_state=42)), ("model", model)]
    )
    grid = GridSearchCV(pipe, param_grid=param_grid, cv=5, scoring="accuracy", n_jobs=-1)
    grid.fit(X_train, y_train)

    best_model = grid.best_estimator_
    save_path = MODEL_DIR / domain / f"{model_name}.pkl"
    joblib.dump(best_model, save_path)

    y_train_pred = best_model.predict(X_train)
    y_test_pred = best_model.predict(X_test)

    train_acc = accuracy_score(y_train, y_train_pred)
    test_acc = accuracy_score(y_test, y_test_pred)
    train_f1 = f1_score(y_train, y_train_pred, average="weighted")
    test_f1 = f1_score(y_test, y_test_pred, average="weighted")

    return {
        "Domain": domain,
        "Model": model_name,
        "TrainAccuracy": train_acc,
        "TestAccuracy": test_acc,
        "TrainF1Weighted": train_f1,
        "TestF1Weighted": test_f1,
        "TrainError": 1 - train_acc,
        "TestError": 1 - test_acc,
        "BestCVScoreAccuracy": grid.best_score_,
        "BestParams": str(grid.best_params_),
        "ModelPath": str(save_path.relative_to(ROOT_DIR)).replace("\\", "/"),
    }


def train_all_models_for_domain(domain: str, cfg: dict, df: pd.DataFrame, models: dict) -> pd.DataFrame:
    X_train, X_test, y_train, y_test = prepare_domain_data(df, cfg)
    preprocessor = build_preprocessor(X_train)
    rows = []
    for model_name, (model, param_grid) in models.items():
        rows.append(
            train_one_model(
                domain=domain,
                model_name=model_name,
                model=model,
                param_grid=param_grid,
                X_train=X_train,
                X_test=X_test,
                y_train=y_train,
                y_test=y_test,
                preprocessor=preprocessor,
            )
        )
    return pd.DataFrame(rows)


def save_visualizations(results_df: pd.DataFrame) -> None:
    sns.set_theme(style="whitegrid")

    plt.figure(figsize=(10, 6))
    sns.barplot(data=results_df, x="Domain", y="TestAccuracy", hue="Model")
    plt.title("Test Accuracy by Domain and Model")
    plt.tight_layout()
    plt.savefig(RESULT_DIR / "test_accuracy_by_domain_model.png", dpi=200)
    plt.close()

    best_df = results_df.loc[results_df.groupby("Domain")["TestAccuracy"].idxmax()].copy()
    plt.figure(figsize=(8, 5))
    sns.barplot(data=best_df, x="Domain", y="TestAccuracy", hue="Model")
    plt.title("Best Model Per Domain (Test Accuracy)")
    plt.tight_layout()
    plt.savefig(RESULT_DIR / "best_model_per_domain.png", dpi=200)
    plt.close()

    heatmap_df = results_df.pivot(index="Domain", columns="Model", values="TestAccuracy")
    plt.figure(figsize=(8, 5))
    sns.heatmap(heatmap_df, annot=True, fmt=".3f", cmap="Blues")
    plt.title("Test Accuracy Heatmap")
    plt.tight_layout()
    plt.savefig(RESULT_DIR / "test_accuracy_heatmap.png", dpi=200)
    plt.close()


def run_pipeline() -> None:
    ensure_dirs()
    df, domain_map = load_inputs()
    models = define_models()

    all_results = []
    for domain, cfg in domain_map.items():
        all_results.append(train_all_models_for_domain(domain, cfg, df, models))

    final_results_df = pd.concat(all_results, ignore_index=True)
    final_results_df = final_results_df.sort_values(
        by=["Domain", "TestAccuracy"], ascending=[True, False]
    )
    final_results_df.to_csv(RESULT_DIR / "model_results.csv", index=False)
    save_visualizations(final_results_df)

    summary = final_results_df.loc[final_results_df.groupby("Domain")["TestAccuracy"].idxmax()]
    summary.to_csv(RESULT_DIR / "best_models_summary.csv", index=False)

    print("Pipeline completed.")
    print(f"Saved outputs to: {RESULT_DIR}")


if __name__ == "__main__":
    run_pipeline()
