import os
import pyodbc
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# ★変更ポイント：環境変数 'DB_CONNECTION_STRING' があればそれを使う
# なければ、一旦これまでの文字列をデフォルトとして置く（移行用）
CONNECTION_STRING = os.environ.get('DB_CONNECTION_STRING', 
    "Driver={ODBC Driver 18 for SQL Server};Server=tcp:testdb01.database.windows.net,1433;Database=free-sql-db-8650869;Uid=dbadmin;Pwd=dbdb@1008;Encrypt=yes;TrustServerCertificate=yes;")

def get_db_connection():
    return pyodbc.connect(CONNECTION_STRING)

# 起動時にテーブルがなければ作成する
def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='restaurants' AND xtype='U')
        CREATE TABLE restaurants (
            id INT IDENTITY(1,1) PRIMARY KEY,
            name NVARCHAR(100) NOT NULL,
            address NVARCHAR(200)
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    ### ここから追加：テーブルがなければ作成 ###
    cursor.execute('''
        IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='restaurants' AND xtype='U')
        CREATE TABLE restaurants (id INT IDENTITY(1,1) PRIMARY KEY, name NVARCHAR(100), address NVARCHAR(200))
    ''')
    conn.commit()
    ### ここまで追加 ###

    cursor.execute("SELECT * FROM restaurants")
    rows = cursor.fetchall()
    conn.close()
    return render_template('index.html', restaurants=rows)

@app.route('/add', methods=['POST'])
def add_restaurant():
    name = request.form.get('name')
    address = request.form.get('address')
    if name:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO restaurants (name, address) VALUES (?, ?)", (name, address))
        conn.commit()
        conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    app.run()
