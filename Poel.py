import splash_screen
from customtkinter import *
from PIL import Image, ImageTk
from ttkthemes import ThemedStyle
from tkinter import messagebox
import subprocess
import os
from tkinter import filedialog
import BluBatch
import webbrowser

FontFamily = "Roboto"
  

def openDashboard():


  def createProject():
    project_name = projectName.get()
    database_name = databaseName.get()
    secret_key_name = secretKeyName.get()


    DIR = f"C:\\{project_name}"
    
    DIR_WEBSITE = f"{DIR}\\website"
    DIR_STATIC = f"{DIR_WEBSITE}\\static"
    DIR_TEMPLATES = f"{DIR_WEBSITE}\\templates"

    DIR_CSS = f"{DIR_STATIC}\\css"
    DIR_JS = f"{DIR_STATIC}\\js"
    DIR_MEDIA = f"{DIR_STATIC}\\media"

    os.mkdir(DIR)
    os.mkdir(DIR_WEBSITE)
    os.mkdir(DIR_STATIC)
    os.mkdir(DIR_TEMPLATES)
    os.mkdir(DIR_CSS)
    os.mkdir(DIR_JS)
    os.mkdir(DIR_MEDIA)

    
    def runProject():
      messagebox.showinfo("Poel", "Oops........disabled for now")
      # def yes():
      #   minapp = CTk()
      #   minapp.geometry("10x10")
      #   minapp.resizable(height=False, width=False)
      #   command = f"{DIR}\\main.py"
      #   command = f"python {command}"
      #   BluBatch.create_batch_files(command)
      #   webbrowser.open("http://127.0.0.1:80")
      #   minapp.mainloop()

      # askToRun = messagebox.askyesno(f"Run {project_name}", f"Do you want to proceed to running `{project_name}`. Alternatively, you can go to this address `http://127.0.0.1:80` in your browser.")

      # if askToRun is True:
      #   yes()

      # else:
      #   webbrowser.open("http://127.0.0.1:80")
      # subprocess.run(, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True)#

    def manageProject():
      pass

		# MAIN FILE

    mainFileContent = """
from website import initialize_app

app = initialize_app()

if __name__ == '__main__':
  app.run(debug="True", host="0.0.0.0", port=80)

    """

		# WEBSITE FILES

    initFileContent = f"""
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from os.path import *
import os
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "{database_name}.db"

def initialize_app():
  app = Flask(__name__)
  app.config['SECRET_KEY'] = '{secret_key_name}'
  app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{database_name}.db'

  db.init_app(app)

  from .views import views
  from .auth import auth

  app.register_blueprint(views, url_prefix='/')
  app.register_blueprint(auth, url_prefix='/')

  from .models import User

  create_db(app)

  login_manager = LoginManager()
  login_manager.login_view = 'auth.login'
  login_manager.init_app(app)

  @login_manager.user_loader
  def load_user(id):
      return User.query.get(int(id))

  @app.errorhandler(500)
  def internal_server_error(e):
      return render_template('broken-page.html'), 500

  return app

def create_db(the_app):
  db_path = os.path.join(os.path.dirname(__file__), DB_NAME)
  if not isfile(db_path):
      with the_app.app_context():
          db.create_all()
      print("Database created!")

    """


    viewsFileContent = """
# views.py

from flask import Blueprint, render_template, flash, request, redirect, url_for, current_app, send_from_directory, session, jsonify
import random
from flask_login import login_required, current_user
from sqlalchemy.sql import func  # Import the 'func' module
from .models import User
from . import db

import os
from werkzeug.utils import secure_filename

views = Blueprint('views', __name__)


@views.route('/')
def index():
  return render_template("base.html")

@views.route('/home')
def home():
  return render_template("home.html")
    """

    authFileContent = """
from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

@auth.route("/login", methods=['GET', 'POST']) 
def login():
  if request.method == 'POST':
      email = request.form.get('email')
      password = request.form.get('password')

      user = User.query.filter_by(email=email).first()
      if user:
          if check_password_hash(user.password, password):
              flash("Logged in successfully.", category='Success')
              login_user(user, remember=True) 
              return redirect(url_for('views.showAppsBoard'))
          else:
              flash("Incorrect password. Please try again.", category="Error occurred")
      else:
          flash("Email not found. Please register first.", category="Error occurred")
  return render_template('login.html')

@auth.route("/logout")
@login_required
def logout():
  logout_user()
  flash("Logged out successfully.", category='Success')
  return redirect(url_for('auth.login'))

@auth.route("/signup", methods=['GET', 'POST'])
def register():
  if request.method == 'POST':
      name = request.form.get('name')
      email = request.form.get('email')
      password1 = request.form.get('password')
      password2 = request.form.get('password2')

      user = User.query.filter_by(email=email).first()

      if user:
          flash("Email is already taken. Please use a different email.", category='Error occurred')
      elif len(email) < 4:
          flash('Invalid email: Email must be at least 4 characters long.', category='Error occurred')
      elif len(name) < 2:
          flash('Invalid name: Name must be at least 2 characters long.', category='Error occurred')
      elif password1 != password2:
          flash('Passwords do not match. Please re-enter your password.', category='Error occurred')
      elif len(password1) < 8:
          flash('Password is too short. It must be at least 8 characters long.', category='Error occurred')
      else:
          new_user = User(email=email, name=name, password=generate_password_hash(password1))
          db.session.add(new_user)
          db.session.commit()
          flash('Account created successfully.', category='Success')
          login_user(new_user, remember=True)  # Log in the newly created user
          return redirect(url_for('views.home'))

  return render_template("signup.html")

    """

    modelsFileContent = """
from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class User(db.Model, UserMixin):
  id = db.Column(db.Integer, primary_key=True)
  email = db.Column(db.String(200), unique=True)
  password = db.Column(db.String(200))
  name = db.Column(db.String(200))
    """

		# TEMPLATES

    basePage = """
<title>{% block title %} Poel {% endblock %}</title>


<link rel="stylesheet" type="text/css" href="{{ url_for('static', filename='css/style.css') }}">

{% with messages = get_flashed_messages(with_categories=true) %}
{% if messages %}
  {% for category, message in messages %}
    {% if category == 'Error occurred' %}
      <div id="modal" class="modal">
          <div class="modal-content">
              <span class="close" id="closeModalBtn">&times;</span>
              <h2>{{ category }}</h2>
              <p>{{ message }}</p>
          </div>
      </div>
    {% else %}
      <div id="modal" class="modal">
          <div class="modal-content">
              <span class="close" id="closeModalBtn">&times;</span>
              <h2>{{ category }}</h2>
              <p>{{ message }}</p>
          </div>
      </div>
    {% endif %}
  {% endfor %}
{% endif %}
{% endwith %}

<script type="text/javascript" src="{{ url_for('static', filename='js/index.js') }}"></script>

{% block content %}

<!-- Start Landing Page -->
<div class="landing-page">
  <header>
    <div class="container">
      <a href="#" class="logo">Poel</a>
      <ul class="links">
        <a href="/"><li>Home</li></a>
        <a href="http://bluvid.000webhostapp.com/apps-page.html"><li>About Us</li></a>
        <a href="/signup"><li>Get Started</li></a>
      </ul>
    </div>
  </header>
  <div class="content">
    <div class="container">
      <div class="info">
        <h1>Share your work.</h1>
        <p>
          Poel, your Flask project manager.
    </p>
        <a href="/login"><button>Login</button></a>
      </div>
    </div>
  </div>
</div>
{% endblock %}
		"""
    loginPage = f"""
{{% extends 'base.html' %}}

{{% block title %}} Login Page - Poel {{% endblock %}}
{{% block content %}}
<style type="text/css">
  /*Start Global Style*/
  *{{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
  }}
  body{{
      background:#e9ebee;
      display: flex;
      justify-content: center;
      align-items: center;
      height:100vh;
      font-family: sans-serif;
  }}
  .container{{
      width: 80%;
      margin: auto;
      padding: 20px;
    height:100%
  }}

  .login ,.register{{width: 50%}}

  /*Start Login Style*/
  .login{{
      float:left;
      background-color: #fafafa;
      height: 100%;
      border-radius: 10px 0 0 10px;
      text-align: center;
      padding-top: 100px;
  }}
  .login h1{{
      margin-bottom: 40px;
      font-size: 2.5em;
  }}

  input[type="email"] , input[type="password"]{{
      width: 100%;
      padding: 10px;
      margin-bottom: 30px;
      border: none;
      background-color: #eeeeef;
  }}
  input[type="checkbox"]{{
      float: left;
      margin-right: 5px;
  }}
  .login span{{
      float: left
  }}
  .login a{{
      float: right;
      text-decoration: none;
      color: #000;
      transition: 0.3s all ease-in-out;
  }}
  .login a:hover{{color: #11d9c7ad;font-weight: bold}}
  .login button{{
      width: 100%;
      margin: 30px 0;
      padding: 10px;
      border: none;
      background-color: #11d9c7ad;
      color: #fff;
      font-size: 20px;
      cursor: pointer;
      transition: 0.3s all ease-in-out;
  }}
  .login button:hover{{
      width:97%;
      font-size: 22px;
      border-radius: 5px;
      
  }}
  .login hr{{
      width: 30%;
      display: inline-block
  }}

  .login p{{
      display: inline-block;
      margin: 0px 10px 30px;
  }}
  .login ul{{
      list-style: none;
      margin-bottom:40px;  
  }}
  .login ul li{{
      display: inline-block;
      margin-right: 30px;
      cursor: pointer;
  }}
  .login ul li:hover{{opacity: 0.6}}
  .login ul li:last-child{{margin-right: 0}}
  .login .copyright{{
      display: inline-block;
      float: none;
  }}
  @media screen and (max-width: 600px) {{
      /* CSS rules for screens 600px or narrower */
      .login{{
        width: 100%;
      }}
      /* Add more styles specific to smaller screens as needed */
  }}
</style>
<div class="container">
      <div class="login">
         <div class="container">
              <h1>Log in</h1>
              <form class="log-form" action="/login" method="POST">
                <input type="email" name="email" placeholder="Email">
                <input type="password" name="password" placeholder="Password"><br>
                <input type="checkbox"><span>Remember me</span>
                <button type="submit">Log In</button>
              </form> 
         </div>
      </div>
    </div>


{{% endblock %}}
		"""
    signupPage = f"""
{{% extends 'base.html' %}}
{{% block title %}} SignUp Page - Poel {{% endblock %}}
{{% block content %}}
<style type="text/css">
  /*Start Global Style*/
  *{{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
  }}
  body{{
      background:#e9ebee;
      display: flex;
      justify-content: center;
      align-items: center;
      height:100vh;
      font-family: sans-serif;
  }}
  .container{{
      width: 80%;
      margin: auto;
      padding: 20px;
    height:100%
  }}

  .login ,.register{{width: 50%}}

  /*Start Login Style*/
  .login{{
      float:left;
      background-color: #fafafa;
      height: 100%;
      border-radius: 10px 0 0 10px;
      overflow-x: hidden;
      overflow-y: auto;
      text-align: center;
      padding-top: 100px;
  }}
  .login h1{{
      margin-bottom: 40px;
      font-size: 2.5em;
  }}

  input[type="email"] , input[type="password"], input[type="number"], input[type="text"]{{
      width: 100%;
      padding: 10px;
      margin-bottom: 30px;
      border: none;
      background-color: #eeeeef;
  }}
  input[type="checkbox"]{{
      float: left;
      margin-right: 5px;
  }}
  .login span{{
      float: left
  }}
  .login a{{
      float: right;
      text-decoration: none;
      color: #000;
      transition: 0.3s all ease-in-out;
  }}
  .login a:hover{{color: #11d9c7ad;font-weight: bold}}
  .login button{{
      width: 100%;
      margin: 30px 0;
      padding: 10px;
      border: none;
      background-color: #11d9c7ad;
      border-radius: 20pc;
      color: #fff;
      font-size: 20px;
      cursor: pointer;
      transition: 0.3s all ease-in-out;
  }}
  .login button:hover{{
      width:97%;
      font-size: 22px;
      
  }}
  .login hr{{
      width: 30%;
      display: inline-block
  }}

  .login p{{
      display: inline-block;
      margin: 0px 10px 30px;
  }}
  .login ul{{
      list-style: none;
      margin-bottom:40px;  
  }}
  .login ul li{{
      display: inline-block;
      margin-right: 30px;
      cursor: pointer;
  }}
  .login ul li:hover{{opacity: 0.6}}
  .login ul li:last-child{{margin-right: 0}}
  .login .copyright{{
      display: inline-block;
      float: none;
  }}
  @media screen and (max-width: 600px) {{
      .login{{
        width: 100%;
      }}
      /* Add more styles specific to smaller screens as needed */
  }}
</style>
<div class="container">
      <div class="login">
         <div class="container">
              <h1>Create an account</h1>
              <form class="sig-form" action="/signup" method="POST">
                <input type="text" name="name" placeholder="Your Name">
                <input type="text" name="theage" placeholder="Your Age">
                <input type="text" name="school" placeholder="Your Current School (Optional)">
                <input type="text" name="class" placeholder="Your Current Class (Optional)">
                <input type="email" name="email" placeholder="Your Email">
                <input type="password" name="password" placeholder="Your Password"><br>
                <input type="password" name="password2" placeholder="Confirm Password"><br>
                <button type="sumbit">Sign Up</button>
              </form>
              <div class="clearfix"></div> 
         </div>
      </div>
    </div>

{{% endblock %}}
		"""
    errorPage = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Error Page</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f0f0f0;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 100vh;
            margin: 0;
        }

        h1 {
            font-size: 2rem;
            margin-bottom: 1rem;
        }

        p {
            font-size: 1rem;
            margin-bottom: 2rem;
        }

        a {
            background-color: #007BFF;
            color: white;
            text-decoration: none;
            padding: 0.5rem 1rem;
            border-radius: 5px;
        }
    </style>
