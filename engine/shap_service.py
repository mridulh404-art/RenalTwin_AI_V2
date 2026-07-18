from pathlib import Path

import joblib
import pandas as pd
import shap

from config.feature_config import MODEL_FEATURES

# ==========================================================
# RenalTwin AI V2
# SHAP Service
# ==========================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent


MODEL_PATHS = {
    "Model A": PROJECT_ROOT / "trained_models" / "Model_A_random_forest.pkl",
    "Model B": PROJECT_ROOT / "trained_models" / "Model_B_random_forest.pkl",
    "Model C": PROJECT_ROOT / "trained_models" / "Model_C_random_forest.pkl",
}


def get_top_features(patient_data: dict,
                     model_name: str = "Model B",
                     top_n: int = 5):
    """
    Return Top SHAP Features
    """

    model = joblib.load(MODEL_PATHS[model_name])

    features = MODEL_FEATURES[model_name]

    X = pd.DataFrame(
        [[patient_data[f] for f in features]],
        columns=features,
    )

    explainer = shap.TreeExplainer(model)

    shap_values = explainer(X)

    values = shap_values.values

    # Binary classifier
    if values.ndim == 3:
        values = values[:, :, 1]

    importance = abs(values[0])

    result = pd.DataFrame({

        "Feature": features,

        "Importance": importance,

    })

    result = result.sort_values(
        "Importance",
        ascending=False,
    )

    return result.head(top_n)