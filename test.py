

#connect to azure sql from python without using odbc connection to azure sql
#https://stackoverflow.com/questions/60336500/connect-to-azure-sql-from-python-without-using-odbc-connection-to-azure-sql
#   
#   import pyodbc
# import struct
# from azure.identity import DefaultAzureCredential
#
# server = 'your_server.database.windows.net'
# database = 'your_database'
# username = 'your_username'
# password = 'your_password'
#
# connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'
#
# credential = DefaultAzureCredential()
# token_bytes = credential.get_token("https://database.windows.net/").token.encode("UTF-16-LE")
# token_struct = struct.pack(f'<I{len(token_bytes)}s', len(token_bytes), token_bytes)
# # This connection option is defined by microsoft in msodbcsql.h

