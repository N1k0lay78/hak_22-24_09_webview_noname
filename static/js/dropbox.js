function dragover_handler(ev) {
    ev.preventDefault();

    // при перетаскивании изображении оно будет копироваться
    ev.dataTransfer.dropEffect = "copy";
}

function drop_handler(ev) {
    ev.preventDefault();

    // получаем перемещённые файлы
    let dt = ev.dataTransfer
    let files = dt.files

    // создаём запросы в API по очереди
    for (let i = 0; i < dt.files.length; i++) {
        // запрос на классификацию детали
        const a = (file) => {
            // создаём форму запроса
            var formData = new FormData()
            formData.append('file', file)

            // создаём запрос для API
            fetch("/check_img", {
                method: 'POST',
                body: formData
            }).then((response) => response.json())
                .then((data) => {
                    // добавляем классифицированное отображение
                    // создаём <div> и добавляем в него <img> и <p>
                    let div = document.createElement("div")
                    let images = document.getElementById("img")
                    div.classList.add("checked__block")
                    let image = document.createElement('img')
                    image.src = "data:image/png;base64," + data.img
                    image.alt = data.type
                    div.append(image)
                    let p = document.createElement('p')
                    // если класс определён, то добавляем ссылку на документ
                    if (!data.successful_determination) {
                        let link = document.createElement('a')
                        link.innerText = data.type
                        link.href = "/blueprint/" + data.link
                        p.append(link)
                    } else {
                        p.innerText = data.type
                    }
                    div.append(p)
                    images.append(div)
                })
        }
        // запрос в API раз в 7 секунд
        setTimeout(a, 7000*i, dt.files[i]);
    }
}