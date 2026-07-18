# 🩺 RenalTwin AI V2

## AI-Powered Clinical Decision Support System for Chronic Kidney Disease

RenalTwin AI V2 is an Explainable Artificial Intelligence (XAI) platform for Chronic Kidney Disease (CKD) risk prediction using NHANES 2017–2020 data.

The system includes three machine learning models, SHAP explainability, Digital Twin simulation, PDF clinical reporting, and an interactive Streamlit dashboard.

---

# Features

## Model A
Early CKD Screening

Uses:

- Age
- Sex
- Race
- BMI
- Waist Circumference
- Blood Pressure
- CBC Biomarkers

No kidney biomarkers required.

---

## Model B
Clinical Screening

Adds:

- Serum Creatinine
- Serum Albumin

Provides higher predictive performance.

---

## Model C
Diagnostic Support

Adds:

- eGFR
- UACR

Designed for diagnostic confirmation.

---

# AI Algorithms

- Logistic Regression
- Random Forest
- XGBoost
- LightGBM

Best performing model:

Random Forest

---

# Explainable AI

- SHAP Feature Importance
- Individual Prediction Explanation
- Clinical Interpretation

---

# Digital Twin

Interactive simulation allows clinicians to evaluate how changes in clinical parameters affect predicted CKD risk.

Examples:

- Lower blood pressure
- Improve serum creatinine
- Compare before vs after risk

---

# Evaluation

- ROC Curve
- Precision-Recall Curve
- Calibration Curve
- Threshold Optimization
- 5-Fold Cross Validation

---

# Technologies

- Python
- Streamlit
- Scikit-Learn
- XGBoost
- LightGBM
- SHAP
- Plotly
- ReportLab

---

# Installation

```bash
pip install -r requirements.txt
```

Run

```bash
streamlit run app.py
```

---

# Dataset

NHANES 2017–2020

---

# Disclaimer

This application is intended for research and educational purposes only.

It is not a replacement for professional clinical judgment.