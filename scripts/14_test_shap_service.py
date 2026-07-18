from engine.shap_service import get_top_features

patient = {

    "RIDAGEYR": 65,
    "Female": 1,
    "RIDRETH3": 3,

    "BMXBMI": 31,
    "BMXWAIST": 102,

    "Mean_SBP": 155,
    "Mean_DBP": 92,

    "Diabetes": 1,
    "Smoker": 0,

    "LBXPLTSI": 260,
    "LBDNENO": 4.8,
    "LBDLYMNO": 1.8,

    "LBXHGB": 12.4,

    "SII": 690,

    "LBXSCR": 2.0,
    "LBDSALSI": 38,

    "eGFR": 42,
    "URDACT": 320,
}

print(
    get_top_features(
        patient,
        "Model B",
    )
)