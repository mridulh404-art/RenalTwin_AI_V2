from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(r"G:\PROJECTS\RenalTwin_AI_V2")

datasets = {

    "DEMO": "data/raw/demographics/DEMO_J.xpt",

    "BMX": "data/raw/examination/BMX_J.xpt",

    "BPX": "data/raw/examination/BPX_J.xpt",

    "CBC": "data/raw/laboratory/CBC_J.xpt",

    "BIOPRO": "data/raw/laboratory/BIOPRO_J.xpt",

    "ALB_CR": "data/raw/laboratory/ALB_CR_J.xpt",

    "DIQ": "data/raw/questionnaire/DIQ_J.xpt",

    "SMQ": "data/raw/questionnaire/SMQ_J.xpt",

}

output_folder = PROJECT_ROOT / "outputs" / "reports"
output_folder.mkdir(parents=True, exist_ok=True)

print("=" * 80)
print("NHANES DATASET VALIDATION")
print("=" * 80)

for name, relative_path in datasets.items():

    path = PROJECT_ROOT / relative_path

    print("\n" + "=" * 80)
    print(name)
    print("=" * 80)

    df = pd.read_sas(path)

    print(f"Rows    : {len(df):,}")
    print(f"Columns : {len(df.columns)}")

    pd.DataFrame({
        "Variable": df.columns
    }).to_csv(
        output_folder / f"{name}_variables.csv",
        index=False
    )

    print("✓ Variable list exported")

print("\nValidation Complete.")