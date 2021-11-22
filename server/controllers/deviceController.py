from flask import redirect, url_for, request

from app import app
from server.enums.DeviceRank import DeviceRank
from server.models.DeviceBE import DeviceBE
from server.services.DeviceService import DeviceService
from server.util.ControllerHelper import ControllerHelper


@app.route("/devices", methods=["POST"])
def addDevice():
    # convert the POST request headers into a python dictionary
    dataDict = ControllerHelper.getDictFromRequestObj(request)
    device = DeviceBE(dataDict["deviceName"], DeviceRank.fromStr(dataDict["deviceRank"]), dataDict["ipAddress"])
    deviceService = DeviceService()
    deviceService.addDeviceAndItsPings(device)
    return redirect(url_for("devicesPage"))


@app.route("/devices", methods=["PUT"])
def updateDevice():
    # convert the PUT request headers into a python dictionary
    dataDict = ControllerHelper.getDictFromRequestObj(request)
    device = DeviceBE(dataDict["deviceName"],
                      DeviceRank.fromStr(dataDict["deviceRank"]),
                      dataDict["ipAddress"],
                      id=dataDict["id"])
    deviceService = DeviceService()
    deviceService.updateDeviceAndItsPings(device)
    return redirect(url_for("devicesPage"))


@app.route("/devices/<int:deviceId>", methods=["DELETE"])
def deleteDevice(deviceId: int):
    deviceService = DeviceService()
    deviceService.deleteDeviceAndItsPingsByDeviceId(deviceId)
    return redirect(url_for("devicesPage"))
