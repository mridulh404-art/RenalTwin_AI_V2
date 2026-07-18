"""
RenalTwin AI V2
Central Feature Configuration
"""

# ==========================================================
# Feature Sets
# ==========================================================

MODEL_FEATURES = {

    "Model A": [

        "RIDAGEYR",
        "Female",
        "RIDRETH3",

        "BMXBMI",
        "BMXWAIST",

        "Mean_SBP",
        "Mean_DBP",

        "Diabetes",
        "Smoker",

        "LBXPLTSI",
        "LBDNENO",
        "LBDLYMNO",

        "LBXHGB",

        "SII",

    ],

    "Model B": [

        "RIDAGEYR",
        "Female",
        "RIDRETH3",

        "BMXBMI",
        "BMXWAIST",

        "Mean_SBP",
        "Mean_DBP",

        "Diabetes",
        "Smoker",

        "LBXPLTSI",
        "LBDNENO",
        "LBDLYMNO",

        "LBXHGB",

        "SII",

        "LBXSCR",
        "LBDSALSI",

    ],

    "Model C": [

        "RIDAGEYR",
        "Female",
        "RIDRETH3",

        "BMXBMI",
        "BMXWAIST",

        "Mean_SBP",
        "Mean_DBP",

        "Diabetes",
        "Smoker",

        "LBXPLTSI",
        "LBDNENO",
        "LBDLYMNO",

        "LBXHGB",

        "SII",

        "LBXSCR",
        "LBDSALSI",

        "eGFR",

        "URDACT",

    ],

}

# ==========================================================
# Recommended Thresholds
# ==========================================================

MODEL_THRESHOLDS = {

    "Model A": 0.50,

    "Model B": 0.40,

    "Model C": 0.50,

}

# ==========================================================
# User-Friendly Labels
# ==========================================================

FEATURE_LABELS = {

    "RIDAGEYR": "Age (years)",

    "Female": "Female",

    "RIDRETH3": "Race/Ethnicity",

    "BMXBMI": "BMI (kg/m²)",

    "BMXWAIST": "Waist Circumference (cm)",

    "Mean_SBP": "Mean Systolic BP (mmHg)",

    "Mean_DBP": "Mean Diastolic BP (mmHg)",

    "Diabetes": "Diabetes",

    "Smoker": "Smoking Status",

    "LBXPLTSI": "Platelet Count",

    "LBDNENO": "Neutrophil Count",

    "LBDLYMNO": "Lymphocyte Count",

    "LBXHGB": "Hemoglobin (g/dL)",

    "SII": "Systemic Immune-Inflammation Index",

    "LBXSCR": "Serum Creatinine (mg/dL)",

    "LBDSALSI": "Serum Albumin (g/L)",

    "eGFR": "Estimated GFR",

    "URDACT": "Urine Albumin/Creatinine Ratio",

}