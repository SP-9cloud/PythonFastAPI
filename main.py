from flask import Flask,redirect,url_for,request,render_template,make_response,session,abort,flash
from werkzeug.utils import secure_filename
from flask_mail import Mail, Message
from forms import ContactForm
import sqlite3
from flask_sqlalchemy import SQLAlchemy
import uvicorn

#constructor
app = Flask(__name__)

#set secret key for session objects
app.secret_key="any random string"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///D:/python/hello-flask/database.db'
app.config['SECRET_KEY']='random string'
#practice basic routing and params

'''
@app.route("/")
def hello_world():
    return "Hello World!"

@app.route("/admin")
def hello_admin():
    return "Hello Admin!"

@app.route("/hello/<param>")
def hello_name(param):
    return "Hello Flask User %s !" % param

@app.route("/print/<number>")
def hello_number(number):
    return "Hello User %d !" % int(number)

@app.route("/user/<name>")
def hello_user(name):
    if name=='admin':
        return redirect(url_for('hello_admin'))
    else:
         return redirect(url_for('hello_name',param=name))
'''

#practice route methods
'''
@app.route("/welcome/<name>")
def welcome(name):
    return "Welcome %s !" % name

@app.route('/login',methods=['POST','GET'])
def login():
    if request.method=='POST':
        user=request.form['user_name']
    else:
        user=request.args.get('user_name')
    return redirect(url_for('welcome',name=user))
'''

#practice framework templates
'''
@app.route('/')
def index():
    str="""
<html>
<body>
<h1>Hello World</h1>
</body>
</html>
"""
    return str

# render using html file
def index():
    return render_template('hello.html')
'''

#practice static files
'''
@app.route('/')
def index():
    return render_template('index.html')
'''

#practice request object
'''
@app.route('/')
def student():
   return render_template('student.html')

@app.route('/result',methods=['POST','GET'])
def result():
    if request.method=='POST':
        result=request.form
        result1=request.cookies
        return render_template('table.html',result=result)
'''

#practice cookies
'''
@app.route('/')
def index():
    return render_template('setcookie.html')

@app.route('/setcookie',methods=['POST','GET'])
def setcookie():
    user=request.form['user_name']
    resp=make_response(render_template('readcookie.html'))
    resp.set_cookie('userId',user)
    return resp

@app.route('/getcookie')
def getcookie():
    name=request.cookies.get('userId')
    return "<h1>Welcome " + name + " !</h1>"
'''

#practice session objects
'''
@app.route('/')
def index():
    if 'username' in session:
        username=session['username']
        return "You are logged in as <b>" + username + '</b> <br><a href="http://127.0.0.1:5000/logout">Click here to logout</a>'
    else:
        return "You are not logged in <br><a href='http://127.0.0.1:5000/login'>Click here to login</a>"

@app.route('/login',methods=['POST','GET'])
def login():
    if request.method=='POST':
        session['username']=request.form['username']
        return redirect(url_for('index'))
    return render_template('session.html')

@app.route('/logout')
def logout():
    session.pop('username',None)
    return redirect(url_for('index'))
'''

#practice redircet with error code
'''
@app.route('/')
def index():
    return render_template('login.html')
    
@app.route('/login',methods=['POST','GET'])
def login():
    if request.method=='POST':
        if request.form['username']=='admin':
            return redirect(url_for('success'))
        else:
            abort(401)
    else:
        return redirect(url_for('index'))

@app.route('/success')
def success():
    return "Logged in successfully"
'''

#practice flash message
'''
@app.route('/')
def index():
    return render_template('flash.html')
    
@app.route('/login',methods=['POST','GET'])
def login():
    error=None
    if request.method=='POST':
        if request.form['username']!='admin' or \
            request.form['password']!='admin':
            error= 'Invalid username or password. Please try again !'
        else:
            flash('You are successfully logged in')
            flash('Logout out before login again')
            return redirect(url_for('index'))
        
    return render_template('log_in.html',error=error)
'''

#practice file upload
'''
@app.route('/')
def index():
    return render_template('upload.html')
    
@app.route('/uploader',methods=['POST'])
def uploadfile():
    f= request.files['file']
    f.save(secure_filename(f.filename))
    flash('You are successfully uploaded.')
    return redirect(url_for('index'))
'''

