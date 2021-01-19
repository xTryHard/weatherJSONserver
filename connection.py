import pyodbc

driver = '{ODBC Driver 17 for SQL Server}'
server = 'xxxxx'
database = 'xxxxx'
uid = 'xxxxx'
pwd = 'xxxxx'
encrypt = 'yes'
TSC = 'no' #Trust server certificate
connection_timeout = '30'

conn = pyodbc.connect(f'DRIVER={driver};SERVER={server};DATABASE={database};UID={uid};\
    PWD={pwd};ENCRYPT={encrypt};TSC={TSC};CONNECTION TIMEOUT={connection_timeout}')


cursor = conn.cursor()

