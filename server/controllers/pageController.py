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
    devicesWrapper = deviceService.getDevicesWrapper()
    # TODO: move the logic for getting valid device ranks to the service layer
    deviceRanks = [DeviceRank.CRITICAL, DeviceRank.KNOWN]
    return render_template("devicesPage/devicesPage.html",
                           critical_devices=devicesWrapper.criticalDevices,
                           known_devices=devicesWrapper.knownDevices,
                           unknown_devices=devicesWrapper.unknownDevices,
                           device_ranks=deviceRanks)


@app.route("/settings-page")
def settingsPage():
    settingsService = SettingsService()
    settings = settingsService.getSettings()
    return render_template("settingsPage.html",
                           settings=settings)
