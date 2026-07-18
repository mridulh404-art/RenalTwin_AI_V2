from engine.model_loader import load_model, get_threshold
from config.feature_config import MODEL_FEATURES

import pandas as pd

# ==========================================================
# RenalTwin AI V2
# Prediction Engine
# ==========================================================


def predict(patient_data: dict, model_name: str = "Model B"):
    """
    Predict CKD risk.

    Parameters
    ----------
    patient_data : dict
        Dictionary containing patient features.

    model_name : str
        Model A, Model B or Model C

    Returns
    -------
    dict
    """

    # ------------------------------------------------------
    # Load model
    # ------------------------------------------------------

    model = load_model(model_name)

    threshold = get_threshold(model_name)

    features = MODEL_FEATURES[model_name]

    # ------------------------------------------------------
    # Prepare Input
    # ------------------------------------------------------

    values = pd.DataFrame(

        [[patient_data[f] for f in features]],

        columns=features,

    )

    # ------------------------------------------------------
    # Prediction
    # ------------------------------------------------------

    probability = float(
        model.predict_proba(values)[0][1]
    )

    prediction = int(
        probability >= threshold
    )

    # ------------------------------------------------------
    # Risk Category
    # ------------------------------------------------------

    if probability < 0.20:

        risk = "Low"

    elif probability < 0.40:

        risk = "Moderate"

    elif probability < 0.70:

        risk = "High"

    else:

        risk = "Very High"

    # ------------------------------------------------------
    # Recommendation
    # ------------------------------------------------------

    if prediction == 0:

        recommendation = (
            "Current findings suggest a lower likelihood of CKD. "
            "Continue routine health monitoring and maintain a healthy lifestyle."
        )

    else:

        recommendation = (
            "This patient is at increased risk of CKD. "
            "Further clinical evaluation, including renal function assessment "
            "and nephrology consultation if appropriate, is recommended."
        )

    # ------------------------------------------------------
    # Return
    # ------------------------------------------------------

    return {

        "Model": model_name,

        "Probability": probability,

        "Threshold": threshold,

        "Prediction": prediction,

        "Risk": risk,

        "Recommendation": recommendation,

    }