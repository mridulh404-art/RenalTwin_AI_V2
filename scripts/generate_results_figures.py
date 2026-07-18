from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt


# Project root
ROOT = Path(__file__).resolve().parent.parent

OUTPUT = ROOT / "docs" / "results"
OUTPUT.mkdir(parents=True, exist_ok=True)


# =====================================================
# Figure 6: Model Performance Comparison
# =====================================================

comparison = pd.read_csv(
    ROOT / "outputs" / "metrics" / "Final_Model_Comparison.csv"
)

plt.figure(figsize=(8, 5))

plt.bar(
    comparison["Model"],
    comparison["ROC_AUC"]
)

plt.ylabel("ROC-AUC")
plt.xlabel("Model")
plt.title("Model Performance Comparison")

plt.tight_layout()

plt.savefig(
    OUTPUT / "Figure6_Model_Performance.png",
    dpi=300
)

plt.close()


# =====================================================
# Figure 7: Feature Importance
# =====================================================

feature = pd.read_csv(
    ROOT / "outputs" / "figures" / "feature_importance.csv"
)

feature = feature.sort_values(
    "Importance",
    ascending=True
)

plt.figure(figsize=(8, 6))

plt.barh(
    feature["Feature"],
    feature["Importance"]
)

plt.xlabel("Importance")
plt.ylabel("Feature")
plt.title(
    "Feature Importance for CKD Prediction"
)

plt.tight_layout()

plt.savefig(
    OUTPUT / "Figure7_Feature_Importance.png",
    dpi=300
)

plt.close()


# =====================================================
# Figure 8: Digital Twin Simulation
# =====================================================

dt = pd.read_csv(
    ROOT / "outputs" / "metrics" / "digital_twin_results.csv"
)

plt.figure(figsize=(10, 5))

plt.bar(
    dt["Scenario"],
    dt["Simulated Risk"]
)

plt.xticks(
    rotation=45,
    ha="right"
)

plt.ylabel("CKD Risk Probability")
plt.title(
    "Digital Twin Intervention Simulation"
)

plt.tight_layout()

plt.savefig(
    OUTPUT / "Figure8_Digital_Twin_Impact.png",
    dpi=300
)

plt.close()


print("All figures generated successfully.")