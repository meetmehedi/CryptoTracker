# ☁️ Cloud Deployment Guide

To make your CryptoTracker live on the internet, follow these steps using **Render** (easiest for beginners).

## 1. Push Your Code to GitHub
Ensure you have run the following commands in your project folder:
```bash
git init
git add .
git commit -m "Deploy: Cloud configuration and metadata"
git branch -M main
git remote add origin <YOUR_GITHUB_REPO_URL>
git push -u origin main
```

## 2. Set Up a MySQL Database
Render and Railway provide "Managed Databases."
- **On Render**: Click "New" > "MySQL".
- Create the database and copy the **Internal Database URL** or specific credentials (Host, User, Password).

## 3. Create the Web Service on Render
- Click **New** > **Web Service**.
- Connect your GitHub repository.
- **Environment**: Python
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `gunicorn app:app`

## 4. Configure Environment Variables
Inside the Render dashboard for your service, click **Environment** and add:
- `MYSQL_HOST`: (From your Render MySQL)
- `MYSQL_USER`: (From your Render MySQL)
- `MYSQL_PASSWORD`: (From your Render MySQL)
- `MYSQL_DB`: `cppt_db`
- `KAGGLE_USERNAME`: `meetmehedi`
- `KAGGLE_KEY`: `57c0b882a6919505edf4813665e9393f`

## 5. Initialize the Cloud Database
Once the app is live, you need to run the schema once. You can do this by using the Render **Shell** tab:
```bash
python seed_data.py
```

---
**Note:** Since the Kaggle dataset is 700MB+, the free tier of some hosting services may run out of disk space or RAM during seeder execution. If that happens, consider seeding only a subset of the data for your demo.
