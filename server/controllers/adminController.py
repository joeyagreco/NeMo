from flask import redirect, url_for, render_template

from app import app
from server.enums.DeviceRank import DeviceRank
from server.services.DeviceService import DeviceService


@app.route('/favicon.ico')
def favicon():
    """
    This is for the browser icon.
    """
    return redirect(url_for('static', filename='icons/network_icon.ico'))


@app.route("/")
def index():
    deviceService = DeviceService()
    criticalDevices = deviceService.getDevicesByDeviceRank(DeviceRank.CRITICAL)
    return render_template("devicesPage/devicesPage.html", critical_devices=criticalDevices,
                           device_rank_class=DeviceRank)
