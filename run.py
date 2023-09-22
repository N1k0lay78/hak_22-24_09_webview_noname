from flask import Flask, render_template, request, json, jsonify
import config
import urllib.request
from PIL import Image

application = Flask(__name__)
application.config.from_object(config)


@application.route("/")
def promotional_page():
    is_desktop = request.headers.get('User-Agent').split()[1][1:-1].split()[0] == "Window"
    print(is_desktop, request.headers.get('User-Agent'))
    return render_template('base.html', title="Обработка изображения", is_desktop=is_desktop)


@application.route("/check_img", methods=["POST", "GET"])
def check_img():
    urllib.request.urlretrieve(request.form["file"], "tmp.png")
    img = Image.open("tmp.png")

    # сюда магию проверки картинки

    response = application.response_class(
        response=json.dumps({"type": "RC101.01.01"}),
        status=300,
        mimetype='application/json'
    )
    return jsonify(type="RC101.01.01")


if __name__ == '__main__':
    application.run(host="localhost", port=8000)  # "192.168.43.33"
