import pandas as pd
from flask import redirect, url_for, render_template

from app import app
from server.models.Device import Device


@app.route('/favicon.ico')
def favicon():
    """
    This is for the browser icon.
    """
    return redirect(url_for('static', filename='icons/network_icon.ico'))


@app.route("/")
def index():
    d1 = Device("Router", "192.168.1.1", id="1", lastAliveTimestamp=pd.Timestamp('2017-01-01T12'))
    d2 = Device("Switch", "192.168.1.5", id="2", lastAliveTimestamp=pd.Timestamp('2017-01-01T12'))
    d3 = Device("JAccessPoint", "192.168.1.10", id="3", lastAliveTimestamp=pd.Timestamp('2017-01-01T12'))
    devices = [d1, d2, d3]
    return render_template("homePage/homePage.html", devices=devices)
