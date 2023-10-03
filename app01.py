import pyodbc
from sqlalchemy import create_engine
import urllib

params = urllib.parse.quote_plus 
(r'Driver={ODBC Driver 18 for SQL Server};Server=tcp:yourDBServerName.database.windows.net,1433;Database=dbname;Uid=username@dbserverName;Pwd=xxx;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;')
conn_str = 'mssql+pyodbc:///?odbc_connect={}'.format(params)
engine_azure = create_engine(conn_str,echo=True)

print('connection is ok')
print(engine_azure.table_names())