</head>
<body>
    <h1>Sorry, Something Went Wrong</h1>
    <p>It seems we've encountered an issue. Our team is working to fix it. Please try again later.</p>
    <a href="/i">Go back to the homepage</a>
</body>
</html>

		"""

    homePage = """
<!DOCTYPE html>
<html>
<head>
	<meta charset="utf-8">
	<meta name="viewport" content="width=device-width, initial-scale=1">
	<title>Logged in as {{ current_user.name }}</title>
	<style type="text/css">
		@keyframes changeB{
			0%{
				background: linear-gradient(128deg, #d9118747, #11d9c7ad);
			}
			10%{
				background: linear-gradient(138deg, #d9118747, #11d9c7ad);
			}
			20%{
				background: linear-gradient(148deg, #d9118747, #11d9c7ad);
			}
			30%{
				background: linear-gradient(158deg, #d9118747, #11d9c7ad);
			}
			40%{
				background: linear-gradient(168deg, #d9118747, #11d9c7ad);
			}
			50%{
				background: linear-gradient(178deg, #d9118747, #11d9c7ad);
			}
			60%{
				background: linear-gradient(188deg, #d9118747, #11d9c7ad);
			}
			70%{
				background: linear-gradient(198deg, #d9118747, #11d9c7ad);
			}
			80%{
				background: linear-gradient(208deg, #d9118747, #11d9c7ad);
			}
			90%{
				background: linear-gradient(218deg, #d9118747, #11d9c7ad);
			}
			100%{
				background: linear-gradient(228deg, #d9118747, #11d9c7ad);
			}
		}
		body{
			display: flex;
		    justify-content: center;
		    align-items: center;
		    height: 100vh;
			font-family: "Segoe UI";
			transition: ease-in;
			background: linear-gradient(118deg, #d9118747, #11d9c7ad);
			animation: changeB 5s infinite linear;
		}
		body p{
			font-weight: bolder;
			text-align: center;
		}
	</style>
</head>
<body>
	<p>You've done it, you can now redefine, reimagine and recreate with Poel!</p>
</body>
</html>
		"""

		# STATIC(CSS)

    styleCSS = """
/* Start Global Rules */
* {
  box-sizing: border-box;
}
body {
  font-family: 'Open Sans', sans-serif;
}
a {
  text-decoration: none;
}
ul {
  list-style: none;
  padding: 0;
  margin: 0;
}
.container {
  padding-left: 15px;
  padding-right: 15px;
  margin-left: auto;
  margin-right: auto;
}
/* Small */
@media (min-width: 768px) {
  .container {
    width: 750px;
  }
}
/* Medium */
@media (min-width: 992px) {
  .container {
    width: 970px;
  }
}
/* Large */
@media (min-width: 1200px) {
  .container {
    width: 1170px;
  }
}
/* End Global Rules */

/* Start Landing Page */
.landing-page header {
  min-height: 80px;
  display: flex;
}
@media (max-width: 767px) {
  .landing-page header {
    min-height: auto;
    display: initial;
  }
}
.landing-page header .container {
  display: flex;
  align-items: center;
  justify-content: space-between;
}
@media (max-width: 767px) {
  .landing-page header .container {
    flex-direction: column;
    justify-content: center;
  }
}
.landing-page header .logo {
  color: #5d5d5d;
  font-style: italic;
  text-transform: uppercase;
  font-size: 20px;
}
@media (max-width: 767px) {
  .landing-page header .logo {
    margin-top: 20px;
    margin-bottom: 20px;
  }
}
.landing-page header .links {
  display: flex;
  align-items: center;
}
@media (max-width: 767px) {
  .landing-page header .links {
    text-align: center;
    gap: 10px;
  }
}
.landing-page header .links li {
  margin-left: 30px;
  color: #5d5d5d;
  cursor: pointer;
  transition: .3s;
}
@media (max-width: 767px) {
  .landing-page header .links li {
    margin-left: auto;
  }
}
.landing-page header .links li:last-child {
  border-radius: 20px;
  padding: 10px 20px;
  color: #FFF;
  background-color: #6c63ff;
}
.landing-page header .links li:not(:last-child):hover {
  color: #6c63ff;
}
.landing-page .content .container {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 140px;
  min-height: calc(100vh - 80px);
}
@media (max-width: 767px) {
  .landing-page .content .container {
    gap: 0;
    min-height: calc(100vh - 101px);
    justify-content: center;
    flex-direction: column-reverse;
  }
}
@media (max-width: 767px) {
  .landing-page .content .info {
    text-align: center;
    margin-bottom: 15px 
  }
}
.landing-page .content .info h1 {
  color: #5d5d5d;
  font-size: 44px;
}
.landing-page .content .info p {
  margin: 0;
  line-height: 1.6;
  font-size: 15px;
  color: #5d5d5d;
}
.landing-page .content .info button {
  border: 0;
  border-radius: 20px;
  padding: 12px 30px;
  margin-top: 30px;
  cursor: pointer;
  color: #FFF;
  background-color: #6c63ff;
}
.landing-page .content .image img {
  max-width: 100%;
}
/* End Landing Page */

.modal {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    
    z-index: 100000000;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.7);
}

.modal-content {
    position: absolute;
    z-index: 100000000;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    background-color: #fff;
    padding: 20px;
    border-radius: 5px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
    text-align: center;
}

.close {
    position: absolute;
    top: 10px;
    right: 10px;
    font-size: 20px;
    cursor: pointer;
}

		"""

		# STATIC(JS)

    scriptJS = """
// Get references to the modal and buttons
const modal = document.getElementById('modal');
try{
    const closeModalBtn = document.getElementById('closeModalBtn');

    // Close the modal
    closeModalBtn.addEventListener('click', () => {
        modal.style.display = 'none';
    });
} catch (error) {
    console.log('error')
}


// Close the modal if the user clicks outside the modal content
window.addEventListener('click', (event) => {
    if (event.target === modal) {
        modal.style.display = 'none';
    }
});

		"""
		

    with open(f"{DIR}\\main.py", "w") as mainFile:
    	mainFile.write(mainFileContent)

    with open(f"{DIR_WEBSITE}\\__init__.py", "w") as initFile:
    	initFile.write(initFileContent)

    with open(f"{DIR_WEBSITE}\\views.py", "w") as viewsFile:
    	viewsFile.write(viewsFileContent)

    with open(f"{DIR_WEBSITE}\\auth.py", "w") as authFile:
    	authFile.write(authFileContent)

    with open(f"{DIR_WEBSITE}\\models.py", "w") as modelsFile:
    	modelsFile.write(modelsFileContent)

    with open(f"{DIR_TEMPLATES}\\base.html", "w") as baseFile:
    	baseFile.write(basePage)

    with open(f"{DIR_TEMPLATES}\\login.html", "w") as loginFile:
    	loginFile.write(loginPage)

    with open(f"{DIR_TEMPLATES}\\signup.html", "w") as signupFile:
    	signupFile.write(signupPage)

    with open(f"{DIR_TEMPLATES}\\broken-page.html", "w") as errorFile:
    	errorFile.write(errorPage)

    with open(f"{DIR_TEMPLATES}\\home.html", "w") as homeFile:
    	homeFile.write(homePage)

    with open(f"{DIR_CSS}\\style.css", "w") as styleFile:
    	styleFile.write(styleCSS)

    with open(f"{DIR_JS}\\index.js", "w") as indexFile:
    	indexFile.write(scriptJS)
		
    print(f"Created {project_name} in [C:]")

    butt2 = CTkButton(root, text=f"Run {project_name}", width=10, command=runProject)
    butt2.place(x=200, y=-5, rely=1.0, anchor='sw')

		# butt3 = CTkButton(root, text=f"Manage {project_name}", width=10, command=manageProject)
		# butt3.place(x=300, y=-5, rely=1.0, anchor='sw')

  dashboard.pack(pady=30, anchor="center")

  CTkLabel(dashboard, text="Create Flask Project", font=(FontFamily, 25, "bold")).pack(pady=10)

  CTkLabel(dashboard, text="Project Name", font=(FontFamily, 13)).pack(pady=10)

  projectName = CTkEntry(dashboard, width=200)
  projectName.pack(pady=10)

  CTkLabel(dashboard, text="If your project is going to use a Database\nCreate one now", font=(FontFamily, 13)).pack(pady=10)

  databaseName = CTkEntry(dashboard, width=200)
  databaseName.pack(pady=10)

  CTkLabel(dashboard, text="Set a secret key. Just put gibberish in there", font=(FontFamily, 13)).pack(pady=10)

  secretKeyName = CTkEntry(dashboard, width=200)
  secretKeyName.pack(pady=10)


  createButton = CTkButton(dashboard, text="Create Flask Project", command=createProject)
  createButton.pack(pady=10)



root = CTk()
root.title("Bluvid Poel")
root.resizable(width=False, height=False)
root.geometry("500x600")
root.iconbitmap("media/Po.png")
style = ThemedStyle(root)
style.set_theme("arc")

# wide_Img = Image.open("media/Poel_Wide.png")
# photo3 = ImageTk.PhotoImage(wide_Img)
# lb = CTkLabel(root, image=photo3, text="")
# lb.pack()

CTkLabel(root, text="Poel", font=("Segoe UI", 50, "bold")).pack()
CTkLabel(root, text="Lightweight Flask Project Maker").pack()

dashboard = CTkFrame(root, height=500, width=400)#bg="white"


# Create a button for opening and saving apps
new_img = Image.open("media/new.png")
photo2 = ImageTk.PhotoImage(new_img)
butt1 = CTkButton(root, image=photo2, text="", width=10, command=openDashboard)
butt1.place(x=5, y=-5, rely=1.0, anchor='sw')


root.mainloop()