from flask import redirect, url_for, request

from app import app
from server.enums.DeviceRank import DeviceRank
from server.models.Device import Device
from server.util.ControllerHelper import ControllerHelper


@app.route("/devices", methods=["POST"])
def addDevice():
    # convert the POST request headers into a python dictionary
    dataDict = ControllerHelper.getDictFromRequestObj(request)
    device = Device(dataDict["deviceName"], DeviceRank.fromStr(dataDict["deviceRank"]), dataDict["ipAddress"])
    print(device)
    return redirect(url_for("index"))


@app.route("/devices", methods=["PUT"])
def updateDevice():
    # convert the PUT request headers into a python dictionary
    dataDict = ControllerHelper.getDictFromRequestObj(request)
    device = Device(dataDict["deviceName"], DeviceRank.fromStr(dataDict["deviceRank"]), dataDict["ipAddress"],
                    id=dataDict["id"],
                    lastAliveTimestamp=dataDict["lastAliveTimestamp"])
    print(device)
    return redirect(url_for("index"))


@app.route("/devices/<string:id>", methods=["DELETE"])
def deleteDevice(id: str):
    print(id)
    return redirect(url_for("index"))
