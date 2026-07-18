from engine.decision_support import generate_decision_support

prediction = {
    "Probability": 0.78,
    "Risk": "High",
}

patient = {
    "eGFR": 55,
    "LBXSCR": 1.9,
    "Mean_SBP": 148,
    "Mean_DBP": 92,
    "Diabetes": 1,
    "Smoker": 1,
}

result = generate_decision_support(
    prediction,
    patient,
)

print(result)