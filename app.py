import os
import pyodbc
from flask import Flask

app = Flask(__name__)

# DB接続文字列（直書き）
#CONNECTION_STRING = "Driver={ODBC Driver 18 for SQL Server};Server=tcp:testdb01.database.windows.net,1433;Database=free-sql-db-8650869;Uid=dbadmin;Pwd={dbdb@1008};Encrypt=yes;TrustServerCertificate=yes;"
# Serverの後の「,1433」をあえて消し、TrustServerCertificateをyesにする
CONNECTION_STRING = "Driver={ODBC Driver 18 for SQL Server};Server=tcp:testdb01.database.windows.net;Database=free-sql-db-8650869;Uid=dbadmin;Pwd={dbdb@1008};Encrypt=yes;TrustServerCertificate=yes;Connection Timeout=60;"
@app.route('/')
def index():
    try:
        # DB接続テスト
        conn = pyodbc.connect(CONNECTION_STRING)
        cursor = conn.cursor()
        cursor.execute("SELECT 'Connection Success!'")
        row = cursor.fetchone()
        return f"<h1>{row[0]}</h1><p>Minimal app is talking to Azure SQL.</p>"
    except Exception as e:
        return f"<h1>Connection Failed</h1><p>Error: {str(e)}</p>"

if __name__ == '__main__':
    app.run()
