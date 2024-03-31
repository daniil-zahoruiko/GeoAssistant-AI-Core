from flask import Flask, request
from flask_cors import CORS, cross_origin
from utils import fetch_image

app = Flask(__name__)
CORS(app)

@app.route("/objects")
@cross_origin()
def get_image_objects():
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

    boundaries = (worldWidth / tileWidth, worldHeight / tileHeight)
    print("Boundaries: {bndrs}\npanoId: {pano}\nOrigin Heading: {oh}\Origin Pitch: {op}\nCurrent Heading: {ch}\nCurrent Pitch: {tw}\Zoom : {z}\n"
          .format(bndrs = boundaries, pano = panoid, oh = originHeading, op = originPitch, ch = currentHeading, cp = currentPitch, z = zoom  ))
    fetch_image((0, 0), boundaries, panoid, zoom)
    return [], 200


if __name__ == "__main__":
    app.run()