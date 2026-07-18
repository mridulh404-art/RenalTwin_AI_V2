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
# Train Multiple Feature Sets
# ==========================================================

PROJECT_ROOT = Path(r"G:\PROJECTS\RenalTwin_AI_V2")

print("=" * 80)
print("RenalTwin AI V2 - Multi-Model Benchmark")
print("=" * 80)

# ----------------------------------------------------------
# Load Data
# ----------------------------------------------------------

df = pd.read_csv(
    PROJECT_ROOT / "data/processed/renal_twin_model.csv"
)

TARGET = "CKD"

y = df[TARGET].astype(int)

# ----------------------------------------------------------
# Feature Sets
# ----------------------------------------------------------

FEATURE_SETS = {

    "Model_A": [

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

    ],

    "Model_B": [

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

    ],

}

# ----------------------------------------------------------
# Output folders
# ----------------------------------------------------------

metrics_folder = PROJECT_ROOT / "outputs" / "metrics"
metrics_folder.mkdir(parents=True, exist_ok=True)

models_folder = PROJECT_ROOT / "trained_models"
models_folder.mkdir(parents=True, exist_ok=True)

# ----------------------------------------------------------
# Loop through feature sets
# ----------------------------------------------------------

for feature_name, FEATURES in FEATURE_SETS.items():

    print("\n" + "#" * 80)
    print(feature_name)
    print("#" * 80)

    X = df[FEATURES]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=42,
        stratify=y,
    )

    print(f"Training Samples : {len(X_train)}")
    print(f"Testing Samples  : {len(X_test)}")
    print(f"Features         : {len(FEATURES)}")

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

    # ------------------------------------------------------
    # Train every model
    # ------------------------------------------------------

    for model_name, model in models.items():

        print("\n" + "-" * 60)
        print(model_name)
        print("-" * 60)

        model.fit(X_train, y_train)

        predictions = model.predict(X_test)

        probabilities = model.predict_proba(X_test)[:, 1]

        accuracy = accuracy_score(
            y_test,
            predictions,
        )

        precision = precision_score(
            y_test,
            predictions,
        )

        recall = recall_score(
            y_test,
            predictions,
        )

        f1 = f1_score(
            y_test,
            predictions,
        )

        auc = roc_auc_score(
            y_test,
            probabilities,
        )

        print(f"Accuracy : {accuracy:.4f}")
        print(f"Precision: {precision:.4f}")
        print(f"Recall   : {recall:.4f}")
        print(f"F1 Score : {f1:.4f}")
        print(f"ROC-AUC  : {auc:.4f}")

        results.append({

            "Model": model_name,

            "Accuracy": accuracy,

            "Precision": precision,

            "Recall": recall,

            "F1": f1,

            "ROC_AUC": auc,

        })

        filename = (
            feature_name
            + "_"
            + model_name.lower().replace(" ", "_")
            + ".pkl"
        )

        joblib.dump(
            model,
            models_folder / filename,
        )

    # ------------------------------------------------------
    # Save comparison
    # ------------------------------------------------------

    results_df = pd.DataFrame(results)

    results_df = results_df.sort_values(
        "ROC_AUC",
        ascending=False,
    )

    results_df.to_csv(

        metrics_folder /

        f"{feature_name}_comparison.csv",

        index=False,

    )

    print("\n")
    print("=" * 80)
    print(feature_name)
    print("=" * 80)

    print(results_df)

    print("\nBest Model")

    print(results_df.iloc[0]["Model"])

    print(

        f"ROC-AUC : "

        f"{results_df.iloc[0]['ROC_AUC']:.4f}"

    )

print("\n")
print("=" * 80)
print("ALL BENCHMARKS COMPLETED")
print("=" * 80)