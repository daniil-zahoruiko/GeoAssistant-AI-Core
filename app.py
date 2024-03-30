from flask import Flask, request
from flask_cors import CORS, cross_origin
from utils import fetch_image

app = Flask(__name__)
CORS(app)

@app.route("/objects")
@cross_origin()
def get_image_objects():
    topleft = (int(request.args.get("topleftx")), int(request.args.get("toplefty")))
    bottomright = (int(request.args.get("bottomrightx")), int(request.args.get("bottomrighty")))
    print(topleft, bottomright)
    panoid = request.args.get("panoId")
    zoom = request.args.get("zoom")
    fetch_image(topleft, bottomright, panoid, zoom)
    return [], 200


if __name__ == "__main__":
    app.run()