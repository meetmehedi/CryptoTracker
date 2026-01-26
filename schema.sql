CREATE DATABASE IF NOT EXISTS cppt_db;
USE cppt_db;

-- Clean up
DROP TRIGGER IF EXISTS update_holdings_after_txn;
DROP VIEW IF EXISTS Holdings; 
-- Note: Dropping the view named Holdings just in case, but we will create a TABLE named Holdings.
-- The order of dropping matters due to FKs.
DROP TABLE IF EXISTS Watchlist;
DROP TABLE IF EXISTS Alerts;
DROP TABLE IF EXISTS Prices;
DROP TABLE IF EXISTS Holdings;
DROP TABLE IF EXISTS Transactions;
DROP TABLE IF EXISTS Coins;
DROP TABLE IF EXISTS Users;

-- 1. Users
CREATE TABLE Users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100) UNIQUE,
    password VARCHAR(255),
    join_date DATE
);

-- 2. Coins
CREATE TABLE Coins (
    id INT AUTO_INCREMENT PRIMARY KEY,
    symbol VARCHAR(50) UNIQUE,
    name VARCHAR(100),
    category VARCHAR(50)
);

-- 3. Prices
CREATE TABLE Prices (
    id INT AUTO_INCREMENT PRIMARY KEY,
    coin_id INT,
    price_date DATE,
    price_usd DECIMAL(24, 8),
    FOREIGN KEY (coin_id) REFERENCES Coins(id) ON DELETE CASCADE
);

-- 4. Transactions
CREATE TABLE Transactions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    coin_id INT,
    type ENUM('buy', 'sell'),
    quantity DECIMAL(24, 8),
    price_at_time DECIMAL(24, 8),
    txn_date DATETIME,
    FOREIGN KEY (user_id) REFERENCES Users(id) ON DELETE CASCADE,
    FOREIGN KEY (coin_id) REFERENCES Coins(id) ON DELETE CASCADE
);

-- 5. Holdings (Now a Table, not a View)
CREATE TABLE Holdings (
    user_id INT,
    coin_id INT,
    total_quantity DECIMAL(30, 8) DEFAULT 0,
    avg_buy_price DECIMAL(24, 8) DEFAULT 0,
    PRIMARY KEY (user_id, coin_id),
    FOREIGN KEY (user_id) REFERENCES Users(id) ON DELETE CASCADE,
    FOREIGN KEY (coin_id) REFERENCES Coins(id) ON DELETE CASCADE
);

-- 6. Watchlist
CREATE TABLE Watchlist (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    coin_id INT,
    FOREIGN KEY (user_id) REFERENCES Users(id) ON DELETE CASCADE,
    FOREIGN KEY (coin_id) REFERENCES Coins(id) ON DELETE CASCADE
);

-- 7. Alerts
CREATE TABLE Alerts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    coin_id INT,
    condition_type ENUM('ABOVE', 'BELOW'),
    target_value DECIMAL(12, 4),
    status ENUM('ACTIVE', 'TRIGGERED'),
    FOREIGN KEY (user_id) REFERENCES Users(id) ON DELETE CASCADE,
    FOREIGN KEY (coin_id) REFERENCES Coins(id) ON DELETE CASCADE
);

-- 8. Trigger
CREATE TRIGGER update_holdings_after_txn
AFTER INSERT ON Transactions
FOR EACH ROW
BEGIN
    IF NEW.type = 'buy' THEN
        INSERT INTO Holdings (user_id, coin_id, total_quantity, avg_buy_price)
        VALUES (NEW.user_id, NEW.coin_id, NEW.quantity, NEW.price_at_time)
        ON DUPLICATE KEY UPDATE 
            avg_buy_price = ((total_quantity * avg_buy_price) + (NEW.quantity * NEW.price_at_time)) / (total_quantity + NEW.quantity),
            total_quantity = total_quantity + NEW.quantity;
    ELSE
        UPDATE Holdings
        SET total_quantity = total_quantity - NEW.quantity
        WHERE user_id = NEW.user_id AND coin_id = NEW.coin_id;
    END IF;
END;
