import sys
from pathlib import Path

# Add project root to Python path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT))

import pandas as pd

from engine.digital_twin import simulate


# ==========================================
# Example Patient Profile
# ==========================================

patient = {

    "RIDAGEYR": 65,

    "BMXBMI": 29,

    "Mean_SBP": 150,

    "Mean_DBP": 85,

    "LBXSCR": 1.8,

    "LBXHGB": 13,

    "SII": 600,

    "LBXPLTSI": 250,

    "BMXWAIST": 105,

    "LBDNENO": 4,

    "Diabetes": 1,

    "LBDLYMNO": 2,

    "LBDSALSI": 40,

    "RIDRETH3": 3,

    "Female": 0,

    "Smoker": 1,

}


# ==========================================
# Simulation Scenarios
# ==========================================

scenarios = {


    "Baseline State":
    {},


    "Blood Pressure Optimization":
    {
        "Mean_SBP": 120,
        "Mean_DBP": 75,
    },


    "Renal Function Improvement":
    {
        "LBXSCR": 1.0,
    },


    "Metabolic Risk Optimization":
    {
        "BMXBMI": 24,
        "Smoker": 0,
    },


    "Combined Intervention":
    {
        "Mean_SBP":120,
        "Mean_DBP":75,
        "LBXSCR":1.0,
        "BMXBMI":24,
        "Smoker":0,
    }

}


results = []


for name, changes in scenarios.items():


    output = simulate(

        patient,

        changes,

        model_name="Model B"

    )


    original = output["original"]

    simulated = output["simulated"]


    results.append({

        "Scenario": name,

        "Changes": str(changes),

        "Baseline Risk":
        round(original["Probability"],4),


        "Simulated Risk":
        round(simulated["Probability"],4),


        "Risk Reduction":
        round(
            original["Probability"]
            -
            simulated["Probability"],
            4
        )

    })


df = pd.DataFrame(results)


df.to_csv(

    "outputs/metrics/digital_twin_results.csv",

    index=False

)


print(df)

print(
    "\nSaved: outputs/metrics/digital_twin_results.csv"
)