import ibm_db
hostname="55fbc997-9266-4331-afd3-888b05e734c0.bs2io90l08kqb1od8lcg.databases.appdomain.cloud
uid="dmc07791"
pwd="NoVyHxFru1R6e2Gj"
driver="{IBM DB2 ODBC DRIVER}"
db="bludb"
port="31929"
protocol="TCPIP"
cert="certificate.crt"
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
print("connectd to database")
except:
print("unable to connect",ibm_db.conn_errormsg())
