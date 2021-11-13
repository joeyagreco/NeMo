function startLoading() {
    document.querySelector("#loader-wrapper").style.display = "flex";
    document.querySelector("#loader-wrapper").style.visibility = "visible";
}

function stopLoading() {
    document.querySelector("#loader-wrapper").style.display = "none";
    document.querySelector("#loader-wrapper").style.visibility = "hidden";
    document.querySelector("body").style.visibility = "visible";
}

function onOpenDeviceForm() {
    document.getElementById("deviceForm").style.display = "flex";
    document.getElementById("formBackground").style.display = "block";
}

function onCloseDeviceForm() {
    document.getElementById("deviceForm").style.display = "none";
    document.getElementById("formBackground").style.display = "none";
    document.getElementById("delete-button").style.display = "none";
    document.getElementById("submit-button").classList.add("disabled");
//    document.getElementById("submit-button").innerHTML = "Submit";
//    setTransactionPopupToDefaultValues();
}

function activateSubmitButtonIfValidInput() {
    const deviceName = document.getElementById("deviceNameInput").value;
    const ipAddress = document.getElementById("ipAddressInput").value;
    console.log(ipAddress.split(".").length);
    if(deviceName.length > 0 && ipAddress.length >= 7 && ipAddress.split(".").length == 4) {
        document.getElementById("submitButton").classList.remove("disabled");
        document.getElementById("submitButton").disabled = false;
    } else {
        document.getElementById("submitButton").classList.add("disabled");
        document.getElementById("submitButton").disabled = true;
    }
}

document.onreadystatechange = function() {
    if (document.readyState !== "complete") {
        startLoading();
    } else {
        stopLoading();
        onOpenDeviceForm();
    }
}