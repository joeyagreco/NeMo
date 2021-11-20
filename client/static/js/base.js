function devicesPageRedirect() {
    startLoading();
    window.location = "/";
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