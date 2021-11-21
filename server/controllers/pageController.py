from flask import render_template, url_for, redirect

from app import app
from server.enums.DeviceRank import DeviceRank
from server.services.DeviceService import DeviceService
from server.services.SettingsService import SettingsService


@app.route("/")
def index():
    return redirect(url_for("devicesPage"))


@app.route("/devices-page")
def devicesPage():
    deviceService = DeviceService()
    criticalDevices = deviceService.getDevicesByDeviceRank(DeviceRank.CRITICAL)
    # deviceService.getAllDevices()
    deviceService.tmpGetPing()
    return render_template("devicesPage/devicesPage.html",
                           critical_devices=criticalDevices,
                           known_devices=[],
                           unknown_devices=[],
                           device_rank_class=DeviceRank)


@app.route("/settings-page")
def settingsPage():
    settingsService = SettingsService()
    settings = settingsService.getSettings()
    return render_template("settingsPage.html",
                           settings=settings)
