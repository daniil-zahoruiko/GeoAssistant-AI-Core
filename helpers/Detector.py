import torch
from torchvision import transforms
from ultralytics import YOLO
from model.SubModels import BollardNet

class SubModel:
    def __init__(self, model_class, imgsz, state_dict):
        self.imgsz = imgsz
        self.device = "cuda:0" if torch.cuda.is_available() else "cpu"
        
        self.model = model_class()
        self.model.load_state_dict(state_dict)
        self.model.to(self.device)

    def predict(self, img, coords):
        cropped_img = img.convert("RGB").crop(coords)
        cropped_img = cropped_img.resize(self.imgsz)
        tensor = transforms.ToTensor()(cropped_img)
        prediction = self.model(tensor.unsqueeze(0).to(self.device))
        return prediction.argmax(dim=1).cpu().tolist()[0]
    
class Detector:

    def __init__(self, file, mapping, model_config):
        CLASSIFICATION_MODEL_CLASSES = { "bollard": BollardNet }

        self.model = YOLO(file)
        self.device = "cuda:0" if torch.cuda.is_available() else "cpu"
        self.mapping = mapping

        self.classification_models = {}
        for model in model_config:
            self.classification_models[model['key']] = SubModel(CLASSIFICATION_MODEL_CLASSES[model['key']], tuple(model['size']), torch.load(model['path']))

        # Warm-up model
        self.model.predict(None, device=self.device)

    def bounding_boxes(self, img):
        res = self.model.predict(img, device=self.device, conf=0.7, imgsz=(1088, 1920))
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