import torch
from ultralytics import YOLO

class Detector:
    def __init__(self, file):
        self.model = YOLO(file)
        self.device = "cuda:0" if torch.cuda.is_available() else "cpu" 
        print(self.device)

    def bounding_boxes(self, img):
        res = self.model.predict(img, device=self.device)
        boxes = []
        for box in res[0].boxes:
            boxes.append({"cls": box.cls.tolist(), "coords": box.xyxy.tolist()[0]})
        print(boxes)
        # res[0].show()
        return boxes