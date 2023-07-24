from flask import Flask, render_template, request,redirect,session
from data import Articles
from models import MyMongo
from config import MONGODB_URL
from datetime import timedelta
from functools import wraps

app = Flask(__name__)
app.secret_key = 'eunah'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=5)
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_TYPE'] = 'filesystem'
mymongo = MyMongo(MONGODB_URL, 'os')

def is_logged(func):
    @wraps(func)
    def wrap(*args,**kwargs):
        if 'is_logged' in session:
            return func(*args,**kwargs)
        else:
            return redirect('/login')
    return wrap

def is_admin(f):
    @wraps(f)
    def wrap(*args,**kwargs):
        if session['username'] == "admin":
            return f(*args,**kwargs)
        else:
            return redirect('/')
    return wrap

@app.route('/', methods=['GET','POST'])
@is_logged
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        phone = request.form['phone']
        password = request.form['password']
        user = mymongo.find_user(email)
        if username == 'admin':
            return render_template('register.html', message ='Impossible')
                # print(type(password))      
        elif user:            
            return render_template('register.html', message ='X')
        else:
            result =  mymongo.user_insert(username,email,phone,password)
            return redirect('/login')  
    
    elif request.method == 'GET':
        return render_template('register.html')    
    
@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        result = mymongo.verify_password(email,password)
        user = mymongo.find_user(email)
        if result == "1":
            session['is_logged'] = True
            session['username'] = user['username']
            return render_template('index.html', message = user )
        elif result == "2":
            return render_template('login.html', message = 'Wrong' )
        else:
            return render_template('register.html', message = 'None')
    print(result)
    return result

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/edit')
def edit():
    edit = mymongo.edit()
    return redirect('/')

@app.route('/delete')
def delete():
    delete = mymongo.delete()
    return redirect('/')

@app.route('/admin', methods=['GET','POST'])
@is_logged
@is_admin
def admin():
    return render_template('admin.html')



@app.route('/list', methods=['GET','POST'])
@is_logged
def list():
    data = mymongo.find_data()
    # for i in data:
    #     print(i)
    return render_template('list.html', data=data)

@app.route('/create', methods=['GET','POST'])
@is_logged
def create():  
    if request.method == 'GET':
        return render_template('create.html')
    else:
        title = request.form['title']
        desc = request.form['desc']  
        author = request.form['author']
        # print(author) 
        # return 'a'    
        result = mymongo.insert_data(title,desc,author) 
        return redirect('/list')



if __name__ == '__main__':
    app.run(debug=True, port=9999)
    
