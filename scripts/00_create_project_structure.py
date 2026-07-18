from pathlib import Path

PROJECT_ROOT = Path(r"G:\PROJECTS\RenalTwin_AI_V2")

folders = [
    "data/raw/demographics",
    "data/raw/examination",
    "data/raw/laboratory",
    "data/raw/questionnaire",

    "data/processed",
    "data/external",

    "models",
    "trained_models",

    "outputs",
    "outputs/figures",
    "outputs/reports",
    "outputs/metrics",

    "scripts",
    "notebooks",

    "config",
    "docs",
]

print("=" * 60)
print("Creating RenalTwin AI V2 Project Structure")
print("=" * 60)

for folder in folders:
    path = PROJECT_ROOT / folder
    path.mkdir(parents=True, exist_ok=True)
    print(f"✓ {path}")

print("\nProject structure created successfully.")