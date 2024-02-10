import base64
import os
import cv2
import numpy as np
from flask import Flask, render_template, send_from_directory
from flask_socketio import SocketIO, emit
from ImageClassifier import ImageClassifier

app = Flask(__name__)
socketio = SocketIO(app)
imageClassifier = ImageClassifier("yolov5x6.pt")

@app.route("/", methods=["GET"])
def index():
    return render_template(
        "index.html",
        title="Homepage",
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
    # Decode the base64-encoded image data
    image = base64_to_image(image)

    # Image processing goes here
    image = imageClassifier.runDetection(image)
    print("done")

    #gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    frame_resized = cv2.resize(image, (640, 360))

    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]

    result, frame_encoded = cv2.imencode(".jpg", frame_resized, encode_param)

    processed_img_data = base64.b64encode(frame_encoded).decode()

    b64_src = "data:image/jpg;base64,"
    processed_img_data = b64_src + processed_img_data

    emit("processed_image", processed_img_data)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001)