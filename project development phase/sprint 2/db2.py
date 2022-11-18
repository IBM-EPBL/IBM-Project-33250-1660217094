import ibm_db

hostname="ba99a9e6-d59e-4883-8fc0-d6a8c9f7a08f.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud"
uid="zts87022"
pwd="LpYRSSF5tqnEgpLt"
driver="{IBM DB2 ODBC DRIVER}"
db="bludb"
port="31321"
protocol="TCPIP"
cert="certificate.crt.crt"

dsn=(
    "DRIVER = {0};"
    "DATABASE={1};"
    "HOSTNAME={2};"
    "PORT={3};"
    "UID={4};"
    "SECURITY=SSL;"
    "SSLServercertificate={5};"
    "PWD={6};"
).format(db,hostname,port,uid,cert,pwd,driver,protocol)
print(dsn)
try:
    db2=ibm_db.connect(dsn,"","")
    print("connected to database")
except:
    print("unable to connect",ibm_db.conn_errormsg())
