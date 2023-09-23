// выводим изображение с камеры
let types = {}
let video = document.getElementById("video");
video.setAttribute('playsinline', '');
video.setAttribute('autoplay', '');
video.setAttribute('muted', '');

/* Setting up the constraint */
let facingMode = "user"; // Can be 'user' or 'environment' to access back or front camera (NEAT!)
let constraints = {
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

function updateTypes() {
    let find = document.getElementById("find")
    find.innerHTML = ""
    for (const name in types) {
        let el = document.createElement("p")
        el.innerText = `${name}: `
        let span = document.createElement("span")
        span.innerText = `${types[name]} шт.`
        el.append(span)
        find.append(el)
    }
}

function ask_ai() {
    // получаем видеопоток и отрисовываем его на холсте
    let canvas = document.createElement("canvas")
    let video = document.getElementById("video")
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    canvas
        .getContext("2d")
        .drawImage(video, 0, 0, video.videoWidth, video.videoHeight)

    // сохраняем изображение с холста, как изображение
    let data = new FormData()
    data.append('file', canvas.toDataURL("image/png"))

    // создаём запрос для API
    fetch('/check_img', {
        method: 'POST',
        body: data
    }).then((response) => response.json())
        .then((data) => {
            // изменяем отображение относительно полученного ответа
            document.getElementById("type_name").innerText = data.type

            // обновляем данные об количестве найденных изделий одного типа
            if (data.type in types) {
                types[data.type]++
            } else {
                types[data.type] = 1
            }
            updateTypes()

            // если может быть допущена ошибка добавляем ссылку на PDF для проверки
            document.getElementById("info").innerHTML = ""
            if (!data.successful_determination) {
                let a = document.createElement("a")
                a.classList.add("open_pdf")
                a.href = "/blueprint/" + data.link
                a.innerText = "открыть чертёж изделия →"
                document.getElementById("info").append(a)
            }
        })
}