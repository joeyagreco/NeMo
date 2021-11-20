from flask import render_template

from app import app


@app.route("/settings")
def settings():
    return render_template("settingsPage.html")
