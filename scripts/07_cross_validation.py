from pathlib import Path

import pandas as pd

from sklearn.model_selection import StratifiedKFold
from sklearn.model_selection import cross_validate

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier

# ==========================================================
# RenalTwin AI V2
# Cross Validation
# ==========================================================

PROJECT_ROOT = Path(r"G:\PROJECTS\RenalTwin_AI_V2")

print("=" * 80)
print("RenalTwin AI V2 - 5 Fold Cross Validation")
print("=" * 80)

df = pd.read_csv(
    PROJECT_ROOT / "data/processed/renal_twin_model.csv"
)

TARGET = "CKD"

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

]

X = df[FEATURES]

y = df[TARGET].astype(int)

cv = StratifiedKFold(

    n_splits=5,

    shuffle=True,

    random_state=42,

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

            class_weight="balanced",

            random_state=42,

            n_jobs=-1,

        ),

}

scoring = [

    "accuracy",

    "precision",

    "recall",

    "f1",

    "roc_auc",

]

results = []

for name, model in models.items():

    print()

    print("=" * 80)

    print(name)

    print("=" * 80)

    scores = cross_validate(

        model,

        X,

        y,

        cv=cv,

        scoring=scoring,

        n_jobs=-1,

    )

    row = {

        "Model": name,

    }

    for metric in scoring:

        mean = scores[f"test_{metric}"].mean()

        std = scores[f"test_{metric}"].std()

        row[f"{metric}_mean"] = mean

        row[f"{metric}_std"] = std

        print(

            f"{metric:<12}"

            f"{mean:.4f}"

            f" ± "

            f"{std:.4f}"

        )

    results.append(row)

results = pd.DataFrame(results)

output = PROJECT_ROOT / "outputs" / "metrics"

output.mkdir(parents=True, exist_ok=True)

results.to_csv(

    output / "cross_validation_results.csv",

    index=False,

)

print()

print("=" * 80)

print("Cross Validation Completed")

print("=" * 80)

print(results)