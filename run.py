import io

from flask import Flask, render_template, request, json, jsonify
import config
import urllib.request
from PIL import Image
from base64 import encodebytes

application = Flask(__name__)
application.config.from_object(config)


@application.route("/")
def promotional_page():
    is_desktop = request.headers.get('User-Agent').split()[1][1:-1].split()[0] == "Window"
    print(is_desktop, request.headers.get('User-Agent'))
    return render_template('base.html', title="Обработка изображения", is_desktop=is_desktop)


def answer(weight_path:str, img_path: str) -> str:
    try:
        from ultralytics import YOLO
    except:
        return "No module YOLO! YOLO is not installed!"

    try:
        from PIL import Image
    except:
        return "No module Image! Image is not installed!"

    try:
        import numpy as np
    except:
        return "No module numpy! numpy is not installed!"

    try:
        import cv2
    except:
        return "No module cv2! cv2 is not installed!"


    img = Image.open(img_path)
    img_array = np.array(img)

    resized_image = cv2.resize(img_array, (640, 640))

    try:
        model = YOLO(weight_path)
    except:
        return "Weights file is not found!"

    results = model.predict(resized_image)
    names = model.names

    try:
        results = model.predict(resized_image)
        names = model.names

    except FileNotFoundError:
        return "Image file is not found!"

    finally:
        return names[int(results[0].boxes.cls[0])]


@application.route("/check_img", methods=["POST", "GET"])
def check_img():
    if "file" in request.form:
        urllib.request.urlretrieve(request.form["file"], "tmp.png")
    else:
        request.files['file'].save("tmp.png")
    # print(answer("C:\\2023\\Hacathon\\hak 22-24.09 web view\\model\\model_1.pt", "C:\\2023\\Hacathon\\hak 22-24.09 web view\\tmp.png"))

    # сюда магию проверки картинки

    response = application.response_class(
        response=json.dumps({"type": "RC101.01.01"}),
        status=300,
        mimetype='application/json'
    )
    pil_img = Image.open('tmp.png', mode='r')  # reads the PIL image
    byte_arr = io.BytesIO()
    pil_img.save(byte_arr, format='PNG')  # convert the PIL image to byte array
    encoded_img = encodebytes(byte_arr.getvalue()).decode('ascii')  # encode as base64
    # print(data)
    return jsonify(type="RC101.01.01", img=encoded_img)


@application.route("/test", methods=["POST", "GET"])
def test():
    print(request.form, 123)
    print(request.data, 321)
    print(request.files['file'].save("tmp.jpeg"), 221)
    return jsonify(type="RC101.01.01")


if __name__ == '__main__':
    application.run(host="localhost", port=8000)  # "192.168.43.33"
