function devicesPageRedirect() {
    startLoading();
    window.location = "/devices-page";
}

function settingsPageRedirect() {
    startLoading();
    window.location = "/settings-page";
}

document.onreadystatechange = function () {
    if (document.readyState !== "complete") {
        startLoading();
    } else {
        stopLoading();
    }
}