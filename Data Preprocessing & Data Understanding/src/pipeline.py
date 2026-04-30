from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = ROOT_DIR / "Food_insecurity_Raw_Survey_Responses.xlsx"
RESULT_DIR = Path(__file__).resolve().parent / "result"
RESULT_DIR.mkdir(parents=True, exist_ok=True)


def _classify_adult_food(score: float) -> str:
    if score == 0:
        return "High"
    if score <= 2:
        return "Marginal"
    if score <= 5:
        return "Low"
    return "Very Low"


def _classify_child_food(score: float) -> str:
    if score == 0:
        return "High"
    if score == 1:
        return "Marginal"
    if score <= 4:
        return "Low"
    return "Very Low"


def _classify_fuel(score: float) -> str:
    if score == 0:
        return "Secure"
    if score <= 2:
        return "Moderate Risk"
    return "High Risk"


def _plot_label_distribution(df: pd.DataFrame, column: str, output_name: str, order: list[str]) -> None:
    plt.figure(figsize=(8, 4))
    sns.countplot(data=df, x=column, order=order, color="#4c72b0")
    plt.title(f"{column} distribution")
    plt.xlabel(column)
    plt.ylabel("Count")
    plt.tight_layout()
    plt.savefig(RESULT_DIR / output_name, dpi=150)
    plt.close()


def _plot_score_distribution(df: pd.DataFrame, column: str, output_name: str) -> None:
    plt.figure(figsize=(8, 4))
    sns.histplot(df[column], bins=20, kde=False, color="#55a868")
    plt.title(f"{column} distribution")
    plt.xlabel(column)
    plt.ylabel("Count")
    plt.tight_layout()
    plt.savefig(RESULT_DIR / output_name, dpi=150)
    plt.close()


