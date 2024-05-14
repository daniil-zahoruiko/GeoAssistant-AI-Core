import numpy as np
from PIL import Image
from io import BytesIO
import requests
import threading
from scipy.ndimage import map_coordinates

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
            img = img[:int(width * 256), :, :] # trim the black rectangle at the bottom
        cache.set(panoId, img)
    # imageio.imsave('img.jpg', panorama_to_plane(img, 127, (2560, 1271), heading - 90, 90 - pitch))
    perspective = panorama_to_plane(img, 127, (2560, 1271), heading - 90, 90 - pitch)
    return perspective

def map_to_sphere(x, y, z, yaw_radian, pitch_radian):


    theta = np.arccos(z / np.sqrt(x ** 2 + y ** 2 + z ** 2))
    phi = np.arctan2(y, x)

    # Apply rotation transformations here
    theta_prime = np.arccos(np.sin(theta) * np.sin(phi) * np.sin(pitch_radian) +
                            np.cos(theta) * np.cos(pitch_radian))

    phi_prime = np.arctan2(np.sin(theta) * np.sin(phi) * np.cos(pitch_radian) -
                           np.cos(theta) * np.sin(pitch_radian),
                           np.sin(theta) * np.cos(phi))
    phi_prime += yaw_radian
    phi_prime = phi_prime % (2 * np.pi)

    return theta_prime.flatten(), phi_prime.flatten()


def interpolate_color(coords, img, method='bilinear'):
    order = {'nearest': 0, 'bilinear': 1, 'bicubic': 3}.get(method, 1)
    red = map_coordinates(img[:, :, 0], coords, order=order, mode='reflect')
    green = map_coordinates(img[:, :, 1], coords, order=order, mode='reflect')
    blue = map_coordinates(img[:, :, 2], coords, order=order, mode='reflect')
    return np.stack((red, green, blue), axis=-1)


def panorama_to_plane(panorama, FOV, output_size, yaw, pitch):
    pano_height, pano_width, _ = panorama.shape
    yaw_radian = np.radians(yaw)
    pitch_radian = np.radians(pitch)

    W, H = output_size
    f = (0.5 * W) / np.tan(np.radians(FOV) / 2)

    u, v = np.meshgrid(np.arange(W), np.arange(H), indexing='xy')

    x = u - W / 2
    y = H / 2 - v
    z = f

    theta, phi = map_to_sphere(x, y, z, yaw_radian, pitch_radian)

    U = phi * pano_width / (2 * np.pi)
    V = theta * pano_height / np.pi

    U, V = U.flatten(), V.flatten()
    coords = np.vstack((V, U))

    colors = interpolate_color(coords, panorama)
    output_image = Image.fromarray(colors.reshape((H, W, 3)).astype('uint8'), 'RGB')

    return output_image