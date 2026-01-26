# CryptoTracker: Real-Time Portfolio Management

A full-stack Cryptocurrency Portfolio Tracker featuring a futuristic **Liquid Glass UI**, automated Kaggle data integration, and real-time market price synchronization.

## 🚀 Key Features
- **Liquid Glass UI**: Minimalist glassmorphism design with animated background blobs.
- **Real-Time Prices**: Integrated with **CoinGecko API** for major assets and dynamic simulation for niche tokens.
- **Advanced DBMS Architecture**:
  - **MySQL Triggers**: Automatic calculation of **Weighted Average Cost (WAC)** and holdings on every transaction.
  - **Referential Integrity**: Robust schema design with foreign key constraints.
- **Kaggle Automation**: Background script (`update_data.py`) that syncs the 700MB+ "Daily Global Crypto Market Tracker" dataset every 12 hours.
- **Portfolio Analytics**: Instant visibility into **Total Value** and **Cumulative Profit/Loss (P&L)**.
- **Localization**: Full support for **Bangladesh Standard Time (BDT)** in transaction history.

## 🛠️ Technical Stack
- **Backend**: Python (Flask)
- **Database**: MySQL
- **Frontend**: JavaScript (Vanilla ES6), Tailwind CSS
- **Data Source**: Kaggle API & CoinGecko API

## 📦 Local Setup
1. **Clone the repository**:
   ```bash
   git clone <your-repo-url>
   cd cppt
   ```
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Database Configuration**:
   - Create a MySQL database named `cppt_db`.
   - Update `DB_CONFIG` in `db.py` with your credentials.
   - Run the initialization script:
     ```bash
     python seed_data.py
     ```
4. **Run the Application**:
   ```bash
   python app.py
   ```
   Access at `http://127.0.0.1:5001`.

5. **(Optional) Enable Kaggle Auto-Sync**:
   - Place your `kaggle.json` in `~/.kaggle/`.
   - Run the background scheduler:
     ```bash
     python update_data.py
     ```

## 📜 Academic Context
This project was developed as part of a **Database Management Systems (DBMS)** course, focusing on relational modeling, data integrity, and automated ETL processes.

---
*Created by [Your Name]*
