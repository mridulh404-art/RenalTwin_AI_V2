from pathlib import Path
import sys

# ----------------------------------------------------------
# Add project root to Python path
# ----------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent

sys.path.append(str(PROJECT_ROOT))

from engine.predictor import predict

# ==========================================================
# Test Patient
# ==========================================================

patient = {

    "RIDAGEYR": 58,

    "Female": 1,

    "RIDRETH3": 3,

    "BMXBMI": 30.2,

    "BMXWAIST": 102,

    "Mean_SBP": 148,

    "Mean_DBP": 92,

    "Diabetes": 1,

    "Smoker": 0,

    "LBXPLTSI": 245,

    "LBDNENO": 4.8,

    "LBDLYMNO": 1.8,

    "LBXHGB": 12.1,

    "SII": 653,

    "LBXSCR": 1.62,

    "LBDSALSI": 39,

    "eGFR": 52,

    "URDACT": 145,

}

# ----------------------------------------------------------
# Test All Models
# ----------------------------------------------------------

for model in [

    "Model A",

    "Model B",

    "Model C",

]:

    print("=" * 80)

    print(model)

    print("=" * 80)

    result = predict(

        patient,

        model,

    )

    for key, value in result.items():

        print(f"{key}: {value}")

    print()