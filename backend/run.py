import io
from flask import Flask, render_template, request, json, jsonify, send_file
import config
import urllib.request
from PIL import Image
from base64 import encodebytes
from ultralytics import YOLO
import numpy as np
import cv2
from dict_links import rus_names, name_to_pdf

application = Flask(__name__)
application.config.from_object(config)


@application.route("/")
def promotional_page():
    # если windows, то возвращаем desktop версию сайта, иначе мобильную
    is_desktop = request.headers.get('User-Agent').split()[1][1:-1].split()[0] == "Window"
    return render_template('base.html', title="Обработка изображения", is_desktop=is_desktop)


def answer(weight_path: str, img_path: str) -> (str, str):
    # TODO:
    # брать из весов успешность определения класса
    # если не получилось распознать возвращаем successful_determination=False

    # загрузка изображения
    img = Image.open(img_path).convert('RGB')
    img_array = np.array(img)

    # сжатие и перевод в чб
    resized_image = cv2.resize(img_array, (640, 640))
    # gray_image = cv2.cvtColor(resized_image, cv2.COLOR_BGR2GRAY)

    # загрузка модели с весами
    try:
        model = YOLO(weight_path)
    except:
        return "Weights file is not found!", ""

    # расчёт вероятности
    try:
        results = model.predict(resized_image)
        names = model.names
    except FileNotFoundError:
        return "Image file is not found!", ""

    # возвращаем результат вычислений
    try:
        name = names[int(results[0].boxes.cls[0])]
        if name in rus_names:
            res = rus_names[name]
            link = name_to_pdf[name]
        else:
            res = name
            link = ""
        return res, link
    except IndexError:  # если не найдено изображение
        return "не обнаружено", ""


@application.route("/check_img/", methods=["POST", "GET"])
def check_img():
    # получение файла из запроса и сохранение его
    if "file" in request.form:
        urllib.request.urlretrieve(request.form["file"], "tmp.png")
        pass
    else:
        request.files['file'].save("tmp.png")

    # сюда магию проверки картинки
    a, link = answer("./model/model_1.pt", "tmp.png")

    # для пк ответ содержит изображение, для телефона не нужно
    if request.headers.get('User-Agent').split()[1][1:-1].split()[0] == "Window":

        if True: # Сжатие изображения 
            img = Image.open("tmp.png")
            img_array = np.array(img)
            
            scale_percent = 60 # percent of original size
            width = int(img_array.shape[1] * scale_percent / 100)
            height = int(img_array.shape[0] * scale_percent / 100)
            dim = (width, height)
            print(f"{width=}, height{height=}, {dim=}")
            
            resized_image = cv2.resize(
                img_array, 
                dim, 
                interpolation = cv2.INTER_AREA
            )
            cv2.imwrite('tmp.png', cv2.cvtColor(resized_image, cv2.COLOR_RGB2BGR))

        # загрузка изображения
        pil_img = Image.open('tmp.png', mode='r')  # reads the PIL image
        byte_arr = io.BytesIO()
        pil_img.save(byte_arr, format='PNG')  # convert the PIL image to byte array
        encoded_img = encodebytes(byte_arr.getvalue()).decode('ascii')  # encode as base64

        return jsonify(type=a, img=encoded_img, link=link, successful_determination=link == "")
    else:
        return jsonify(type=a, link=link, successful_determination=link == "")


@application.route("/blueprint/<string:filename>/")
def get_pdf(filename):
    # возвращаем файл из библиотеки чертежей
    # /blueprint/CS150.01.427-01.pdf
    return send_file("static/blueprints/" + filename)


if __name__ == '__main__':
    application.run(host="0.0.0.0", port=5000)
