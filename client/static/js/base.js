function devicesPageRedirect() {
    startLoading();
    window.location = "/devices";
}

function settingsPageRedirect() {
    startLoading();
    window.location = "/settings";
}

document.onreadystatechange = function () {
    if (document.readyState !== "complete") {
        startLoading();
    } else {
        stopLoading();
    }
}