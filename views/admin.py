from flask import redirect, url_for, render_template

from app import app


@app.route('/favicon.ico')
def favicon():
    """
    This is for the browser icon.
    """
    return redirect(url_for('static', filename='icons/network_icon.ico'))


@app.route("/")
def index():
    return render_template("homePage.html")
