import os
import uuid

from flask import Flask, render_template, request, redirect, session
import psycopg2.extras
app = Flask(__name__)
app.secret_key = 'your_secret_key_here'
database_session=psycopg2.connect(database="patient",user="postgres",password="mansi*2004",host="localhost",port="5432")

@app.route('/home_p')
def home():
    return render_template('home_patient.html')
@app.route('/home_d')
def homed():
    return render_template('home_doctor.html')
@app.route('/aboutus_p')
def aboutus():
    return render_template('aboutus_patient.html')
@app.route('/aboutus_d')
def aboutusd():
    return render_template('aboutus_doctor.html')

@app.route('/patient')
def patient():
    userdata = session.get('user')
    return render_template('profile_patient.html',userdata=userdata)
@app.route('/doctor')
def doctor():
    userdata = session.get('user')
    return render_template('profile_doctor.html', userdata=userdata)
@app.route('/',methods=['GET','POST'])
def login():  # put application's code here
    messages=None
    if request.method=='GET':
      return render_template('login.html')
    elif request.method=='POST':
        email=request.form.get('email')
        password=request.form.get('password')
        cur=database_session.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute('select * from patient where emailAddress=%s and password=%s',(email,password))
        userdata=cur.fetchone()
        if userdata:
            session['user'] = dict(userdata)
            return redirect('/patient')
        elif userdata is None:
            cur = database_session.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cur.execute('select * from doctor where emailAddress=%s and password=%s', (email, password))
            userdata = cur.fetchone()
            if userdata:
                session['user'] = dict(userdata)
                return redirect('/doctor')
            elif userdata is None:

               messages = 'invalid credentials'
               return render_template('login.html', message=messages)




@app.route('/signup',methods=['GET','POST'])
def signup():  # put application's code here
    message=None
    if request.method == 'GET':
       return render_template('signuptest2.html')
    if request.method == 'POST':
        fname = request.form.get('fname')
        lname = request.form.get('lname')
        email = request.form.get('email')
        phone = request.form.get('phone')
        password = request.form.get('password')
        confirm = request.form.get('cpassword')
        check1=request.form.get('check1')
        check2=request.form.get('check2')
        age = request.form.get('age')
        gender = request.form.get('gender')
        picture=request.files.get('photo')
        pic_name = str(uuid.uuid4()) + os.path.splitext(picture.filename)[1]
        picture.save(os.path.join("static/images/", pic_name))


        if gender!='male' and gender!='female' and gender!='Male' and gender!='Female':
            message='please choose male or female'
            return render_template('signuptest2.html', msg=message)
        if password != confirm:
            message='passwords do not match'
            return render_template('signuptest2.html', msg=message)
        else:
            if check1=='on' and check2=='on':
                message = 'both are checked please choose only one'
            elif check1=='on':
                cur = database_session.cursor(cursor_factory=psycopg2.extras.DictCursor)
                cur.execute('select * from patient where emailAddress=%s', (email,))
                if cur.fetchone():
                    message = 'user already exists'
                    return render_template('signuptest2.html', msg=message)
                cur.execute('select * from doctor where emailAddress=%s', (email,))

                if cur.fetchone():
                    message = 'you are already doctor'

                else:
                    cur.execute(
                        'INSERT INTO patient(fname,lname,phoneNumber,emailAddress,age,gender,password,confirmPassword,picture) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)',
                        (fname, lname, phone, email,age,gender, password, confirm,pic_name))
                    database_session.commit()
                    message = 'success'
            elif check2=='on':
                cur = database_session.cursor(cursor_factory=psycopg2.extras.DictCursor)
                cur.execute('select * from doctor where emailAddress=%s', (email,))
                if cur.fetchone():
                    message = 'user already exists'
                    return render_template('signuptest2.html', msg=message)
                cur.execute('select * from patient where emailAddress=%s', (email,))
                if cur.fetchone():
                    message = 'you are already patient'
                else:
                    cur.execute(
                        'INSERT INTO doctor(fname,lname,phoneNumber,emailAddress,age,gender,password,confirmPassword,picture) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)',
                        (fname, lname, phone, email, age,gender,password, confirm,pic_name))
                    database_session.commit()
                    message = 'success'


            return render_template('signuptest2.html', msg=message)

@app.route('/edit_p',methods=['GET','POST'])
def edit():
    if request.method=='GET':
        userdata = session.get('user')
        return render_template('edit_patient.html', userdata=userdata)
    elif request.method=='POST':
        fname = request.form.get('edit_fname')
        lname=request.form.get('edit_lname')
        phone=request.form.get('edit_phone')
        email=request.form.get('email_p')
        age=request.form.get('age_p')
        gender=request.form.get('edit_gender')
        id_p=request.form.get('id_p')
        print(id_p)
        cur = database_session.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute(
            'UPDATE patient SET fname= %s,lname= %s,phonenumber= %s,emailaddress= %s,age= %s,gender= %s WHERE id= %s',
            (fname,lname,phone,email,age,gender,id_p,))


        cur.execute('select * from patient where id=%s',(id_p,))
        userdata=cur.fetchone()
        session['user'] = dict(userdata)
        database_session.commit()
        return redirect('/patient')

@app.route('/edit_d',methods=['GET','POST'])
def edit_d():
    if request.method == 'GET':
        userdata = session.get('user')
        return render_template('edit_doctor.html', userdata=userdata)
    elif request.method == 'POST':
        fname = request.form.get('e_fname')
        lname = request.form.get('e_lname')
        phone = request.form.get('e_phone')
        email = request.form.get('e_email')
        age = request.form.get('e_age')
        gender = request.form.get('e_gender')
        id_d= request.form.get('id_d')
        print(id_d)
        cur = database_session.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute(
            'UPDATE doctor SET fname= %s,lname= %s,phonenumber= %s,emailaddress= %s,age= %s,gender= %s WHERE id= %s',
            (fname, lname, phone, email, age, gender, id_d,))

        cur.execute('select * from doctor where id=%s', (id_d,))
        userdata = cur.fetchone()
        session['user'] = dict(userdata)
        database_session.commit()
        return redirect('/doctor')


if __name__ == '__main__':
    app.run(debug=True)
