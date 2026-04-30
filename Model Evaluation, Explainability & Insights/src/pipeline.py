from __future__ import annotations

from pathlib import Path

import joblib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.metrics import (
    accuracy_score,
    auc,
    classification_report,
    confusion_matrix,
    f1_score,
    roc_curve,
)
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, label_binarize


ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = ROOT_DIR / "dataset" / "feature_engineered_data.csv"
ROLE3_RESULTS_PATH = ROOT_DIR / "role3_model_results.csv"
RESULT_DIR = ROOT_DIR / "src" / "result"

TARGET_MAP = {
    "food": "food_security_label",
    "fuel": "fuel_security_label",
    "child": "child_security_label",
}


def resolve_model_path(raw_model_path: str) -> Path:
    parts = raw_model_path.replace("\\", "/").split("/")
    return ROOT_DIR.joinpath(*parts)


def evaluate_domain(
    model,
    model_name: str,
    domain: str,
    x_data: pd.DataFrame,
    y_data: pd.Series,
) -> tuple[dict, str]:
    label_encoder = LabelEncoder()
    y_encoded = label_encoder.fit_transform(y_data.astype(str))

    x_train, x_test, y_train, y_test = train_test_split(
        x_data,
        y_encoded,
        test_size=0.25,
        random_state=42,
        stratify=y_encoded,
    )

    y_train_pred = model.predict(x_train)
    y_test_pred = model.predict(x_test)

    train_acc = accuracy_score(y_train, y_train_pred)
    test_acc = accuracy_score(y_test, y_test_pred)
    train_error = 1 - train_acc
    test_error = 1 - test_acc
    error_gap = test_error - train_error
    f1_weighted = f1_score(y_test, y_test_pred, average="weighted", zero_division=0)

    report_text = classification_report(y_test, y_test_pred, zero_division=0)

    cm = confusion_matrix(y_test, y_test_pred)
    plt.figure(figsize=(6, 5))
    sns.heatmap(
        cm,
        annot=True,
        fmt="d",
        cmap="Blues",
        xticklabels=label_encoder.classes_,
        yticklabels=label_encoder.classes_,
    )
    plt.title(f"{domain.upper()} - Confusion Matrix ({model_name})")
    plt.xlabel("Predicted")
    plt.ylabel("Actual")
    plt.tight_layout()
    plt.savefig(RESULT_DIR / f"{domain}_confusion_matrix.png", dpi=300)
    plt.close()

    error_df = pd.DataFrame(
        {"Type": ["Train Error", "Test Error"], "Value": [train_error, test_error]}
    )
    plt.figure(figsize=(5, 4))
    sns.barplot(data=error_df, x="Type", y="Value")
    plt.title(f"{domain.upper()} - Train vs Test Error ({model_name})")
    plt.ylabel("Error")
    plt.ylim(0, 1)
    plt.tight_layout()
    plt.savefig(RESULT_DIR / f"{domain}_train_vs_test_error_best_model.png", dpi=300)
    plt.close()

    if hasattr(model, "predict_proba") and len(np.unique(y_test)) > 1:
        y_prob = model.predict_proba(x_test)
        n_classes = len(np.unique(y_test))
        y_bin = label_binarize(y_test, classes=np.arange(n_classes))

        plt.figure(figsize=(6, 5))
        plotted = False
        for class_idx in range(n_classes):
            if len(np.unique(y_bin[:, class_idx])) < 2:
                continue
            fpr, tpr, _ = roc_curve(y_bin[:, class_idx], y_prob[:, class_idx])
            roc_auc = auc(fpr, tpr)
            plt.plot(fpr, tpr, label=f"Class {class_idx} AUC={roc_auc:.2f}")
            plotted = True

        if plotted:
            plt.plot([0, 1], [0, 1], linestyle="--")
            plt.title(f"{domain.upper()} - ROC Curve ({model_name})")
            plt.xlabel("False Positive Rate")
            plt.ylabel("True Positive Rate")
            plt.legend()
            plt.tight_layout()
            plt.savefig(RESULT_DIR / f"{domain}_roc_curve.png", dpi=300)
        plt.close()

    summary_row = {
        "Domain": domain,
        "BestModel": model_name,
        "Accuracy": test_acc,
        "F1Score": f1_weighted,
        "TrainError": train_error,
        "TestError": test_error,
        "ErrorGap": error_gap,
    }
    return summary_row, report_text


