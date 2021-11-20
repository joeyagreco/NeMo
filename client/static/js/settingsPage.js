function putSettings() {
    const pingsToSave = document.getElementById("pingsToSaveInput").value;
    const pingOnlineThreshold = document.getElementById("pingOnlineThresholdInput").value;
    const pageRefreshFrequency = document.getElementById("pageRefreshFrequencyInput").value;
    const pingCriticalRefreshFrequency = document.getElementById("pingCriticalRefreshFrequencyInput").value;
    const pingKnownRefreshFrequency = document.getElementById("pingKnownRefreshFrequencyInput").value;
    const pingScanFrequency = document.getElementById("pingScanFrequencyInput").value;

    const data = {
        "pingsToSave": pingsToSave,
        "pingOnlineThreshold": pingOnlineThreshold,
        "pageRefreshFrequency": pageRefreshFrequency,
        "pingCriticalRefreshFrequency": pingCriticalRefreshFrequency,
        "pingKnownRefreshFrequency": pingKnownRefreshFrequency,
        "pingScanFrequency": pingScanFrequency
    };
    // send POST request
    let fetchPromise = put("/settings", data);
    fetchPromise.then(response => {
        window.location.href = response.url;
    });
}

function activateUpdateButtonIfValidInput() {
    const pingsToSave = document.getElementById("pingsToSaveInput").value;
    const pingOnlineThreshold = document.getElementById("pingOnlineThresholdInput").value;
    const pageRefreshFrequency = document.getElementById("pageRefreshFrequencyInput").value;
    const pingCriticalRefreshFrequency = document.getElementById("pingCriticalRefreshFrequencyInput").value;
    const pingKnownRefreshFrequency = document.getElementById("pingKnownRefreshFrequencyInput").value;
    const pingScanFrequency = document.getElementById("pingScanFrequencyInput").value;

    if (pingsToSave > 0 && pingOnlineThreshold <= 100 && pingOnlineThreshold > 0 && pageRefreshFrequency > 0 && pingCriticalRefreshFrequency > 0 && pingKnownRefreshFrequency > 0 && pingScanFrequency > 0) {
        document.getElementById("updateSettingsButton").classList.remove("disabled");
        document.getElementById("updateSettingsButton").disabled = false;
    } else {
        document.getElementById("updateSettingsButton").classList.add("disabled");
        document.getElementById("updateSettingsButton").disabled = true;
    }

}