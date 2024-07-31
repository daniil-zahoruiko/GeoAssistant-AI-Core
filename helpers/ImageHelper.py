from PIL import Image
import os

class ImageHelper:
    def save_image(self, img_file):
        PATH_TO_DIRECTORY = "images"  # path starting from the root of repo
        FILENAME = "img"    # base filename
        SIZE = (1024, 512)

        path = os.path.join(os.getcwd(), PATH_TO_DIRECTORY)
        if not os.path.exists(path):
            os.mkdir(path)

        filenames = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f)) and f[-3:] == "jpg" and f.startswith(FILENAME + '-') and f[len(FILENAME) + 1:-4].isnumeric()]
        numbers = [int(f[len(FILENAME) + 1:-4]) for f in filenames]
        number = 1
        if len(numbers) > 0:
            number = max(numbers) + 1

        img_path = os.path.join(path, FILENAME + '-' + str(number) + '.jpg')
        img_file.save(img_path)
        img = Image.open(img_path)
        resized_img = img.convert('RGB').resize(SIZE)
        resized_img.save(img_path)