import ast

from flask import redirect, url_for, request

from app import app
from server.models.Device import Device


@app.route("/devices", methods=["POST"])
def addDevice():
    # convert the POST request headers into a python dictionary
    dataStr = request.data.decode("UTF-8")
    dataDict = ast.literal_eval(dataStr)
    device = Device(dataDict["deviceName"], dataDict["ipAddress"])
    print(device)
    return redirect(url_for("index"))


@app.route("/devices", methods=["PUT"])
def updateDevice():
    # convert the POST request headers into a python dictionary
    dataStr = request.data.decode("UTF-8")
    dataDict = ast.literal_eval(dataStr)
    device = Device(dataDict["deviceName"], dataDict["ipAddress"], id=dataDict["id"],
                    lastAliveTimestamp=dataDict["lastAliveTimestamp"])
    print(device)
    return redirect(url_for("index"))


@app.route("/devices/<id>", methods=["DELETE"])
def deleteDevice(id):
    print(id)
    return redirect(url_for("index"))
