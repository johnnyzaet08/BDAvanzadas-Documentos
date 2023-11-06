from flask import Flask, render_template, request, redirect, url_for
from flask_cors import CORS
from api import *

app = Flask(__name__)
app.static_folder = "static"
app.static_url_path = "/static"
app.secret_key = 'BDA-2023'

CORS(app)
socketio.init_app(app)

# Authentication check function
def check_authentication():
    if "username" in session:
        return True
    return False

@app.route("/")
def index():
    if check_authentication():
        return redirect(url_for("home"))
    return redirect(url_for("login"))

@app.route("/home")
def home():
    if not check_authentication():
        return redirect(url_for("login"))
    return render_template("home.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    access = False
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = getUsersEmail(username)
        if  len(user) == 1:
            if user[0]['contraseña'] == password:
                access = True
                if user[0]['tipo'] == 'administrador':
                    session["admin"] = True
                else:
                    session["admin"] = False
        else:
            return redirect(url_for("login", message="User not found"))

        if access:
            session["username"] = username
            return redirect(url_for("home"))
        else:
            return redirect(url_for("login", message="Invalid Credentials"))

    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    save = False
    if request.method == "POST":
        try:
            if("@admin.em" in request.form["username"] and request.form["tipo_cuenta"] == "administrador"):
                save = True
            elif(request.form["tipo_cuenta"] == "administrador" or "@admin.em" in request.form["username"]):
                return redirect(url_for("register", message="Error: Invalid Email"))
            else:
                save = True
            if(save):
                if addUser(request.form["username"], request.form["password"], request.form["tipo_cuenta"]):
                    return redirect(url_for("login", message="User added Successful"))
                else:
                    return redirect(url_for("register", message="Error Adding User"))
        except Exception as e:
            return redirect(url_for("register", message="Error Adding User"))
    return render_template("register.html")

@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("login"))

@app.route("/register_travel")
def register_travel():
    if not check_authentication():
        return redirect(url_for("login"))
    return render_template("register_travel.html")

@app.route("/modify_travel")
def modify_travel():
    if not check_authentication():
        return redirect(url_for("login"))
    return render_template("modify_eliminate_travel.html")

@app.route("/travel_history")
def travel_history():
    if not check_authentication():
        return redirect(url_for("login"))
    return render_template("history_request.html")

@app.route("/admin/evaluate_request")
def evaluate_request():
    if not check_authentication():  # Add additional check for admin role
        return redirect(url_for("login"))
    return render_template("evaluate_request.html")

@app.route("/admin/scheduled_travels")
def scheduled_travels():
    if not check_authentication():  # Add additional check for admin role
        return redirect(url_for("login"))
    return render_template("scheduled_travels.html")

@app.route("/admin/international_travels")
def international_travels():
    if not check_authentication():  # Add additional check for admin role
        return redirect(url_for("login"))
    return render_template("international_travels.html")

@app.route("/admin/specific_destination")
def specific_destination():
    if not check_authentication():  # Add additional check for admin role
        return redirect(url_for("login"))
    return render_template("specific_destination.html")

if __name__ == '__main__':
    socketio.run(app, debug=True)