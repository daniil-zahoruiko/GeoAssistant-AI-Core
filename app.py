from flask import Flask, request, jsonify, current_app as app
from flask_cors import CORS, cross_origin
from helpers.Detector import Detector
from helpers.ImageHelper import ImageHelper
from helpers.JSONLoader import JSONLoader
from PIL import Image
import os

app = Flask(__name__)
CORS(app)

CLASSIFICATION_MAPPING_FILE_PATH = os.path.join(app.static_folder, 'classification_mapping.json')
DETECTION_MAPPING_FILE_PATH = os.path.join(app.static_folder, 'detection_mapping.json')
SUBMODELS_CONFIG_PATH = os.path.join(app.static_folder, 'submodels_cfg.json')

CLASSIFICATION_MAPPING = JSONLoader.load(CLASSIFICATION_MAPPING_FILE_PATH)
DETECTION_MAPPING = JSONLoader.load(DETECTION_MAPPING_FILE_PATH)
SUBMODELS_CONFIG = JSONLoader.load(SUBMODELS_CONFIG_PATH)

detector = Detector(os.path.join(os.getcwd(), "model/best.pt"), DETECTION_MAPPING, CLASSIFICATION_MAPPING, SUBMODELS_CONFIG)
image_helper = ImageHelper()

@app.route("/update", methods=["POST"])
@cross_origin()
def update():
    files = request.files
    res = []
    for file in files.keys():
        # files[file].save(os.path.join(os.getcwd(), f'{file}.png'))
        img = Image.open(files[file])
        res.append(detector.bounding_boxes(img))
    
    print(res)
    return jsonify(res), 200

@app.route("/imsave", methods=["POST"])
@cross_origin()
def imsave():
    """ Saves the panorama image

    Repsonses:
        200:
            description: Image fetched and saved successfully
    """
    files = request.files
    for file in files.keys():
        image_helper.save_image(files[file])

    return [], 200

if __name__ == "__main__":
    app.run()