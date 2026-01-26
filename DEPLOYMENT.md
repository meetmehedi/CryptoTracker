# ☁️ Cloud Deployment Guide

To make your CryptoTracker live on the internet, I recommend using **Railway.app** because it supports MySQL very easily compared to Render.

## 1. Push Your Code to GitHub (Already Done)
I have already pushed your code to: `https://github.com/meetmehedi/CryptoTracker`

## 2. Set Up on Railway
1.  Go to [Railway.app](https://railway.app/) and log in with GitHub.
2.  Click **"New Project"** > **"Deploy from GitHub repo"**.
3.  Select your `CryptoTracker` repository.
4.  Click **"Add a Service"** within the project and select **"MySQL"**. This creates your database instantly.

## 3. Connect the App and Database
1.  Click on your **MySQL** service on Railway, go to the **Variables** tab, and copy the values for:
    - `MYSQLHOST`
    - `MYSQLUSER`
    - `MYSQLPASSWORD`
    - `MYSQLPORT` (usually 3306)
    - `MYSQLDATABASE`
2.  Click on your **Web Service** (the app), go to the **Variables** tab, and add these:
    - `MYSQL_HOST`: Copy value from `MYSQLHOST`
    - `MYSQL_USER`: Copy value from `MYSQLUSER`
    - `MYSQL_PASSWORD`: Copy value from `MYSQLPASSWORD`
    - `MYSQL_DB`: Copy value from `MYSQLDATABASE`
    - `KAGGLE_USERNAME`: `meetmehedi`
    - `KAGGLE_KEY`: `57c0b882a6919505edf4813665e9393f`

## 4. Deploy and Initialize
1.  Railway will automatically deploy your app.
2.  Once the status is "Success", go to the **View Logs** or **Terminal** tab for the web service.
3.  Run the initialization command (one-time):
    ```bash
    python seed_data.py
    ```


---
**Note:** Since the Kaggle dataset is 700MB+, the free tier of some hosting services may run out of disk space or RAM during seeder execution. If that happens, consider seeding only a subset of the data for your demo.
