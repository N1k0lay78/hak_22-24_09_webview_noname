function dragover_handler(ev) {
    ev.preventDefault();
    ev.dataTransfer.dropEffect = "copy";
}

function drop_handler(ev) {
    ev.preventDefault();

    let dt = ev.dataTransfer
    let files = dt.files

    Array.prototype.forEach.call(dt.files,(file) => {
        var formData = new FormData()
        formData.append('file', file)
        formData.append("rjkz", "RJKZAVR")

        console.log(formData.file, "ADSADd")

        fetch("/check_img", {
            method: 'POST',
            body: formData
        }).then((response) => response.json())
        .then((data) => {
            let images = document.getElementById("img")
            let div = document.createElement("div")
            div.classList.add("checked__block")
            let image = document.createElement('img')
            image.src="data:image/png;base64,"+data.img
            image.alt=data.type
            div.append(image)
            let p = document.createElement('p')
            p.innerText = data.type
            div.append(p)
            images.append(div)
            console.log("GET ANSWER")
        })
    })
}