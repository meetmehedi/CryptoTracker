# 📊 PROJECT REPORT: CryptoTracker
**Real-Time Portfolio Management System**

---

## Table of Contents

1. [Introduction](#1-introduction)
    - [1.1 Background](#11-background)
    - [1.2 Problem Statement](#12-problem-statement)
    - [1.3 Project Overview](#13-project-overview)
2. [Project Objectives](#2-project-objectives)
3. [Technical Architecture](#3-technical-architecture)
    - [Tech Stack](#tech-stack)
    - [System Diagram](#system-diagram)
4. [Database Design](#4-database-design)
    - [Entity-Relationship Diagram](#entity-relationship-diagram)
    - [Key Logic: Weighted Average Cost (WAC)](#key-logic-weighted-average-cost-wac)
5. [Key Features](#5-key-features)
    - [Liquid Glass UI](#liquid-glass-ui)
    - [Real-Time Market Sync](#real-time-market-sync)
    - [Portfolio Analytics](#portfolio-analytics)
    - [Smart Alert System](#smart-alert-system)
    - [Dual-Timezone Logging](#dual-timezone-logging)
6. [Setup & Deployment](#6-setup--deployment)
    - [Local Environment](#local-environment)
    - [Cloud Deployment](#cloud-deployment)
7. [Conclusion & Future Work](#7-conclusion--future-work)

---

## 1. Introduction

### 1.1 Background
The financial landscape has undergone a paradigm shift with the advent of cryptocurrency and blockchain technology. What began as a niche experiment with Bitcoin has evolved into a global asset class worth trillions of dollars. However, this decentralized nature brings unique challenges: unlike traditional equity markets, the crypto market operates 24/7, is highly volatile, and involves assets distributed across exchanges and wallets.

### 1.2 Problem Statement
For investors, manually tracking a diverse portfolio is increasingly difficult. Calculating the **Weighted Average Cost (WAC)** of holdings after multiple buy/sell transactions, monitoring real-time price fluctuations, and assessing overall profitability often requires complex spreadsheets that are prone to human error.

### 1.3 Project Overview
**CryptoTracker** is a specialized Database Management System (DBMS) designed to solve these challenges. It provides a robust, web-based platform for real-time portfolio tracking. By integrating a structured MySQL database with a responsive Flask-based web application, the system ensures data integrity through automated triggers while offering a premium "Glassmorphism" user interface. This project demonstrates the practical application of relational database concepts—such as ACID properties, triggers, and foreign key constraints—to a modern fintech use case.

## 2. Project Objectives
- **Portfolio Management**: Allow users to log transactions (buy/sell) and monitor their holdings in real-time.
- **Data Integrity**: Implement MySQL Triggers to automatically calculate weighted average costs and update inventory.
- **Visual Excellence**: Utilize modern "Glassmorphism" design principles for a premium user experience.
- **Scalability**: Handle massive datasets (700MB+) through efficient indexing and automated background synchronization.

## 3. Technical Architecture

### Tech Stack
- **Backend**: Python (Flask) for routing and API management.
- **Database**: MySQL for relational data storage and business logic (Triggers/Views).
- **Frontend**: Vanilla ES6 JavaScript, HTML5, and Tailwind CSS.
- **Data Pipeline**: Python-driven ETL pipeline using Kaggle and CoinGecko APIs.

### System Diagram
```mermaid
graph LR
    User((User)) --> WebUI[Glassmorphism UI]
    WebUI --> FlaskServer[Flask Backend]
    FlaskServer --> MySQL[(MySQL DB)]
    KaggleScript[Kaggle ETL Script] --> MySQL
    LiveAPI[CoinGecko API] --> FlaskServer
```

## 4. Database Design

### Entity-Relationship Diagram
```mermaid
erDiagram
    Users ||--o{ Transactions : "performs"
    Users ||--o{ Holdings : "owns"
    Users ||--o{ Watchlist : "monitors"
    Users ||--o{ Alerts : "sets"
    
    Coins ||--o{ Transactions : "involved_in"
    Coins ||--o{ Holdings : "part_of"
    Coins ||--o{ Prices : "has_history"
    Coins ||--o{ Watchlist : "added_to"
    Coins ||--o{ Alerts : "monitored"

    Users {
        int id PK
        string name
        string email
        string password
        date join_date
    }
    Coins {
        int id PK
        string symbol
        string name
        string category
    }
    Transactions {
        int id PK
        int user_id FK
        int coin_id FK
        enum type
        double quantity
        double price_at_time
        datetime txn_date
    }
    Holdings {
        int user_id PK, FK
        int coin_id PK, FK
        double total_quantity
        double avg_buy_price
    }
    Prices {
        int id PK
        int coin_id FK
        date price_date
        double price_usd
    }
    Watchlist {
        int id PK
        int user_id FK
        int coin_id FK
    }
    Alerts {
        int id PK
        int user_id FK
        int coin_id FK
        enum condition
        decimal target_value
        enum status
    }
```

### Key Logic: Weighted Average Cost (WAC)
The system ensures that the `Holdings` table is always accurate without manual interference. This is achieved via a **MySQL Trigger**:
      - **WAC Calculation**: System automatically determines the weighted average cost for portfolio tracking.
- When a **Buy** transaction is inserted:
  - New Quantity = `Old Quantity + New Quantity`
  - New WAC = `((Old WAC * Old Quantity) + (New Price * New Quantity)) / New Quantity`
- When a **Sell** transaction is inserted:
  - New Quantity = `Old Quantity - Sold Quantity`

## 5. Key Features

### 💎 Liquid Glass UI
The interface features a minimalist, semi-transparent design with animated background "blobs." This ensures that data presentation is clear while maintaining a futuristic aesthetic.

### ⏱️ Real-Time Market Sync
Major assets (BTC, ETH, SOL) are synced directly with CoinGecko. For smaller tokens, the system uses the 700MB+ Kaggle dataset to provide historical context and dynamic simulations.

### 📈 Portfolio Analytics
The "Dashboard" provides instant insights into:
- **Total Portfolio Value**
- **Average Buy Price** for each asset
- **Real-time Profit/Loss (P&L)** calculations with visual indicators.

### 🔔 Smart Alert System
Users can set custom price thresholds (ABOVE or BELOW) for any asset. The system dynamically monitors these conditions and highlights triggered alerts with a high-visibility "Liquid Red" glow on the dashboard.

### 🌍 Dual-Timezone Logging
To cater to global analysis, the system displays transaction timestamps in both **Bangladesh Standard Time (BDT)** and **US Eastern Time (EST/EDT)**. This ensures that users can correlate market movements across different time zones instantly.

## 6. Setup & Deployment

### Local Environment
1. Install dependencies: `pip install -r requirements.txt`
2. Initialize Database: `python seed_data.py`
3. Run App: `python app.py`

### Cloud Deployment
The project is optimized for deployment on **Railway.app**, leveraging integrated MySQL services and environment variable configuration for secure database connections.

## 7. Conclusion & Future Work
CryptoTracker successfully demonstrates the application of advanced DBMS concepts in a modern fintech context. Future versions will include:
- Advanced charting (Candlestick charts).
- Multi-currency support (EUR, BDT, etc.).
- Automated notifications (Email/SMS Integration).

---
**Report Generated on:** January 30, 2026
**Created by:** `meetmehedi/CryptoTracker`