def main() -> None:
    pd.set_option("display.max_columns", None)
    sns.set_theme(style="whitegrid")

    xls = pd.ExcelFile(DATA_FILE)
    sheet_names = xls.sheet_names

    df1 = pd.read_excel(DATA_FILE, sheet_name="2022-12-03_incentivised")
    df2 = pd.read_excel(DATA_FILE, sheet_name="2022-11-22_27_incentivised")
    df3 = pd.read_excel(DATA_FILE, sheet_name="2022-11-22_27_non_incentivised")
    df = pd.concat([df1, df2, df3], ignore_index=True)

    consent_col = (
        "By agreeing to take part in this survey, you confirm that you have read, understood and agreed with the following statements. "
        "Please note that this survey will skip to the end if you disagree to take part: \n \n "
        "_I agree that data gathered in this study will be stored anonymously and securely, and will be used for research purposes only. _\n \n "
        "_I understand that my participation is voluntary and that I am free to withdraw at any time without giving reason. _\n \n "
        "_I understand that all personal information will remain confidentially within OLIOâ€™s database, and that no personally identifiable "
        "information will be shared with any third party, and that no data will be made available that can allow me to be personally identified "
        "in the results of this research. _\n \n _I am 18 years of age or older. _\n \n I agree to take part in this survey:"
    )
    if consent_col not in df.columns:
        fallback = [c for c in df.columns if "By agreeing to take part in this survey" in c]
        if not fallback:
            raise KeyError("Consent column not found in source data.")
        consent_col = fallback[0]
    df = df[df[consent_col] == 1].copy()

    rename_map = {
        "The next questions are about your householdâ€™s diet in the past 12 months, since October of last year, and whether you were able to afford the food you needed. In the past 12 months, was the following statement true for you?\n \n We worried whether our food would run out before we got money to buy more.": "food_worry",
        "The food that we bought just didn't last, and we didn't have money to get more.": "food_not_last",
        "We couldnâ€™t afford to eat balanced meals.": "no_balanced_meal",
        "The next questions are about the food situation of your children. In the past 12 months, was the following statement true for you? \n \n We relied on only a few kinds of low-cost food to feed our children because we were running out of money to buy food.": "We relied on only a few kinds of low-cost food to feed our children because we were running out of money to buy food",
        "We couldnâ€™t feed our children a balanced meal, because we couldnâ€™t afford that.": "We couldn't feed our children a balanced meal, because we couldn't afford that.",
        "Did you ever cut the size of any of the children€™s meals because there wasn't enough money for food?": "Did you ever cut the size of any of the children's meals because there wasn't enough money for food?",
        "The following questions are about challenges your household may have had paying energy bills or maintaining heating in your home in the past 12 months. \n \n How frequently did your household reduce or forego expenses for basic household necessities, such as medicine or food, in order to pay an energy bill?": "How frequently did your household reduce or forego expenses for basic household necessities, such as medicine or food, in order to pay an energy bill?",
        "In the last year, was there ever a time your household was unable to use your main source of heat because you could not afford to pay for gas or electricity?": "In the last year, was there ever a time your household was unable to use your main source of heat because you could not afford to pay for gas or electricity?",
        "In the last year, was there ever a time your household was unable to use your main source of heat because the equipment was broken, and you couldnâ€™t afford to pay to repair or replace the equipment?": "In the last year, was there ever a time your household was unable to use your main source of heat because the equipment was broken, and you couldn't afford to pay to repair or replace the equipment?",
    }
    df.rename(columns=rename_map, inplace=True)

    if "food_not_last" not in df.columns:
        fallback_cols = [c for c in df.columns if "The food that we bought just" in c and "have money to get more" in c]
        if fallback_cols:
            df.rename(columns={fallback_cols[0]: "food_not_last"}, inplace=True)

    food_cols = [
        "food_worry",
        "food_not_last",
        "no_balanced_meal",
        "Did you or other adults in your household ever cut the size of your meals or skip meals because there wasn't enough money for food?",
        "How often did this happen?",
        "Did you ever eat less than you felt you should because there wasn't enough money for food?",
        "Were you ever hungry but didn't eat because there wasn't enough money for food?",
        "Did you lose weight because there wasn't enough money for food?",
        "Did you or other adults in your household ever not eat for a whole day because there wasn't enough money for food?",
        "How often did this happen?.1",
    ]

    child_cols = [
        "We relied on only a few kinds of low-cost food to feed our children because we were running out of money to buy food",
        "We couldn't feed our children a balanced meal, because we couldn't afford that.",
        "The children were not eating enough because we just couldn't afford enough food.",
        "Did you ever cut the size of any of the children's meals because there wasn't enough money for food?",
        "Did any of the children ever skip meals because there wasn't enough money for food?",
        "Were the children ever hungry but you just couldn't afford more food?",
        "Did any of the children ever not eat for a whole day because there wasn't enough money for food?",
        "How often did this happen?.2",
    ]

    fuel_cols = [
        "How frequently did your household reduce or forego expenses for basic household necessities, such as medicine or food, in order to pay an energy bill?",
        "In the past year, how frequently did your household keep your home at a cold temperature that you felt was unsafe or unhealthy?",
        "In the past year, how frequently did your household run behind on payments for energy bills, or receive a notice to disconnect?",
        "In the last year, was there ever a time your household was unable to use your main source of heat because you could not afford to pay for gas or electricity?",
        "About how many days over the past year has your household gone without heat because you could not afford to pay for gas or electricity?",
        "In the last year, was there ever a time your household was unable to use your main source of heat because the equipment was broken, and you couldn't afford to pay to repair or replace the equipment?",
        "In the past year, did anyone in your household need medical attention because your home was too cold?",
    ]

    mapping_dict = {
        "Often true": 1,
        "Sometimes true": 1,
        "Yes": 1,
        "Almost every month": 1,
        "Some months": 1,
        ">=36": 1,
        "Never true": 0,
        "No": 0,
        "Only 1 or 2 months": 0,
        "Never": 0,
        "<36": 0,
        "DK": 0,
    }

    all_cols = food_cols + child_cols + fuel_cols
    for col in all_cols:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()
            df[col] = df[col].replace(mapping_dict)
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

    heating_days_col = "About how many days over the past year has your household gone without heat because you could not afford to pay for gas or electricity?"
    if heating_days_col in df.columns:
        df[heating_days_col] = df[heating_days_col].fillna(0)
        df[heating_days_col] = df[heating_days_col].apply(lambda x: 1 if float(x) >= 36 else 0)

    valid_food_cols = [c for c in food_cols if c in df.columns]
    valid_child_cols = [c for c in child_cols if c in df.columns]
    valid_fuel_cols = [c for c in fuel_cols if c in df.columns]

    df["food_security_score"] = df[valid_food_cols].sum(axis=1) if valid_food_cols else 0
    df["child_security_score"] = df[valid_child_cols].sum(axis=1) if valid_child_cols else 0
    df["fuel_security_score"] = df[valid_fuel_cols].sum(axis=1) if valid_fuel_cols else 0

    df["food_security_label"] = df["food_security_score"].apply(_classify_adult_food)
    df["child_security_label"] = df["child_security_score"].apply(_classify_child_food)
    df["fuel_security_label"] = df["fuel_security_score"].apply(_classify_fuel)

    support_cols = [
        "Foodbank",
        "Community or faith group",
        "Close family or friends",
        "Neighbours",
    ]
    for support_col in support_cols:
        if support_col in df.columns:
            df[support_col] = df[support_col].eq(support_col).astype(int)

    output_csv = RESULT_DIR / "cleaned_dataset_role01.csv"
    df.to_csv(output_csv, index=False)

    summary = {
        "input_file": str(DATA_FILE.name),
        "sheets_found": sheet_names,
        "rows_after_processing": int(df.shape[0]),
        "columns_after_processing": int(df.shape[1]),
        "duplicate_rows_after_consent_filter": int(df.duplicated().sum()),
        "food_label_distribution": df["food_security_label"].value_counts(dropna=False).to_dict(),
        "child_label_distribution": df["child_security_label"].value_counts(dropna=False).to_dict(),
        "fuel_label_distribution": df["fuel_security_label"].value_counts(dropna=False).to_dict(),
    }
    (RESULT_DIR / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

    _plot_label_distribution(
        df=df,
        column="food_security_label",
        output_name="food_security_label_distribution.png",
        order=["High", "Marginal", "Low", "Very Low"],
    )
    _plot_label_distribution(
        df=df,
        column="child_security_label",
        output_name="child_security_label_distribution.png",
        order=["High", "Marginal", "Low", "Very Low"],
    )
    _plot_label_distribution(
        df=df,
        column="fuel_security_label",
        output_name="fuel_security_label_distribution.png",
        order=["Secure", "Moderate Risk", "High Risk"],
    )

    _plot_score_distribution(df, "food_security_score", "food_security_score_distribution.png")
    _plot_score_distribution(df, "child_security_score", "child_security_score_distribution.png")
    _plot_score_distribution(df, "fuel_security_score", "fuel_security_score_distribution.png")

    print(f"Pipeline complete. Outputs saved to: {RESULT_DIR}")


if __name__ == "__main__":
    main()
