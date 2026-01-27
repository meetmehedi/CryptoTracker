import csv
import os
import MySQLdb

# Configuration
# Railway uses MYSQLHOST, MYSQLUSER, etc. while my app used MYSQL_HOST, MYSQL_USER
DB_CONFIG = {
    'host': os.environ.get('MYSQLHOST') or os.environ.get('MYSQL_HOST', 'localhost'),
    'user': os.environ.get('MYSQLUSER') or os.environ.get('MYSQL_USER', 'root'),
    'passwd': os.environ.get('MYSQLPASSWORD') or os.environ.get('MYSQL_PASSWORD', ''),
    'port': int(os.environ.get('MYSQLPORT') or os.environ.get('MYSQL_PORT', 3306))
}
DB_NAME = os.environ.get('MYSQLDATABASE') or os.environ.get('MYSQL_DB', 'cppt_db')
CSV_PATH_KAGGLE = '/kaggle/input/daily-crypto-tracker-dataset/daily_crypto_tracker.csv'
CSV_PATH_LOCAL = 'combined_data.csv'

def get_connection():
    conn = MySQLdb.connect(**DB_CONFIG)
    conn.autocommit(False)
    return conn

def run_schema(cursor):
    print("Running schema...")
    with open('schema.sql', 'r') as f:
        full_schema = f.read()
    
    # Split into main schema and trigger
    # Using the known comment marker as separator
    parts = full_schema.split('-- 8. Trigger')
    
    # Run Table Creatons
    main_schema = parts[0]
    statements = main_schema.split(';')
    for stmt in statements:
        if stmt.strip():
            cursor.execute(stmt)
            
    # Run Trigger if exists
    if len(parts) > 1:
        trigger_sql = parts[1].replace('DELIMITER $$', '').replace('DELIMITER ;', '').strip()
        # The tool removed DELIMITER lines already, but good to be safe.
        # We need to run the whole create statement as one
        # Assuming the file now ends with END; we might need to be careful with trailing chars
        print("Creating Trigger...")
        cursor.execute(trigger_sql)

def seed_data(cursor, conn):
    # check if user exists
    cursor.execute(f"USE {DB_NAME}")
    cursor.execute("SELECT * FROM Users WHERE email = 'mehedi@example.com'")
    if not cursor.fetchone():
        print("Creating dummy user...")
        # Add join_date (CURDATE() equivalent)
        cursor.execute("INSERT INTO Users (name, email, password, join_date) VALUES ('Mehedi Hasan', 'mehedi@example.com', 'hashedpassword', CURDATE())")
    
    # Try finding CSV
    csv_file = None
    if os.path.exists(CSV_PATH_KAGGLE):
        csv_file = CSV_PATH_KAGGLE
    elif os.path.exists(CSV_PATH_LOCAL):
        csv_file = CSV_PATH_LOCAL
    
    if csv_file:
        print(f"Found CSV at {csv_file}. Seeding coins...")
        with open(csv_file, 'r') as f:
            reader = csv.DictReader(f)
            seen_coins = set()
            
            cursor.execute("SELECT symbol FROM Coins")
            existing = {row[0] for row in cursor.fetchall()}
            
            print("Reading CSV...")
            count = 0 
            price_count = 0
            
            # Use 'utf-8-sig' to handle potential BOM
            # We need to re-open to handle encoding if needed, but let's assume standard
            # Parse combined_data.csv: open,low,volume,high,close,timestamp,ticker
            for row in reader:
                ticker = row.get('ticker')
                # Use ticker for name as well since `combined_data.csv` doesn't have a separate name
                name = ticker 
                
                # timestamp is unix epoch float/int
                ts_val = row.get('timestamp')
                close_price = row.get('close')
                
                if ticker:
                    # Insert Coin if new
                    if ticker not in existing and ticker not in seen_coins:
                        cursor.execute("INSERT INTO Coins (symbol, name, category) VALUES (%s, %s, %s)", (ticker, name, 'General'))
                        seen_coins.add(ticker)
                        existing.add(ticker) # Add to existing so we don't try again
                        count += 1
                    
                    # Insert Price if available
                    if close_price and ts_val:
                        # Fetch coin_id
                        cursor.execute("SELECT id FROM Coins WHERE symbol=%s", (ticker,))
                        coin_row = cursor.fetchone()
                        if coin_row:
                            coin_id = coin_row[0]
                            try:
                                price_val = float(close_price)
                                # timestamp to date
                                # We can use FROM_UNIXTIME in SQL or datetime in python. 
                                # Let's use FROM_UNIXTIME(%s) in SQL if it's seconds. 
                                # Looking at the csv head: 1701302400.0, this is seconds.
                                cursor.execute("INSERT INTO Prices (coin_id, price_date, price_usd) VALUES (%s, FROM_UNIXTIME(%s), %s)", (coin_id, ts_val, price_val))
                                price_count += 1
                            except ValueError:
                                pass # Skip bad price data

                if (count + price_count) % 1000 == 0:
                    conn.commit()
                    print(f"Processed {count} coins, {price_count} prices...")

            conn.commit() # Final commit
            print(f"Added {count} new coins and {price_count} price entries.")
    else:
        print("CSV file not found. Skipping coin seed.")

def main():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        run_schema(cursor)
        conn.commit()
        seed_data(cursor, conn)
        print("Database initialized successfully.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    main()
