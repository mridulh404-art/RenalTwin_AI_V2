from copy import deepcopy

from engine.predictor import predict


def simulate(
    patient: dict,
    changes: dict,
    model_name: str = "Model B",
):
    """
    Simulate clinical changes and compare
    prediction before and after intervention.
    """

    original_patient = deepcopy(patient)

    simulated_patient = deepcopy(patient)

    simulated_patient.update(changes)

    original = predict(
        original_patient,
        model_name,
    )

    simulated = predict(
        simulated_patient,
        model_name,
    )

    return {

        "original": original,

        "simulated": simulated,

        "changes": changes,

    }