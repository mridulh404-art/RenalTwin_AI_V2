from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(r"G:\PROJECTS\RenalTwin_AI_V2")

files = [

    "data/raw/demographics/DEMO_J.XPT",
    "data/raw/examination/BMX_J.XPT",
    "data/raw/examination/BPX_J.XPT",
    "data/raw/laboratory/CBC_J.XPT",
    "data/raw/laboratory/BIOPRO_J.XPT",
    "data/raw/laboratory/ALB_CR_J.XPT",
    "data/raw/questionnaire/DIQ_J.XPT",
    "data/raw/questionnaire/SMQ_J.XPT",

]

print("=" * 80)
print("NHANES Variable Inspector")
print("=" * 80)

for file in files:

    path = PROJECT_ROOT / file

    print("\n" + "=" * 80)
    print(path.name)
    print("=" * 80)

    df = pd.read_sas(path)

    print(f"Rows: {len(df):,}")
    print(f"Columns: {len(df.columns)}")

    print("\nVariables:\n")

    for col in df.columns:
        print(col)