function onOpenDeviceForm(id, deviceName, deviceRank, ipAddress, lastAliveTimestamp) {
    document.getElementById("deviceForm").style.display = "flex";
    document.getElementById("formBackground").style.display = "block";
    // display delete button if input fields are given
    if (id && deviceName && deviceRank && ipAddress && lastAliveTimestamp) {
        document.getElementById("deleteButton").style.display = "block";
        document.getElementById(deviceRank + "_option").classList.add("active");
    }
    // set values of all fields
    document.getElementById("deviceIdHolder").value = id;
    document.getElementById("deviceNameInput").value = deviceName;
    document.getElementById("ipAddressInput").value = ipAddress;
    document.getElementById("lastAliveTimestampHolder").value = lastAliveTimestamp;
    document.getElementById("deviceRankDropdownButton").value = deviceRank;
    document.getElementById("deviceRankDropdownButton").innerText = deviceRank;
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
    const deviceRank = document.getElementById("deviceRankDropdownButton").value;
    // ip format validation source: https://www.w3resource.com/javascript/form/ip-address-validation.php
    const ipFormat = /^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$/;
    if (deviceName.length > 0 && ipAddress.match(ipFormat) && deviceRank !== "Rank") {
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
    document.getElementById("deviceRankDropdownButton").value = "Rank";
    document.getElementById("deviceRankDropdownButton").innerText = "Rank";
    setRankDropdownValue("Rank");
}

function setRankDropdownValue(rankName) {
    // remove all 'active' classes from elements in the device rank dropdown
    let activeElements = document.getElementsByClassName("active");
    for (i = 0; i < activeElements.length; i++) {
        // check if this element has the class 'rankDropdownItem' in its classlist
        if (activeElements[i].classList.contains("rankDropdownItem")) {
            // then we want to remove the 'active' class
            activeElements[i].classList.remove("active");
        }
    }
    // don't set anything to "active" if given rankName is "Rank"
    if (rankName !== "Rank") {
        document.getElementById(rankName + "_option").classList.add("active");
    }
    // update button text
    let button = document.getElementById("deviceRankDropdownButton")
    button.value = rankName;
    button.innerText = rankName;

    // validation for submit button
    activateSubmitButtonIfValidInput();
}

function onSubmitDeviceForm() {
    startLoading();
    // if we have an id then we want to PUT, else we can POST
    if (document.getElementById("deviceIdHolder").value === "") {
        // this is a new device, post
        postNewDevice();
    } else {
        putDevice();
    }
}

function onDeleteDeviceForm() {
    startLoading();
    const id = document.getElementById("deviceIdHolder").value;
    let fetchPromise = del("/devices/" + id);
    fetchPromise.then(response => {
        window.location.href = response.url;
    });
}

function postNewDevice() {
    const deviceName = document.getElementById("deviceNameInput").value;
    const deviceRank = document.getElementById("deviceRankDropdownButton").value;
    const ipAddress = document.getElementById("ipAddressInput").value;
    const data = {"deviceName": deviceName, "deviceRank": deviceRank, "ipAddress": ipAddress};
    // send POST request
    let fetchPromise = post("/devices", data);
    fetchPromise.then(response => {
        window.location.href = response.url;
    });
}

function putDevice() {
    const id = document.getElementById("deviceIdHolder").value;
    const deviceName = document.getElementById("deviceNameInput").value;
    const deviceRank = document.getElementById("deviceRankDropdownButton").value;
    const ipAddress = document.getElementById("ipAddressInput").value;
    const lastAliveTimestamp = document.getElementById("lastAliveTimestampHolder").value;
    const data = {
        "id": id,
        "deviceName": deviceName,
        "deviceRank": deviceRank,
        "ipAddress": ipAddress,
        "lastAliveTimestamp": lastAliveTimestamp
    };
    // send PUT request
    let fetchPromise = put("/devices", data);
    fetchPromise.then(response => {
        window.location.href = response.url;
    });
}

function refreshPage() {
    startLoading();
    location.reload();
}