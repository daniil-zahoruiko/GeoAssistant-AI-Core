import numpy as np
from PIL import Image
from io import BytesIO
import requests
import matplotlib.pyplot as plt
import matplotlib.image

URL = "https://streetviewpixels-pa.googleapis.com/v1/tile?cb_client=apiv3&panoid={}&output=tile&x={}&y={}&zoom={}&nbt=1&fover=2"

def fetch_image(topleft, bottomright, panoId, zoom):
    height = bottomright[1] - topleft[1] + 1
    width = bottomright[0] - topleft[0] + 1
    img = np.zeros((height * 512, width * 512, 3), dtype=np.uint8)
    print(height, width)
    for i in range(height):
        for j in range(width):
            url = URL.format(panoId, topleft[0] + j, topleft[1] + i, zoom)
            response = requests.get(url)
            if response.status_code == 200:
                curr_img = Image.open(BytesIO(response.content))
                img[i * 512:(i + 1) * 512, j * 512:(j + 1) * 512, :] = np.array(curr_img, dtype=np.uint8)
            else:
                print(url)
    matplotlib.image.imsave('img.jpg', img)
    return img