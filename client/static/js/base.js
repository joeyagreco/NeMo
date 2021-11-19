document.onreadystatechange = function () {
    if (document.readyState !== "complete") {
        startLoading();
    } else {
        stopLoading();
    }
}