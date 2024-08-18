import torch
from ultralytics import YOLO

class SubModel:
    def __init__(self, imgsz, model):
        self.imgsz = imgsz
        self.model = model
        self.device = "cuda:0" if torch.cuda.is_available() else "cpu"

        self.model.predict(None, device=self.device)

    def predict(self, img, coords):
        cropped_img = img.crop(coords)
        cropped_img.resize(self.imgsz)
        return self.model.predict(cropped_img, device=self.device, imgsz=self.imgsz)[0].probs.top1
    
class Detector:

    def __init__(self, file, mapping, model_config):
        self.model = YOLO(file)
        self.device = "cuda:0" if torch.cuda.is_available() else "cpu"
        self.mapping = mapping

        self.classification_models = {}
        for model in model_config:
            self.classification_models[model['key']] = SubModel(tuple(model['size']), YOLO(model['path']))

        # Warm-up model
        self.model.predict(None, device=self.device)

    def bounding_boxes(self, img):
        res = self.model.predict(img, device=self.device, conf=0.8, imgsz=(1088, 1920))
        boxes = []
        for box in res[0].boxes:
            cls = self.classification_models["bollard"].predict(img, box.xyxy.tolist()[0])
            map = [item for item in self.mapping if item["cls"] == str(cls)]
            boxes.append({  "cls": cls,
                            "name": map[0]["name"],
                            "description":map[0]["description"],
                            "coords": box.xyxy.tolist()[0]
                        })
        # print(boxes)
        # res[0].show()
        return boxes