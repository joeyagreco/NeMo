function startLoading() {
    document.querySelector("#loader-wrapper").style.display = "flex";
    document.querySelector("#loader-wrapper").style.visibility = "visible";
}

function stopLoading() {
    document.querySelector("#loader-wrapper").style.display = "none";
    document.querySelector("#loader-wrapper").style.visibility = "hidden";
    document.querySelector("body").style.visibility = "visible";
}

function onOpenDeviceForm(deviceName, ipAddress, lastAliveTimestamp) {
    document.getElementById("deviceForm").style.display = "flex";
    document.getElementById("formBackground").style.display = "block";
    // display delete button if input fields are given
    if(deviceName && ipAddress && lastAliveTimestamp) {
        document.getElementById("deleteButton").style.display = "block";
        document.getElementById("lastAliveTimestampField").style.display = "block";
        document.getElementById("lastAliveTimestampFieldLabel").style.display = "block";
    } else {
        document.getElementById("lastAliveTimestampField").style.display = "none";
        document.getElementById("lastAliveTimestampFieldLabel").style.display = "none";
    }
    // set values of all fields
    document.getElementById("deviceNameInput").value = deviceName;
    document.getElementById("ipAddressInput").value = ipAddress;
    document.getElementById("lastAliveTimestampField").value = lastAliveTimestamp;
    activateSubmitButtonIfValidInput();
}

function onCloseDeviceForm() {
    document.getElementById("deviceForm").style.display = "none";
    document.getElementById("formBackground").style.display = "none";
    document.getElementById("deleteButton").style.display = "none";
    document.getElementById("submitButton").classList.add("disabled");
    document.getElementById("submitButton").innerHTML = "Submit";
    setDeviceFormInputFieldsToDefaultValues();
}

function activateSubmitButtonIfValidInput() {
    const deviceName = document.getElementById("deviceNameInput").value;
    const ipAddress = document.getElementById("ipAddressInput").value;
    if(deviceName.length > 0 && ipAddress.length >= 7 && ipAddress.split(".").length == 4) {
        document.getElementById("submitButton").classList.remove("disabled");
        document.getElementById("submitButton").disabled = false;
    } else {
        document.getElementById("submitButton").classList.add("disabled");
        document.getElementById("submitButton").disabled = true;
    }
}

function setDeviceFormInputFieldsToDefaultValues() {
    document.getElementById("deviceNameInput").value = "";
    document.getElementById("ipAddressInput").value = "";
}

document.onreadystatechange = function() {
    if (document.readyState !== "complete") {
        startLoading();
    } else {
        stopLoading();
//        onOpenDeviceForm();
    }
}