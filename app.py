from flask import Flask, request
from flask_cors import CORS, cross_origin
from flask_caching import Cache
from utils import fetch_image, save_image
import math

app = Flask(__name__)
app.config['CACHE_TYPE'] = 'SimpleCache'
cache = Cache(app)
CORS(app)

@app.route("/objects")
@cross_origin()
def get_image_objects():
    # TODO: Add screen width and screen height for panorama conversion (for now set by hand in utils)
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
    fetch_image((0, 0), boundaries, panoid, zoom, currentHeading - originHeading, currentPitch + originPitch, cache, (2560, 1271))
    return [], 200

@app.route("/imsave")
@cross_origin()
def imsave():
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
    img = fetch_image((0, 0), boundaries, panoid, zoom, currentHeading - originHeading, currentPitch + originPitch, cache)  # use default output size in fetch image here
    save_image(img)

    return [], 200

if __name__ == "__main__":
    app.run()