from flask import *
import bcrypt,sqlite3
from requests import *
from flask_login import *
import pybase64 as base64

SECRET_KEY = "f090df93d86e77d20f128ef3843a4bd65726b9d8d08981899d8d326a96a437bc" # ENV me daalde bhai
app = Flask(__name__)
loginManager = LoginManager()
loginManager.init_app(app)
User = ''

@app.route("/")
def index():
    print("Homepage will be shown here")
    # return render_template("index.html")


@app.route("/register", methods = ["GET","POST"])
def register():
    if request.method == "POST":
        username = request.form.get("user")
        password = request.form.get("passwd")
        password = bytes(password, "utf-8")
        hashed = bcrypt.hashpw(password, bcrypt.gensalt(14))
        with sqlite3.connect("instance/database.db") as con:
            DB = con.cursor()
            DB.execute('''CREATE TABLE IF NOT EXISTS users(
                            username TEXT PRIMARY KEY,
                            password TEXT NOT NULL
                        )
                        ''')
            DB.execute("INSERT INTO users (username,password) VALUES (?,?)", (username,hashed))
            con.commit()
            username = bytes(password,"utf-8")
            username = base64.b64encode(username)
            DB.execute(f'''CREATE TABLE {username}(
                            service TEXT NOT NULL,      
                            username TEXT NOT NULL,
                            password TEXT NOT NULL,
                        )
                       ''' )            # Should Service be primary key?? IDK
            con.commit()
        return redirect(url_for("login"))
    else:
        return render_template("register")
    

@app.route("/login", methods = ["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("user")
        password = request.form.get("passwd")
        password = bytes(password, "utf-8")
        # hashed = bcrypt.hashpw(password, bcrypt.gensalt(14)) 
        with sqlite3.connect("instance/database.db") as con:
            DB = con.cursor()
            DB.execute("SELECT IFNULL(SELECT password FROM users WHERE username = (?)),0",(username)) # Selecting 0 if user if not returns
            result = DB.fetchall()
            if result == "0":
                pass # User doesn't exist print
            else:
                global User
                User = username
                result = bytes(result,"utf-8")
                if bcrypt.checkpw(password, result):
                    pass # User exists and save cookie
                    return redirect(url_for("dashboard"))

@app.route("/dashboard", method = "GET")
@login_required
def dashboard():
    global User
    with sqlite3.connect("instance/database.db") as con:
        username = base64.b64encode(User)
        DB = con.cursor()
        DB.execute(f'''SELECT * FROM {username}''')
        result = DB.fetchall()
    
