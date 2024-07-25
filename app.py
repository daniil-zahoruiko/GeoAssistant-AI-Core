from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from flask_caching import Cache
from helpers.Detector import Detector
from PIL import Image
import math
import os

app = Flask(__name__)
app.config['CACHE_TYPE'] = 'SimpleCache'
cache = Cache(app)
CORS(app)
detector = Detector(os.path.join(os.getcwd(), "model/best.pt"))

@app.route("/update", methods=["POST"])
@cross_origin()
def update():
    # TODO: check for the same bounding boxes with multiple files
    files = request.files
    res = []
    for file in files.keys():
        files[file].save(os.path.join(os.getcwd(), f'{file}.png'))
        img = Image.open(files[file])
        for boundingBox in detector.bounding_boxes(img):
            res.append(boundingBox)

    print(res)
    return jsonify(res), 200

@app.route("/imsave")
@cross_origin()
def imsave():
    """ Saves the panorama image

    Repsonses:
        200:
            description: Image fetched and saved successfully
    """
    # TODO: implement

    return [], 200

if __name__ == "__main__":
    app.run()