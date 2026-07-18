from pathlib import Path
import joblib
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
)

from xgboost import XGBClassifier
from lightgbm import LGBMClassifier

# ==========================================================
# RenalTwin AI V2
# Model C
# Diagnostic Decision Support
# ==========================================================

PROJECT_ROOT = Path(r"G:\PROJECTS\RenalTwin_AI_V2")

print("=" * 80)
print("RenalTwin AI V2 - Model C")
print("=" * 80)

df = pd.read_csv(
    PROJECT_ROOT /
    "data/processed/renal_twin_model.csv"
)

FEATURES = [

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

]

TARGET = "CKD"

X = df[FEATURES]

y = df[TARGET].astype(int)

X_train, X_test, y_train, y_test = train_test_split(

    X,
    y,

    test_size=0.20,

    random_state=42,

    stratify=y,

)

models = {

    "Logistic Regression":

        Pipeline([

            ("scaler", StandardScaler()),

            ("model",

             LogisticRegression(

                 max_iter=1000,

                 class_weight="balanced",

                 random_state=42,

             ))

        ]),

    "Random Forest":

        RandomForestClassifier(

            n_estimators=300,

            random_state=42,

            class_weight="balanced",

            n_jobs=-1,

        ),

    "XGBoost":

        XGBClassifier(

            random_state=42,

            eval_metric="logloss",

        ),

    "LightGBM":

        LGBMClassifier(

            random_state=42,

        ),

}

results = []

model_folder = PROJECT_ROOT / "trained_models"

metrics_folder = PROJECT_ROOT / "outputs" / "metrics"

model_folder.mkdir(exist_ok=True)

metrics_folder.mkdir(parents=True, exist_ok=True)

for name, model in models.items():

    print()

    print("=" * 80)

    print(name)

    print("=" * 80)

    model.fit(
        X_train,
        y_train,
    )

    pred = model.predict(X_test)

    prob = model.predict_proba(X_test)[:,1]

    accuracy = accuracy_score(
        y_test,
        pred,
    )

    precision = precision_score(
        y_test,
        pred,
    )

    recall = recall_score(
        y_test,
        pred,
    )

    f1 = f1_score(
        y_test,
        pred,
    )

    auc = roc_auc_score(
        y_test,
        prob,
    )

    print(f"Accuracy : {accuracy:.4f}")
    print(f"Precision: {precision:.4f}")
    print(f"Recall   : {recall:.4f}")
    print(f"F1 Score : {f1:.4f}")
    print(f"ROC-AUC  : {auc:.4f}")

    results.append({

        "Model": name,

        "Accuracy": accuracy,

        "Precision": precision,

        "Recall": recall,

        "F1": f1,

        "ROC_AUC": auc,

    })

    filename = (
        "Model_C_"
        + name.lower().replace(" ","_")
        + ".pkl"
    )

    joblib.dump(
        model,
        model_folder / filename,
    )

results = pd.DataFrame(results)

results = results.sort_values(
    "ROC_AUC",
    ascending=False,
)

results.to_csv(

    metrics_folder /

    "Model_C_comparison.csv",

    index=False,

)

print()

print("=" * 80)

print("MODEL C RESULTS")

print("=" * 80)

print(results)

print()

print("Best Model")

print(results.iloc[0]["Model"])

print(

    "ROC-AUC:",

    round(

        results.iloc[0]["ROC_AUC"],

        4,

    )

)