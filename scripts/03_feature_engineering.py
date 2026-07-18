from pathlib import Path
import numpy as np
import pandas as pd

# ==========================================================
# RenalTwin AI Version 2
# Feature Engineering
# ==========================================================

PROJECT_ROOT = Path(r"G:\PROJECTS\RenalTwin_AI_V2")

print("=" * 80)
print("RenalTwin AI V2 - Feature Engineering")
print("=" * 80)

# ----------------------------------------------------------
# Load merged dataset
# ----------------------------------------------------------

master = pd.read_csv(
    PROJECT_ROOT / "data/processed/renal_twin_master.csv"
)

print(f"Loaded dataset: {master.shape}")

# ----------------------------------------------------------
# Mean Blood Pressure
# ----------------------------------------------------------

master["Mean_SBP"] = master[
    [
        "BPXSY1",
        "BPXSY2",
        "BPXSY3",
        "BPXSY4",
    ]
].mean(axis=1)

master["Mean_DBP"] = master[
    [
        "BPXDI1",
        "BPXDI2",
        "BPXDI3",
        "BPXDI4",
    ]
].mean(axis=1)

print("✓ Mean Blood Pressure calculated")

# ----------------------------------------------------------
# Systemic Immune-Inflammation Index (SII)
# ----------------------------------------------------------

master["SII"] = (
    master["LBXPLTSI"]
    * master["LBDNENO"]
) / master["LBDLYMNO"]

master.loc[
    master["LBDLYMNO"] <= 0,
    "SII"
] = np.nan

print("✓ SII calculated")

# ----------------------------------------------------------
# CKD-EPI 2021 eGFR
# ----------------------------------------------------------

def calculate_egfr(row):

    creatinine = row["LBXSCR"]
    age = row["RIDAGEYR"]
    female = row["RIAGENDR"] == 2

    if pd.isna(creatinine):
        return np.nan

    if female:
        k = 0.7
        alpha = -0.241
        sex_factor = 1.012
    else:
        k = 0.9
        alpha = -0.302
        sex_factor = 1.0

    return (
        142
        * min(creatinine / k, 1) ** alpha
        * max(creatinine / k, 1) ** (-1.200)
        * (0.9938 ** age)
        * sex_factor
    )

master["eGFR"] = master.apply(
    calculate_egfr,
    axis=1,
)

print("✓ eGFR calculated")

# ----------------------------------------------------------
# CKD Stage
# ----------------------------------------------------------

def ckd_stage(egfr):

    if pd.isna(egfr):
        return np.nan

    if egfr >= 90:
        return "G1"

    elif egfr >= 60:
        return "G2"

    elif egfr >= 45:
        return "G3a"

    elif egfr >= 30:
        return "G3b"

    elif egfr >= 15:
        return "G4"

    return "G5"

master["CKD_Stage"] = master["eGFR"].apply(
    ckd_stage
)

print("✓ CKD Stage created")

# ----------------------------------------------------------
# Albuminuria Category (KDIGO)
# ----------------------------------------------------------

def albumin_stage(uacr):

    if pd.isna(uacr):
        return np.nan

    if uacr < 30:
        return "A1"

    elif uacr < 300:
        return "A2"

    return "A3"

master["Albuminuria"] = master["URDACT"].apply(
    albumin_stage
)

print("✓ Albuminuria category created")

# ----------------------------------------------------------
# CKD Label
# ----------------------------------------------------------

master["CKD"] = np.where(

    (master["eGFR"] < 60)

    |

    (master["URDACT"] >= 30),

    1,

    0,

)

print("✓ CKD outcome created")

# ----------------------------------------------------------
# Save
# ----------------------------------------------------------

output = PROJECT_ROOT / "data/processed"

master.to_csv(

    output / "renal_twin_engineered.csv",

    index=False,

)

print()

print("=" * 80)
print("Feature engineering completed successfully.")
print("=" * 80)

print(master.shape)

print()

print(master[
    [
        "Mean_SBP",
        "Mean_DBP",
        "SII",
        "eGFR",
        "CKD_Stage",
        "Albuminuria",
        "CKD",
    ]
].head())