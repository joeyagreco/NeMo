from flask import request

from app import app
from server.controllers.pageController import *
from server.models.Settings import Settings
from server.util.ControllerHelper import ControllerHelper


@app.route("/settings", methods=["PUT"])
def updateSettings():
    # convert the PUT request headers into a python dictionary
    dataDict = ControllerHelper.getDictFromRequestObj(request)
    settings = Settings(dataDict["pingsToSave"], dataDict["pingOnlineThreshold"], dataDict["pageRefreshFrequency"],
                        dataDict["pingCriticalRefreshFrequency"], dataDict["pingKnownRefreshFrequency"],
                        dataDict["pingScanFrequency"])
    settingsService = SettingsService()
    settingsService.updateSettings(settings)
    return redirect(url_for("settingsPage"))
