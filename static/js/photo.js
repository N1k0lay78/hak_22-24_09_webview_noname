var video = document.getElementById("video");
video.setAttribute('playsinline', '');
video.setAttribute('autoplay', '');
video.setAttribute('muted', '');

/* Setting up the constraint */
var facingMode = "user"; // Can be 'user' or 'environment' to access back or front camera (NEAT!)
var constraints = {
    audio: false,
    video: {
        facingMode: facingMode,
        width: 1280,
        height: 640
    }
};

/* Stream it to video element */
navigator.mediaDevices.getUserMedia(constraints).then(function success(stream) {
    video.srcObject = stream;
});

function ask_ai() {
    console.log("START", window.isSecureContext)
    var canvas = document.createElement("canvas")
    var video = document.getElementById("video")
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;

    console.log(video.videoWidth, video.videoHeight)
    console.log(video.clientWidth, video.clientHeight)

    canvas
        .getContext("2d")
        .drawImage(video, 0, 0, video.videoWidth, video.videoHeight)
    var data = new FormData()
    data.append('file', canvas.toDataURL("image/png"))

    console.log("ADD PHOTO")

    fetch('/check_img', {
        method: 'POST',
        body: data
    }).then((response) => response.json())
        .then((data) => {
            document.getElementById("type_name").innerText = data.type
        })
}