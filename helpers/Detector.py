import torch
import torch.nn as nn
import torch.nn.functional as F
from torchvision import transforms
from ultralytics import YOLO
from model.SubModels import BollardNet

class SubModel:
    def __init__(self, imgsz, state_dict):
        self.imgsz = imgsz
        self.device = "cuda:0" if torch.cuda.is_available() else "cpu"
        self.model = torch.quantization.quantize_dynamic(BollardNet(), {nn.Linear}, dtype=torch.qint8)
        self.model.load_state_dict(state_dict)

    def predict(self, img, coords):
        cropped_img = img.convert("RGB").crop(coords)
        cropped_img = cropped_img.resize(self.imgsz)
        tensor = transforms.ToTensor()(cropped_img)
        prediction = F.softmax(self.model(tensor.unsqueeze(0)), dim=1)
        return prediction.argmax(dim=1).cpu().tolist()[0]
    
class Detector:

    def __init__(self, file, mapping, model_config):
        self.model = YOLO(file)
        self.device = "cuda:0" if torch.cuda.is_available() else "cpu"
        self.mapping = mapping

        self.classification_models = {}
        for model in model_config:
            self.classification_models[model['key']] = SubModel(tuple(model['size']), torch.load(model['path']))

        # Warm-up model
        self.model.predict(None, device=self.device)

    def bounding_boxes(self, img):
        res = self.model.predict(img, device=self.device, conf=0.5, imgsz=(1088, 1920))
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