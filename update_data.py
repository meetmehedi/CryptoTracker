import os
import time
import subprocess
import schedule
from seed_data import main as seed_db

# Configuration
DATASET_ID = "urvishahir/daily-crypto-tracker-dataset" 
DOWNLOAD_PATH = "."

def download_data():
    print(f"Downloading data ({DATASET_ID}) from Kaggle...")
    try:
        cmd = ["kaggle", "datasets", "download", "-d", DATASET_ID, "-p", DOWNLOAD_PATH, "--unzip", "--force"]
        subprocess.run(cmd, check=True)
        # Rename if necessary to match seed_data.py expectations
        if os.path.exists("daily_crypto_tracker.csv"):
             # Optional: os.replace("daily_crypto_tracker.csv", "combined_data.csv")
             pass
        print("Download complete.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error downloading data: {e}")
        return False
    except FileNotFoundError:
        print("Error: 'kaggle' command not found. Please install kaggle CLI.")
        return False

def job():
    print("Starting scheduled update...")
    if download_data():
        print("Seeding database with new data...")
        try:
            seed_db()
            print("Update cycle complete.")
        except Exception as e:
            print(f"Error during seeding: {e}")

def main():
    if DATASET_ID == "INSERT_DATASET_SLUG_HERE":
        print("Please update DATASET_ID in update_data.py first.")
        return

    # Initial run
    job()
    
    # Schedule every 12 hours
    schedule.every(12).hours.do(job)
    
    print("Scheduler running. Waiting for next update...")
    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    main()
