from pathlib import Path
import joblib

from config.feature_config import MODEL_THRESHOLDS

# ==========================================================
# RenalTwin AI V2
# Model Loader
# ==========================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

# ----------------------------------------------------------
# Model Paths
# ----------------------------------------------------------

MODEL_PATHS = {

    "Model A":
        PROJECT_ROOT / "trained_models" / "Model_A_random_forest.pkl",

    "Model B":
        PROJECT_ROOT / "trained_models" / "Model_B_random_forest.pkl",

    "Model C":
        PROJECT_ROOT / "trained_models" / "Model_C_random_forest.pkl",

}


# ----------------------------------------------------------
# Load Model
# ----------------------------------------------------------

def load_model(model_name: str):
    """
    Load a trained AI model.

    Parameters
    ----------
    model_name : str
        Model A, Model B or Model C

    Returns
    -------
    sklearn model
    """

    if model_name not in MODEL_PATHS:
        raise ValueError(
            f"Unknown model: {model_name}"
        )

    model_path = MODEL_PATHS[model_name]

    if not model_path.exists():
        raise FileNotFoundError(
            f"Model file not found:\n{model_path}"
        )

    return joblib.load(model_path)


# ----------------------------------------------------------
# Get Threshold
# ----------------------------------------------------------

def get_threshold(model_name: str):
    """
    Return the recommended probability threshold.
    """

    if model_name not in MODEL_THRESHOLDS:
        raise ValueError(
            f"Unknown model: {model_name}"
        )

    return MODEL_THRESHOLDS[model_name]


# ----------------------------------------------------------
# Available Models
# ----------------------------------------------------------

def available_models():
    """
    Return available AI models.
    """

    return list(MODEL_PATHS.keys())