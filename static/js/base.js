// method for sending POST requests
window.post = function(url, data) {
    return fetch(url, {method: "POST", body: JSON.stringify(data)});
}

// method for sending PUT requests
window.put = function(url, data) {
    return fetch(url, {method: "PUT", body: JSON.stringify(data)});
}

function startLoading() {
    document.querySelector("#loader-wrapper").style.display = "flex";
    document.querySelector("#loader-wrapper").style.visibility = "visible";
}

function stopLoading() {
    document.querySelector("#loader-wrapper").style.display = "none";
    document.querySelector("#loader-wrapper").style.visibility = "hidden";
    document.querySelector("body").style.visibility = "visible";
}

function onOpenDeviceForm(id, deviceName, ipAddress, lastAliveTimestamp) {
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
    document.getElementById("deviceIdHolder").value = id;
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
    // ip format validation source: https://www.w3resource.com/javascript/form/ip-address-validation.php
    const ipFormat = /^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$/;
    if(deviceName.length > 0 && ipAddress.match(ipFormat)) {
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

function onSubmitDeviceForm() {
    // if we have an id then we want to PUT, else we can POST
    if(document.getElementById("deviceIdHolder").value == "") {
        // this is a new device, post
        postNewDevice();
    } else {
        putDevice();
    }
}

function postNewDevice() {
    const deviceName = document.getElementById("deviceNameInput").value;
    const ipAddress = document.getElementById("ipAddressInput").value;
    const data = {"deviceName": deviceName, "ipAddress": ipAddress};
    // send POST request
    let fetchPromise = post("/devices", data);
    fetchPromise.then(response => {
      window.location.href = response.url;
    });
}

function putDevice() {
    const id = document.getElementById("deviceIdHolder").value
    const deviceName = document.getElementById("deviceNameInput").value;
    const ipAddress = document.getElementById("ipAddressInput").value;
    const lastAliveTimestamp = document.getElementById("lastAliveTimestampField").value;
    const data = {"id": id, "deviceName": deviceName, "ipAddress": ipAddress, "lastAliveTimestamp": lastAliveTimestamp};
    // send POST request
    let fetchPromise = put("/devices", data);
    fetchPromise.then(response => {
      window.location.href = response.url;
    });
}

document.onreadystatechange = function() {
    if (document.readyState !== "complete") {
        startLoading();
    } else {
        stopLoading();
//        onOpenDeviceForm();
    }
}