# Real-time Object Detection and Tracking with YOLOv8 & Streamlit

This project focuses on both **object segmentation** and **detection**. It allows users to identify and outline objects within images and videos in real-time using advanced AI models like YOLOv8, all within a simple and intuitive interface powered by Streamlit.

## WebApp Demo on Streamlit Server

This app is up and running on Streamlit cloud server! You can check the demo of this web application on this link: [web app](https://yolov8-web.streamlit.app/)

## Demo

### Home page

<!-- Insert Home Page Screenshot here -->
<img width="1281" alt="homepageYOLO" src="https://github.com/shialis/yolov8-streamlit/assets/126681215/ff3296d5-0d4f-4afb-b966-26c74701299b">

### Image object detection

<!-- Insert Screenshot after object detection on image here -->
<img width="1281" alt="imagedemoYOLO" src="https://github.com/shialis/yolov8-streamlit/assets/126681215/123eb86b-4e0a-4c3e-87da-da96f66429ac">

### Segmentation task on image

<!-- Insert Segmentation Task Screenshot here -->
<img width="1281" alt="segdemoYOLO" src="https://github.com/shialis/yolov8-streamlit/assets/126681215/36b43cd8-9659-47d0-91db-8a921b24d849">

## Object Detection Video Demo

<!-- Insert Demo Video or GIF here -->
[videoDemoYOLO.webm](https://github.com/shialis/yolov8-streamlit/assets/126681215/127ba068-dfe7-4b8d-adcc-2dcc0fb15477)

## Requirements

- Python 3.6+
- YOLOv8 Models (Choose from 'yolov8n', 'yolov8s', 'yolov8m', 'yolov8l', 'yolov8x' for detection and 'yolov8n-seg', 'yolov8s-seg', 'yolov8m-seg', 'yolov8l-seg', 'yolov8x-seg' for segmentation)
- Have streamlit installed
  
```bash
pip install ultralytics streamlit

pip install requirements.txt

pip install streamlit
```


## Installation

1. Clone the repository: `[(https://github.com/shialis/yolov8-streamlit.git)]`
2. Add the ultralytics folder from the original yolov8 repository, to `/yolov8-streamlit`. That repository can be found [here]([https://github.com/ultralytics/ultralytics/tree/main/ultralytics])
3. Download the pre-trained YOLOv8 weights from [here]([https://docs.ultralytics.com/models/yolov8/#__tabbed_1_1])
 - You must download all Detection (coco) files, and place them in the `/weights/detection` directory, these are yolov8n.pt,..., yolov8x.pt
 - You must download all Segmentation (coco) files, and place them in the `/weights/segmentation` directory, 
   these are yolov8n-seg.pt,..., yolov8x-seg.pt

## Usage

1. Run the app with the following command: `streamlit run app.py`
2. The app should open in a new browser window.

### ML Model Config

- Select task (Detection, Segmentation)
- Select model confidence
- Select yolov8 model
- Use the slider to adjust the confidence threshold (0-100) for the model.

Once the model config is done, select a source. There are 3 options to choose from:
- Images
- Videos
- Webcam
  
## Detection on images

- A default image with its objects-detected image is displayed on the main page.
- Select yolov8 model
- Select a source ( button selection `Image`).
- Upload an image by clicking on the `Browse files` button.
- Click the `Detect Objects` button to run the object detection algorithm on the uploaded image with the selected confidence threshold.
- The resulting image with objects detected will be displayed on the page.

## Detection in Videos

- A default video with its objects-detected image is displayed on the main page.
- Select yolov8 model
- Upload a video by clicking on the `Browse files` button.
- Click the `Detect Objects` button to run the object detection algorithm on the uploaded video with the selected confidence threshold.
- The resulting video with objects detected will be displayed on the page.

## Detection on Webcam

- Click on the `Webcam` option to start real-time object detection from your webcam.

## Acknowledgements

This app uses [YOLOv8](https://github.com/ultralytics/ultralytics) for object detection algorithm and [Streamlit](https://github.com/streamlit/streamlit) library for the user interface.

### Disclaimer

Please note this project is intended for educational purposes only and should not be used in production environments.