def plot_best_model_comparison(summary_df: pd.DataFrame) -> None:
    plt.figure(figsize=(10, 6))
    sns.barplot(data=summary_df, x="Domain", y="Accuracy", hue="BestModel")
    plt.title("Best Model Accuracy by Domain")
    plt.ylim(0, 1)
    plt.tight_layout()
    plt.savefig(RESULT_DIR / "best_model_accuracy_by_domain.png", dpi=300)
    plt.close()

    plt.figure(figsize=(10, 6))
    sns.barplot(data=summary_df, x="Domain", y="ErrorGap", hue="BestModel")
    plt.title("Overfitting Gap by Domain")
    plt.tight_layout()
    plt.savefig(RESULT_DIR / "best_model_overfitting_gap_by_domain.png", dpi=300)
    plt.close()


def plot_all_models_train_test_accuracy(results_df: pd.DataFrame) -> None:
    plot_df = results_df.melt(
        id_vars=["Domain", "Model"],
        value_vars=["TrainAccuracy", "TestAccuracy"],
        var_name="Metric",
        value_name="Accuracy",
    )
    plot_df["Metric"] = plot_df["Metric"].replace(
        {"TrainAccuracy": "Train Accuracy", "TestAccuracy": "Test Accuracy"}
    )

    for domain in results_df["Domain"].unique():
        domain_df = plot_df[plot_df["Domain"] == domain]
        plt.figure(figsize=(10, 6))
        sns.barplot(data=domain_df, x="Model", y="Accuracy", hue="Metric")
        plt.title(f"{domain.upper()} - Train vs Test Accuracy")
        plt.xlabel("Model")
        plt.ylabel("Accuracy")
        plt.ylim(0, 1)
        plt.tight_layout()
        plt.savefig(
            RESULT_DIR / f"{domain}_all_models_train_vs_test_accuracy.png",
            dpi=300,
        )
        plt.close()


def plot_all_models_train_test_error(results_df: pd.DataFrame) -> None:
    plot_df = results_df.melt(
        id_vars=["Domain", "Model"],
        value_vars=["TrainError", "TestError"],
        var_name="Metric",
        value_name="Error",
    )
    plot_df["Metric"] = plot_df["Metric"].replace(
        {"TrainError": "Train Error", "TestError": "Test Error"}
    )

    for domain in results_df["Domain"].unique():
        domain_df = plot_df[plot_df["Domain"] == domain]
        plt.figure(figsize=(10, 6))
        sns.barplot(data=domain_df, x="Model", y="Error", hue="Metric")
        plt.title(f"{domain.upper()} - Train vs Test Error")
        plt.xlabel("Model")
        plt.ylabel("Error")
        plt.ylim(0, 1)
        plt.tight_layout()
        plt.savefig(
            RESULT_DIR / f"{domain}_all_models_train_vs_test_error.png",
            dpi=300,
        )
        plt.close()


def main() -> None:
    RESULT_DIR.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(DATA_PATH)
    results_df = pd.read_csv(ROLE3_RESULTS_PATH)

    # Kept aligned with main.ipynb: evaluate XGBoost rows from role3 results.
    best_models = results_df[results_df["Model"] == "XGBoost"].reset_index(drop=True)

    summary_rows: list[dict] = []
    domain_reports: dict[str, str] = {}
    for _, row in best_models.iterrows():
        domain = row["Domain"]
        model_name = row["Model"]
        model = joblib.load(resolve_model_path(row["ModelPath"]))
        target_col = TARGET_MAP[domain]

        x_data = df.drop(
            columns=[
                "food_security_label",
                "fuel_security_label",
                "child_security_label",
            ],
            errors="ignore",
        )
        y_data = df[target_col].copy()
        mask = y_data.notna()
        x_data = x_data.loc[mask]
        y_data = y_data.loc[mask]

        summary_row, report_text = evaluate_domain(
            model=model,
            model_name=model_name,
            domain=domain,
            x_data=x_data,
            y_data=y_data,
        )
        summary_rows.append(summary_row)
        domain_reports[domain] = report_text

    summary_df = pd.DataFrame(summary_rows)
    summary_df.to_csv(RESULT_DIR / "best_model_summary.csv", index=False)

    reports_path = RESULT_DIR / "classification_reports.txt"
    with reports_path.open("w", encoding="utf-8") as file:
        for domain, report in domain_reports.items():
            file.write("=" * 80 + "\n")
            file.write(f"DOMAIN: {domain.upper()}\n")
            file.write("=" * 80 + "\n")
            file.write(report.strip() + "\n\n")

    plot_best_model_comparison(summary_df)
    plot_all_models_train_test_accuracy(results_df)
    plot_all_models_train_test_error(results_df)

    print(f"Pipeline completed. Results saved in: {RESULT_DIR}")


if __name__ == "__main__":
    main()
