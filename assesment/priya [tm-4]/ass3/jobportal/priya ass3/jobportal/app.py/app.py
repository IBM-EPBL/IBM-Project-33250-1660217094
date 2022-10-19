from collections import UserDict
from flask import Flask,render_template,request,redirect,url_for,session
import ibm_db
import re

app = Flask(__name__)

app.secret_key ='a'

conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=55fbc997-9266-4331-afd3-888b05e734c0.bs2io90l08kqb1od8lcg.databases.appdomain.cloud;PORT=31929;SECURITY=SSL;SSLServerCertificate=certificate.crt.crt;UID=dmc07791;PWD=NoVyHxFru1R6e2Gj",'','')


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login',methods =['GET','POST'])
def login():
    global userid 
    msg =''
    
    if request.method == 'POST':
        username =request.form['username']
        password =request.form['password']
        sql ="SELECT *FROM users WHERE username =? AND password=?"
        stmt = ibm_db.prepare(conn,sql)
        ibm_db.blind_param(stmt,1,username)
        ibm_db.blind_param(stmt,2,password)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)
        print(account)
        if account:
            session['loggedin']=True
            session['id'] =account['USERNAME']
            userid =account['USERNAME']
            session['username'] = account['USERNAME']
            msg ='logged in sucessfully !'
           
            return render_template('dashboard.html', msg = msg)
       
        else: 
            msg ='Incorrect username /password !'
        return render_template('login.html', msg = msg)
    
@app.route('/register',methods =['GET','POST'])
def register():
    msg =''
    if request.method == 'POST':
        username =request.form['username']
        email =request.form['email']
        password =request.form['password']
        sql ="SELECT * FROM users WHERE username = ?"
        stmt = ibm_db.prepare(conn.sql)
        ibm_db.blind_param(stmt,1,username)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)
        print(account)
        if account:
            msg ='Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+',email):
            msg ='Invalid email address !'
        elif not re.match(r'[A-Za-Z0-9]+',username):
            msg ='Name must contain only characters and numbers !'
        else:
            insert_sql ="INSERT INTO users VALUES (?,?,?)"
            prep_stmt =ibm_db.prepare(conn,insert_sql)
            ibm_db.blind_param(prep_stmt,1,username)
            ibm_db.blind_param(prep_stmt,2,email)
            ibm_db.blind_param(prep_stmt,3,password)
            ibm_db.execute(prep_stmt)
            msg = 'You have sucessfully registered !'
    elif request.method == 'POST':
        msg ='please fill out the form !'
    return render_template('apply.html',msg =msg)

@app.route('/dashboard')
def dash():
    
    return render_template('dashboard.html')

@app.route('/apply',methods =['GET','POST'])
def apply():
    msg =''
    if request.method =='POST':
        username =request.form['username']
        email=request.form['email']
        qualification=request.form['qualification']
        skills = request.form['skills']
        jobs =request.form['s']
        sql ="SELECT *FROM users WHERE username =?"
        insert_sql ="INSERT INTO job VALUES (?,?,?,?,?)"
        prep_stmt =ibm_db.prepare(conn,insert_sql)
        ibm_db.blind_param(prep_stmt,1,username)
        ibm_db.blind_param(prep_stmt,2,email)
        ibm_db.blind_param(prep_stmt,3,qualification)
        ibm_db.blind_param(prep_stmt,4,skills)
        ibm_db.blind_param(prep_stmt,5,jobs)
        ibm_db.execute(prep_stmt)
        msg ='You have sucessfully applied for job !'
        session['loggedin']=True
    elif request.method == 'POST':
        msg ='please fill out the form !'
    return render_template('apply.html',msg =msg)
@app.route('/display')
def display():
    
    print(session["username"],session['id'])
    cursor = mysql.connection,cursor()
    cursor.execute('SELECT * FROM jobs WHERE userid = %s',(session['id']))
    account = cursor.fetchname()
    
    print("accountdisplay",account)
    
    return render_template('display.html',account =account)

@app.route('/logout')
def logout():
     session.pop('loggedin',None)
     session.pop('id',None)
     session.pop('username',None)
     return render_template('home.html')
if __name__=='__main__':
    app.run(host='0.0.0.0')