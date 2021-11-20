from flask import redirect, url_for, request

from app import app
from server.models.Settings import Setting
from server.util.ControllerHelper import ControllerHelper


@app.route("/settings", methods=["PUT"])
def updateSettings():
    # convert the PUT request headers into a python dictionary
    dataDict = ControllerHelper.getDictFromRequestObj(request)
    setting = Setting(dataDict["pingsToSave"], dataDict["pingOnlineThreshold"], dataDict["pageRefreshFrequency"],
                      dataDict["pingCriticalRefreshFrequency"], dataDict["pingKnownRefreshFrequency"],
                      dataDict["pingScanFrequency"])
    print(setting)
    return redirect(url_for("settingsPage"))
