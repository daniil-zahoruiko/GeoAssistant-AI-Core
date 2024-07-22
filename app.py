from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from flask_caching import Cache
from helpers.ImageHelper import ImageHelper
from helpers.Detector import Detector
from PIL import Image
from w3lib.url import parse_data_uri
import math
import os
import io

app = Flask(__name__)
app.config['CACHE_TYPE'] = 'SimpleCache'
cache = Cache(app)
CORS(app)
imageHelper = ImageHelper()
detector = Detector(os.path.join(os.getcwd(), "model/best.pt"))

'''
@app.route("/objects")
@cross_origin()
def get_image_objects():
    """ Fetches the bounding boxes of detected objects on a panorama image

    Responses:
        200:
            description: Image fetched successfully
    """

    tileWidth = (int(request.args.get("tileWidth")))
    tileHeight = (int(request.args.get("tileHeight")))
    worldWidth = (int(request.args.get("worldWidth")))
    worldHeight = (int(request.args.get("worldHeight")))
    panoid = request.args.get("panoId")
    originHeading = (float(request.args.get("originHeading")))
    originPitch = (float(request.args.get("originPitch")))
    currentHeading = (float(request.args.get("currentHeading")))
    currentPitch = (float(request.args.get("currentPitch")))
    zoom = (int(request.args.get("zoom")))

    boundaries = (math.ceil(worldWidth / tileWidth / 2) - 1, math.ceil(worldHeight / tileHeight / 2) - 1)
    img = imageHelper.fetch_image((0, 0), boundaries, panoid, zoom, currentHeading - originHeading, currentPitch + originPitch, cache, (2560, 1271))
    boundingBoxes = detector.bounding_boxes(img)
    # print(jsonify(boundingBoxes))
    return jsonify(boundingBoxes), 200
'''

@app.route("/update", methods=["POST"])
@cross_origin()
def update():
    files = request.files
    for file in files.keys():
        print(file)
        files[file].save(os.path.join(os.getcwd(), f'{file}.png'))

    return [], 200

@app.route("/imsave")
@cross_origin()
def imsave():
    """ Saves the panorama image

    Repsonses:
        200:
            description: Image fetched and saved successfully
    """

    tileWidth = (int(request.args.get("tileWidth")))
    tileHeight = (int(request.args.get("tileHeight")))
    worldWidth = (int(request.args.get("worldWidth")))
    worldHeight = (int(request.args.get("worldHeight")))
    panoid = request.args.get("panoId")
    originHeading = (float(request.args.get("originHeading")))
    originPitch = (float(request.args.get("originPitch")))
    currentHeading = (float(request.args.get("currentHeading")))
    currentPitch = (float(request.args.get("currentPitch")))
    zoom = (int(request.args.get("zoom")))

    boundaries = (math.ceil(worldWidth / tileWidth / 2) - 1, math.ceil(worldHeight / tileHeight / 2) - 1)
    img = imageHelper.fetch_image((0, 0), boundaries, panoid, zoom, currentHeading - originHeading, currentPitch + originPitch, cache)  # use default output size in fetch image here
    imageHelper.save_image(img)

    return [], 200

if __name__ == "__main__":
    app.run()