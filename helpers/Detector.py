import torch
from torchvision import transforms
from ultralytics import YOLO
from model.SubModels import get_classification_model

class SubModel:
    def __init__(self, model_class, imgsz, state_dict, metadata):
        self.imgsz = imgsz
        self.metadata = metadata
        self.device = "cuda:0" if torch.cuda.is_available() else "cpu"

        self.model = model_class()
        self.model.load_state_dict(state_dict)
        self.model.to(self.device)

    def predict(self, img, coords):
        cropped_img = img.convert("RGB").crop(coords)
        cropped_img = cropped_img.resize(self.imgsz)
        tensor = transforms.ToTensor()(cropped_img)

        prediction = self.model(tensor.unsqueeze(0).to(self.device))
        res = prediction.argmax(dim=1).cpu().tolist()[0]
        metadata = self.metadata[str(res)]
        
        return { 
            'cls': res,
            'name': metadata['name'],
            'description': metadata['description']
        }
    
class Detector:

    def __init__(self, file, detection_mapping, classification_mapping, submodels_config):
        self.model = YOLO(file)
        self.device = "cuda:0" if torch.cuda.is_available() else "cpu"
        self.mapping = detection_mapping

        self.classification_models = {}
        for model in submodels_config:
            self.classification_models[model['key']] = SubModel(get_classification_model(model['key']), 
                                                                tuple(model['size']), 
                                                                torch.load(model['path']), 
                                                                classification_mapping[model['key']])

        # Warm-up model
        self.model.predict(None, device=self.device)

    def bounding_boxes(self, img):
        res = self.model.predict(img, device=self.device, conf=0.7, imgsz=(1088, 1920))
        boxes = []
        for box in res[0].boxes:
            res = self.classification_models[self.mapping[str(int(box.cls.tolist()[0]))]].predict(img, box.xyxy.tolist()[0])
            boxes.append({  "cls": res['cls'],
                            "name": res['name'],
                            "description":res['description'],
                            "coords": box.xyxy.tolist()[0]
                        })
        # print(boxes)
        # res[0].show()
        return boxes