let countLoading = 0;

function updateAnimation(val) {
    countLoading += val
    if (countLoading > 0) {
        console.log("LOADING")
        document.getElementById("loading").classList.add("show")
    } else {
        console.log("END LOAD")
        document.getElementById("loading").classList.remove("show")
    }
}