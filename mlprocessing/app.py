import base64
import os
import cv2
import numpy as np
from flask import Flask, request, render_template, jsonify
from flask_socketio import SocketIO, emit
from joblib import load
import json

app = Flask(__name__)
socketio = SocketIO(app)
model = load("smoke_detection.joblib")


@app.route("/predict", methods=["POST"])
def predict():
    temperature = float(request.form.get("temperature"))
    humidity = float(request.form.get("humidity"))
    voc = float(request.form.get("voc"))
    co2 = float(request.form.get("co2"))
    airhpa = float(request.form.get("airhpa"))
    hydrogen = float(request.form.get("hydrogen"))

    data = [[temperature, humidity, voc, co2, hydrogen,
        19501.0, airhpa, 1.81, 1.88, 12.45,
        1.943, 0.044, 9336.0]]
    
    # 20.13
    # 50.15
    # 981.0
    # 400.0
    # 12924.0
    # 19501.0
    # 938.816
    # 1.81
    # 1.88
    # 12.45
    # 1.943
    # 0.044
    # 9336.0


    out = {"output": int(model.predict(data)[0])}
    return jsonify(out)

@app.route("/imageclassifier", methods=["GET"])
def classify():
    with open("../flask/yolov5/output.json") as json_file:
        data = json.load(json_file)
    return jsonify(data)

@app.route("/tryme.html", methods=["GET"])
def tryme():
    return render_template(
        "tryme.html",
        title="Try Me"
    )

@app.route("/", methods=["GET"])
def index():
    return render_template(
        "solution.html",
        title="Home",
    )
@app.route("/solution.html", methods=["GET"])
def solution():
    return render_template(
        "solution.html",
        title="Home",
    )
@app.route("/testai.html", methods=["GET"])
def testai():
    return render_template(
        "testai.html",
        title = "Documentation"
    )
@app.route("/features.html", methods=["GET"])
def features():
    return render_template(
        "features.html",
        title="Features",
    )

def base64_to_image(base64_string):
    # Extract the base64 encoded binary data from the input string
    base64_data = base64_string.split(",")[1]
    # Decode the base64 data to bytes
    image_bytes = base64.b64decode(base64_data)
    # Convert the bytes to numpy array
    image_array = np.frombuffer(image_bytes, dtype=np.uint8)
    # Decode the numpy array as an image using OpenCV
    image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
    
    return image


@socketio.on("connect")
def test_connect():
    print("Connected")
    emit("my response", {"data": "Connected"})


@socketio.on("image")
def receive_image(image):
    image = cv2.imread("../flask/output.png")

    frame_resized = cv2.resize(image, (640, 360))

    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]

    result, frame_encoded = cv2.imencode(".jpg", frame_resized, encode_param)

    processed_img_data = base64.b64encode(frame_encoded).decode()

    b64_src = "data:image/jpg;base64,"
    processed_img_data = b64_src + processed_img_data

    emit("processed_image", processed_img_data)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001)