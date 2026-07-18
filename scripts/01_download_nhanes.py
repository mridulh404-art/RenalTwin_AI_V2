from pathlib import Path
import requests

# ==========================================================
# RenalTwin AI V2
# NHANES Downloader
# ==========================================================

BASE_URL = "https://wwwn.cdc.gov/Nchs/Nhanes/2017-2018"

PROJECT_ROOT = Path(r"G:\PROJECTS\RenalTwin_AI_V2")

FILES = {
    "demographics": [
        "DEMO_J.XPT",
    ],

    "examination": [
        "BMX_J.XPT",
        "BPX_J.XPT",
    ],

    "laboratory": [
        "CBC_J.XPT",
        "BIOPRO_J.XPT",
        "ALB_CR_J.XPT",
    ],

    "questionnaire": [
        "DIQ_J.XPT",
        "SMQ_J.XPT",
    ],
}


def download_file(url, destination):

    print(f"Downloading {destination.name}...")

    response = requests.get(url, timeout=60)

    if response.status_code == 200:

        destination.write_bytes(response.content)

        print("   ✓ Success")

    else:

        print(f"   ✗ Failed ({response.status_code})")


def main():

    print("=" * 60)
    print("Downloading NHANES 2017-2018 Dataset")
    print("=" * 60)

    for folder, files in FILES.items():

        save_folder = PROJECT_ROOT / "data" / "raw" / folder

        save_folder.mkdir(parents=True, exist_ok=True)

        for filename in files:

            url = f"{BASE_URL}/{filename}"

            destination = save_folder / filename

            if destination.exists():

                print(f"{filename} already exists.")

                continue

            download_file(url, destination)

    print("\nDownload process finished.")


if __name__ == "__main__":
    main()