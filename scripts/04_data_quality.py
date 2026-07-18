from pathlib import Path

import pandas as pd

# ==========================================================
# RenalTwin AI Version 2
# Data Quality Assessment
# ==========================================================

PROJECT_ROOT = Path(r"G:\PROJECTS\RenalTwin_AI_V2")

print("=" * 80)
print("RenalTwin AI V2 - Data Quality Assessment")
print("=" * 80)

# ----------------------------------------------------------
# Load dataset
# ----------------------------------------------------------

df = pd.read_csv(
    PROJECT_ROOT / "data/processed/renal_twin_engineered.csv"
)

# ----------------------------------------------------------
# Keep adults only
# ----------------------------------------------------------

df = df[df["RIDAGEYR"] >= 18].copy()

print(f"\nAdult Dataset Shape: {df.shape}")

# ----------------------------------------------------------
# Missing Values
# ----------------------------------------------------------

print("\n" + "=" * 80)
print("Missing Values")
print("=" * 80)

missing = pd.DataFrame({
    "Variable": df.columns,
    "Missing": df.isna().sum().values,
    "Percent": (
        df.isna().mean() * 100
    ).round(2).values
})

missing = missing.sort_values(
    "Percent",
    ascending=False
)

print(missing)

# Save report
reports = PROJECT_ROOT / "outputs" / "reports"
reports.mkdir(parents=True, exist_ok=True)

missing.to_csv(
    reports / "missing_values_report.csv",
    index=False
)

# ----------------------------------------------------------
# Summary Statistics
# ----------------------------------------------------------

print("\n" + "=" * 80)
print("Summary Statistics")
print("=" * 80)

summary = df.describe(include="all")

print(summary)

summary.to_csv(
    reports / "summary_statistics.csv"
)

# ----------------------------------------------------------
# CKD Distribution
# ----------------------------------------------------------

print("\n" + "=" * 80)
print("CKD Indicator Distribution")
print("=" * 80)

ckd = df["CKD"].value_counts(dropna=False)

print(ckd)

ckd.to_csv(
    reports / "ckd_distribution.csv"
)

# ----------------------------------------------------------
# CKD Stage Distribution
# ----------------------------------------------------------

print("\n" + "=" * 80)
print("CKD Stage Distribution")
print("=" * 80)

stage = df["CKD_Stage"].value_counts(dropna=False)

print(stage)

stage.to_csv(
    reports / "ckd_stage_distribution.csv"
)

# ----------------------------------------------------------
# Albuminuria Distribution
# ----------------------------------------------------------

print("\n" + "=" * 80)
print("Albuminuria Distribution")
print("=" * 80)

album = df["Albuminuria"].value_counts(dropna=False)

print(album)

album.to_csv(
    reports / "albuminuria_distribution.csv"
)

# ----------------------------------------------------------
# Numeric Outlier Summary
# ----------------------------------------------------------

print("\n" + "=" * 80)
print("Potential Outliers (IQR Method)")
print("=" * 80)

numeric = df.select_dtypes(include="number")

rows = []

for col in numeric.columns:

    q1 = numeric[col].quantile(0.25)
    q3 = numeric[col].quantile(0.75)

    iqr = q3 - q1

    lower = q1 - 1.5 * iqr
    upper = q3 + 1.5 * iqr

    outliers = (
        (numeric[col] < lower)
        |
        (numeric[col] > upper)
    ).sum()

    rows.append({
        "Variable": col,
        "Outliers": int(outliers)
    })

outliers = pd.DataFrame(rows)

print(outliers)

outliers.to_csv(
    reports / "outlier_report.csv",
    index=False
)

print("\n" + "=" * 80)
print("Data Quality Assessment Complete")
print("=" * 80)