#practice mail
'''
mail=Mail(app)
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT']=465
app.config['MAIL_USERNAE']='xyz@gmail.com'
app.config['MAIL_PASSWORD']='123456'
app.config['MAIL_TLS']=False
app.config['MAIL_SSL']=True

@app.route('/')
def index():
    msg=Message('Hello',sender='xyz@gmail.com',recipients=['abc@gmail.com'])
    msg.body="Hello Flask! This message is sent from Flask-Mail"
    mail.send(msg)
    return "Message sent"
'''

#practice form & inputs
'''   
@app.route('/contact',methods=['POST','GET'])
def contact():
    form= ContactForm()
    if request.method=='POST':
        if form.validate()==False:
            flash("All fields are required.")
        else:
            flash("Form posted successfully.")
        return render_template("contact.html",form=form)
    
    if request.method=='GET':
        return render_template("contact.html",form=form)
'''
#practice sqlite
'''
@app.route('/')
def index():
    conn=sqlite3.connect('database.db')
    print('Opened database successfully')
    conn.execute('CREATE TABLE STUDENTS (name TEXT,addr TEXT ,city TEXT,pin TEXT)')
    print('Table created successfully')
    conn.close()

@app.route('/addrecord',methods=['POST','GET'])
def addrecord():
    if request.method=='POST':
        conn=sqlite3.connect('database.db')
        cur=conn.cursor()
        try:
            cur.execute("INSERT INTO STUDENTS (name,addr,city,pin) values (?,?,?,?)",(request.form['name'],request.form['address'],request.form['city'],request.form['pin']))
            conn.commit()
        except:
            conn.rollback()
            flash("Error in insert operation.")
            return render_template("addrecord.html")
        finally:
            conn.close()
            flash("Record added successfully.")
            return redirect(url_for('list'))
    else:
        return render_template("addrecord.html")

@app.route('/deleterecord/<pin>')
def deleterecord(pin):
    conn=sqlite3.connect('database.db')
    cur=conn.cursor()
    cur.execute("DELETE FROM STUDENTS where pin= '" + pin+"'")
    conn.commit()
    conn.close()
    flash("Record deleted successfully.")
    return redirect(url_for('list'))

@app.route('/updaterecord/<pin>')
def updaterecord(pin):
    conn=sqlite3.connect('database.db')
    cur=conn.cursor()
    newpin=pin+"updated"
    cur.execute("UPDATE STUDENTS set pin=' "+newpin+" ' where pin= '" + pin+"'")
    conn.commit()
    conn.close()
    flash("Record updated successfully.")
    return redirect(url_for('list'))

@app.route('/list')
def list():
    conn=sqlite3.connect('database.db')
    conn.row_factory=sqlite3.Row
    cur=conn.cursor()
    cur.execute("select * from students")
    rows=cur.fetchall()
    return render_template('list.html',rows=rows)
'''

#practice sqlalchemy
'''
db=SQLAlchemy(app)
class Studentsnew(db.Model):
    __tablename__ = 'studentsnew'  # Explicitly mention table name
    id = db.Column('student_id', db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    addr = db.Column(db.String(200))
    city = db.Column(db.String(50))
    pin = db.Column(db.String(10))

    def __init__(self, name, addr, city, pin):
        self.name = name
        self.addr = addr
        self.city = city
        self.pin = pin

@app.route('/showall')
def show_all():
    return render_template('show_all.html',students=Studentsnew.query.all())


@app.route('/addmodelrecord',methods=['POST','GET'])
def addmodelrecord():
    if request.method=='POST':
        conn=sqlite3.connect('database.db')
        cur=conn.cursor()
        try:
            if not request.form['name'] or not request.form['addr'] or not request.form['city'] or not request.form['pin']:
                flash("Please enter all fields.")
            else:
                student=Studentsnew(request.form['name'],request.form['addr'],request.form['city'],request.form['pin'])
                db.session.add(student)
                db.session.commit()
        except:
            conn.rollback()
            flash("Error in insert operation.")
            return render_template("addmodelrecord.html")
        finally:
            conn.close()
            flash("Record added successfully.")
            return redirect(url_for('show_all'))
    else:
        return render_template("addmodelrecord.html")
'''


if __name__=='__main__': #it signfies this is the main file we are running not imported otherwise name==app
    app.run(debug=True)