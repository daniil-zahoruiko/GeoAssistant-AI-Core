<p align="center">
  <img width="70%" src="./readme_helpers/logo.svg">
</p>
<p>
  <img src="https://img.shields.io/badge/release-v1.0.0-blue?style=flat-square"/>
  <img src="https://img.shields.io/badge/release_date-september_2024-979621?style=flat-square"/>
  <img src="https://img.shields.io/badge/license-CC_BY_NC_SA_4.0-red?style=flat-square"/>
  <img src="https://img.shields.io/badge/Jupyter-Notebook-red?logo=jupyter&style=flat-square"/>
  <img src="https://img.shields.io/badge/Server-Flask-yellow?logo=flask&style=flat-square"/>
  <img src="https://img.shields.io/badge/Made_with-YOLOv8-blue?style=flat-square"/>
</p>

<p>
   Back-end server of <a href="https://github.com/daniil-zahoruiko/GeoAssistant-AI-Extension">GeoAssistant AI Extension</a> with core computations and Machine Learning models.
</p>

<h1 align="center">Documentation</h1>

We use the YOLOv8 pose model to detect general object categories, such as bollards. Given that YOLO’s classification performance on small objects has not been the best, we further process the detected objects using a ResNet model, implemented in PyTorch, to classify them based on country-specific categories. In this workflow, the YOLO model classifies the object as "bollard", while the ResNet model handles the country-level classification.

Our repository provides trained models; however, the dataset is not publicly available. If you wish to train the models on your own dataset, please refer to `build_model.ipynb`, which contains the necessary training scripts. This notebook allows you to use your own data by simply adjusting the file paths in the training functions. Although it includes a script to download data from an AWS S3 bucket, this is optional if your data is already locally available. Additionally, the notebook offers a script to convert standard YOLO annotations into YOLO pose annotations. If your annotations are in the standard YOLO format, this conversion is required to use the pose model.

<h1 align="center">Supported countries</h1>

- France
  * Red bollards
  * Grey bollards
- Italy
  * Bollards
- Guatemala, Dominican Republic, Curacao, Kyrgyzstan, Mongolia, Ghana, Senegal
  * Google Car Roof Rack

<h1 align="center">Technologies used</h1>

- **<a href="https://pytorch.org/docs/stable/index.html">PyTorch</a>**
- **<a href="https://github.com/ultralytics/ultralytics">YOLOv8</a>**
- **ResNet**
- **Python**

<h1 align="center">Contributions</h1>
App was created by Daniil Zahoruiko, University of Alberta student, and Dmytro Avdieienko, University of Southampton student, where each contributed in all sections of development.
