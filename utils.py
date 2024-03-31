import numpy as np
from PIL import Image
from io import BytesIO
import requests
import matplotlib.pyplot as plt
import matplotlib.image
import threading

URL = "https://streetviewpixels-pa.googleapis.com/v1/tile?cb_client=apiv3&panoid={}&output=tile&x={}&y={}&zoom={}&nbt=1&fover=2"

def worker(img, x, y, panoid, zoom):
    url = URL.format(panoid, x, y, zoom)
    response = requests.get(url)
    if response.status_code == 200:
        curr_img = Image.open(BytesIO(response.content))
        img[y * 512:(y + 1) * 512, x * 512:(x + 1) * 512, :] = np.array(curr_img, dtype=np.uint8)
    else:
        print(url)

def fetch_image(topleft, bottomright, panoId, zoom):
    height = bottomright[1] - topleft[1] + 1
    width = bottomright[0] - topleft[0] + 1
    img = np.zeros((height * 512, width * 512, 3), dtype=np.uint8)
    threads = []
    for i in range(height):
        for j in range(width):
            thread = threading.Thread(target=worker, args=(img, j, i, panoId, zoom))
            thread.start()
            threads.append(thread)

    for t in threads:
        t.join()
    matplotlib.image.imsave('img.jpg', img)
    return img