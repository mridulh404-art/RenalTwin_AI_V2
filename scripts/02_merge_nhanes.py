from pathlib import Path
import pandas as pd

# ==========================================================
# RenalTwin AI Version 2
# Merge NHANES Datasets
# ==========================================================

PROJECT_ROOT = Path(r"G:\PROJECTS\RenalTwin_AI_V2")

print("=" * 80)
print("RenalTwin AI V2 - NHANES Dataset Merge")
print("=" * 80)


# ----------------------------------------------------------
# Load datasets
# ----------------------------------------------------------

demo = pd.read_sas(
    PROJECT_ROOT / "data/raw/demographics/DEMO_J.xpt"
)

bmx = pd.read_sas(
    PROJECT_ROOT / "data/raw/examination/BMX_J.xpt"
)

bpx = pd.read_sas(
    PROJECT_ROOT / "data/raw/examination/BPX_J.xpt"
)

cbc = pd.read_sas(
    PROJECT_ROOT / "data/raw/laboratory/CBC_J.xpt"
)

bio = pd.read_sas(
    PROJECT_ROOT / "data/raw/laboratory/BIOPRO_J.xpt"
)

alb = pd.read_sas(
    PROJECT_ROOT / "data/raw/laboratory/ALB_CR_J.xpt"
)

diq = pd.read_sas(
    PROJECT_ROOT / "data/raw/questionnaire/DIQ_J.xpt"
)

smq = pd.read_sas(
    PROJECT_ROOT / "data/raw/questionnaire/SMQ_J.xpt"
)

print("✓ All datasets loaded")


# ----------------------------------------------------------
# Select required variables
# ----------------------------------------------------------

demo = demo[
    [
        "SEQN",
        "RIDAGEYR",
        "RIAGENDR",
        "RIDRETH3",
    ]
]

bmx = bmx[
    [
        "SEQN",
        "BMXHT",
        "BMXWT",
        "BMXBMI",
        "BMXWAIST",
    ]
]

bpx = bpx[
    [
        "SEQN",
        "BPXSY1",
        "BPXSY2",
        "BPXSY3",
        "BPXSY4",
        "BPXDI1",
        "BPXDI2",
        "BPXDI3",
        "BPXDI4",
    ]
]

cbc = cbc[
    [
        "SEQN",
        "LBXPLTSI",
        "LBDNENO",
        "LBDLYMNO",
        "LBXHGB",
    ]
]

bio = bio[
    [
        "SEQN",
        "LBXSCR",
        "LBDSALSI",
    ]
]

alb = alb[
    [
        "SEQN",
        "URXUMA",
        "URXUCR",
        "URDACT",
    ]
]

diq = diq[
    [
        "SEQN",
        "DIQ010",
    ]
]

smq = smq[
    [
        "SEQN",
        "SMQ020",
    ]
]

print("✓ Required variables selected")


# ----------------------------------------------------------
# Merge
# ----------------------------------------------------------

master = demo

for dataset in [

    bmx,
    bpx,
    cbc,
    bio,
    alb,
    diq,
    smq,

]:

    master = master.merge(
        dataset,
        on="SEQN",
        how="left",
    )

print("✓ Merge completed")


# ----------------------------------------------------------
# Save
# ----------------------------------------------------------

output = PROJECT_ROOT / "data/processed"

output.mkdir(
    parents=True,
    exist_ok=True,
)

master.to_csv(

    output / "renal_twin_master.csv",

    index=False,

)

print()

print("=" * 80)
print("Master dataset created successfully.")
print("=" * 80)

print(master.shape)

print()

print(master.head())