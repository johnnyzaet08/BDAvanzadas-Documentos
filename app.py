from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Authentication check function
def check_authentication():
    if "username" in session:
        return True
    return False

@app.route("/")
def index():
    #if check_authentication():
    #    return redirect(url_for("home"))
    return redirect(url_for("login"))

@app.route("/home")
def home():
    # if not check_authentication():
    #    return redirect(url_for("login"))
    return render_template("home.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        # TODO: Validate username and password with database
        if True:  # Replace with actual validation
            session["username"] = username
            return redirect(url_for("home"))
        else:
            return redirect(url_for("login", message="Invalid Credentials"))

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("login"))

@app.route("/register_travel")
def register_travel():
    #if not check_authentication():
    #    return redirect(url_for("login"))
    return render_template("register_travel.html")

@app.route("/modify_travel")
def modify_travel():
    #if not check_authentication():
    #    return redirect(url_for("login"))
    return render_template("modify_eliminate_travel.html")

@app.route("/travel_history")
def travel_history():
    if not check_authentication():
        return redirect(url_for("login"))
    return render_template("travel_history.html")

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
    app.run(debug=True)