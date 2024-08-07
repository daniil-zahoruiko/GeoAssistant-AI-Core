import torch
from ultralytics import YOLO

class Detector:
    def __init__(self, file, mapping):
        self.model = YOLO(file)
        self.device = "cuda:0" if torch.cuda.is_available() else "cpu"
        self.mapping = mapping

    def bounding_boxes(self, img):
        res = self.model.predict(img, device=self.device)
        boxes = []
        for box in res[0].boxes:
            map = [item for item in self.mapping if item["cls"] == str(int(box.cls.tolist()[0]))]
            boxes.append({  "cls": box.cls.tolist(),
                            "name": map[0]["name"],
                            "description":map[0]["description"],
                            "coords": box.xyxy.tolist()[0]
                        })
        # print(boxes)
        # res[0].show()
        return boxes