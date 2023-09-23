import io
from flask import Flask, render_template, request, json, jsonify
import config
import urllib.request
from PIL import Image
from base64 import encodebytes
from ultralytics import YOLO
import numpy as np
import cv2

application = Flask(__name__)
application.config.from_object(config)


@application.route("/")
def promotional_page():
    is_desktop = request.headers.get('User-Agent').split()[1][1:-1].split()[0] == "Window"
    print(is_desktop, request.headers.get('User-Agent'))
    return render_template('base.html', title="Обработка изображения", is_desktop=is_desktop)


def answer(weight_path: str, img_path: str) -> str:
    img = Image.open(img_path)
    img_array = np.array(img)

    resized_image = cv2.resize(img_array, (640, 640))

    # gray_image = cv2.cvtColor(resized_image, cv2.COLOR_BGR2GRAY)

    try:
        model = YOLO(weight_path)
    except:
        return "Weights file is not found!"

    try:
        results = model.predict(resized_image)
        names = model.names
    except FileNotFoundError:
        return "Image file is not found!"

    try:
        rus_names = {
            'CS120.01.413': 'CS120.01.413',
            'CS120.07.442': 'CS120.07.442',
            'CS150.01.427-01': 'CS150.01.427-01',
            'SU80.01.426': 'SU80.01.426',
            'SU80.10.409A': 'SU80.10.409A',
            'SU160.00.404': 'SU160.00.404',
            '3BT86_103K_02': 'ЗВТ86.103К-02',
            'SBM_37_060': 'СВМ.37.060',
            'SVM.37.060A': 'СВМ.37.060А',
            'SVP_120_00_060': 'СВП-120.00.060',
            'SVP120_42_020': 'СВП120.42.020',
            'SVP120_42_030': 'СВП120.42.030',
            'SK_20_01_01_01_406': 'СК20.01.01.01.406',
            'SK_20_01_01_02_402': 'СК20.01.01.02.402',
            'SK30.01.01.02.402': 'СК30.01.01.02.402',
            'SK30_01_01_03_403': 'СК30.01.01.03.403',
            'SK_50_01_01_404': 'СК50.01.01.404',
            'SK_50_02_01_411': 'СК50.02.01.411',
            'SPO_250_14_190': 'СПО250.14.190',
            '-.37.060': 'СВМ.37.060',
            '-.37.060-': 'СВМ.37.060А',
            '-120.00.060': 'СВП-120.00.060',
            '-120.42.020': 'СВП120.42.020',
            '-120.42.030': 'СВП120.42.030',
            '-20.01.01.01.406': 'СК20.01.01.01.406',
            '-20.01.01.02.402': 'СК20.01.01.02.402',
            '-250.14.190': 'СПО250.14.190',
            '-30.01.01.02.402': 'СК30.01.01.02.402',
            '-30.01.01.03.403': 'СК30.01.01.03.403',
            '-50.01.01.404': 'СК50.01.01.404',
            '-50.02.01.411': 'СК50.02.01.411',
            '-86.103-02': 'ЗВТ86.103К-02',
        }
        name = names[int(results[0].boxes.cls[0])]
        if name in rus_names:
            res = rus_names[name]
        else:
            res = name
        return res
    except IndexError:
        return "не обнаружено"


@application.route("/check_img", methods=["POST", "GET"])
def check_img():
    if "file" in request.form:
        urllib.request.urlretrieve(request.form["file"], "tmp.png")
    else:
        request.files['file'].save("tmp.png")

    if True:  # Сжатие изображение ДЕЛАЕТ ЕГО СИНИМ
        img = Image.open("tmp.png")
        img_array = np.array(img)
        resized_image = cv2.resize(img_array, (640, 640))
        cv2.imwrite(f'tmp.png', resized_image)

    # сюда магию проверки картинки
    a = answer("model\\model_1.pt", "tmp.png")

    pil_img = Image.open('tmp.png', mode='r')  # reads the PIL image
    byte_arr = io.BytesIO()
    pil_img.save(byte_arr, format='PNG')  # convert the PIL image to byte array
    encoded_img = encodebytes(byte_arr.getvalue()).decode('ascii')  # encode as base64
    return jsonify(type=a, img=encoded_img)


@application.route("/test", methods=["POST", "GET"])
def test():
    print(request.form, 123)
    print(request.data, 321)
    print(request.files['file'].save("tmp.jpeg"), 221)
    return jsonify(type="RC101.01.01")


if __name__ == '__main__':
    application.run(host="localhost", port=8000)  # "192.168.43.33"
