import numpy as np
from PIL import Image
from io import BytesIO
import requests
import threading
from Equirectangular import Equirectangular
import matplotlib.image

URL = "https://streetviewpixels-pa.googleapis.com/v1/tile?cb_client=apiv3&panoid={}&output=tile&x={}&y={}&zoom={}&nbt=1&fover=2"

def worker(img, x, y, panoid, zoom):
    url = URL.format(panoid, x, y, zoom)
    response = requests.get(url)
    if response.status_code == 200:
        curr_img = Image.open(BytesIO(response.content))
        img[y * 512:(y + 1) * 512, x * 512:(x + 1) * 512, :] = np.array(curr_img, dtype=np.uint8)
    else:
        print(url)

def fetch_image(topleft, bottomright, panoId, zoom, heading, pitch, cache):
    img = cache.get(panoId)
    if img is None:
        height = bottomright[1] - topleft[1] + 1
        width = bottomright[0] - topleft[0] + 1
        img = np.zeros((height * 512, width * 512, 3), dtype=np.uint8)
        threads = []
        for i in range(height):
            for j in range(width):
                thread = threading.Thread(target=worker, args=(img, j, i, panoId, zoom))
                thread.start()
                threads.append(thread)
        print("threads started")
        for t in threads:
            t.join()
        if width / height != 2:
            img = img[:width / 2 - height, :, :] # trim the black rectangle at the bottom
        cache.set(panoId, img)
    equ = Equirectangular(img)
    matplotlib.image.imsave('img.jpg', equ.GetPerspective(120, heading, pitch, 1080, 1920))
    return img