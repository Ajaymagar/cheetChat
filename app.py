from flask import Flask ,render_template
from flask_login import LoginManager , current_user , login_user , login_required , logout_user
from flask import request , redirect , url_for
from flask_socketio import SocketIO , send ,join_room
from dbs import get_user , save_user
from models import User
from pymongo.errors import DuplicateKeyError
app = Flask(__name__)
socketio = SocketIO(app)
app.secret_key = "keyissecret"
login_manager = LoginManager(app)
login_manager.login_view = 'login'

@app.route('/')
def home():
    return render_template('index.html')
 


@app.route('/login',methods=["POST" , "GET"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))    
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        
        user = get_user(username)
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            print("Failed")
    return render_template('index.html')


@app.route('/signup' , methods=['GET' , 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('login'))
    
    if request.method == "POST":
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        try:
            save_user(username ,email , password)
            return redirect(url_for('login'))
        except DuplicateKeyError:
            message = 'user already exits'
    return render_template('index.html' , message=message)



@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))







@login_manager.user_loader
def user_loader(username):
    return get_user(username)

              



if __name__ == "__main__":
    socketio.run(app,debug=True)


