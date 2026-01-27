from flask_mysqldb import MySQL

mysql = MySQL()

import os

def init_db(app):
    # Railway uses MYSQLHOST, MYSQLUSER, etc.
    host = os.environ.get('MYSQLHOST') or os.environ.get('MYSQL_HOST')
    user = os.environ.get('MYSQLUSER') or os.environ.get('MYSQL_USER')
    password = os.environ.get('MYSQLPASSWORD') or os.environ.get('MYSQL_PASSWORD')
    db_name = os.environ.get('MYSQLDATABASE') or os.environ.get('MYSQL_DB')
    
    # If variables are missing, we likely have a configuration issue on Railway
    if not host or not user:
        print("⚠️ WARNING: MySQL environment variables are missing! Falling back to defaults.")
        host = host or 'localhost'
        user = user or 'root'
        db_name = db_name or 'cppt_db'
        password = password or ''
    
    print(f"Connecting to host: {host}, user: {user}, db: {db_name}")
    
    app.config['MYSQL_HOST'] = host
    app.config['MYSQL_USER'] = user
    app.config['MYSQL_PASSWORD'] = password
    app.config['MYSQL_DB'] = db_name
    app.config['MYSQL_PORT'] = int(os.environ.get('MYSQLPORT') or os.environ.get('MYSQL_PORT', 3306))
    
    mysql.init_app(app)
