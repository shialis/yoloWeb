import tempfile
from ultralytics import YOLO
import streamlit as st
import cv2

import configurations

def load_model(model_path):
    """
    Loads a YOLO object detection model from the specified model_path.

    Parameters:
        model_path (str): The path to the YOLO model file.

    Returns:
        A YOLO object detection model.
    """
    model = YOLO(model_path)
    return model


def display_detected_frames(conf, model, st_frame, image):
    """
    Display the detected objects on a video frame using the YOLOv8 model.

    Args:
    - conf (float): Confidence threshold for object detection.
    - model (YoloV8): A YOLOv8 object detection model.
    - st_frame (Streamlit object): A Streamlit object to display the detected video.
    - image (numpy array): A numpy array representing the video frame.

    Returns:
    None
    """
    # Resize the image to a standard size
    image = cv2.resize(image, (720, int(720*(9/16))))

    # Predict the objects in the image using the YOLOv8 model
    res = model.predict(image, conf=conf)

    # Plot the detected objects on the video frame
    res_plotted = res[0].plot()
    st_frame.image(res_plotted,
                   caption='Detected Video',
                   channels="BGR",
                   use_column_width=True
                   )


def play_video(conf, model, video_source):
    """
    Plays a video stream from the specified video source.
    Detects Objects in real-time using the YOLOv8 object detection model.

    Parameters:
        conf: Confidence of YOLOv8 model.
        model: An instance of the `YOLOv8` class containing the YOLOv8 model.
        video_source: The video source (webcam or user-uploaded video file).

    Returns:
        None

    Raises:
        None
    """
    if video_source == "webcam":
        source = configurations.WEBCAM_PATH
    else:
        source = video_source

    try:
        vid_cap = cv2.VideoCapture(source)
        st_frame = st.empty()
        while vid_cap.isOpened():
            success, image = vid_cap.read()
            if success:
                display_detected_frames(conf, model, st_frame, image)
            else:
                vid_cap.release()
                break
    except Exception as e:
        st.sidebar.error(f"Error loading video: {str(e)}")


def main():
    # Load the YOLOv8 model
    model = load_model(configurations.DETECTION_MODELS['yolov8n'])

    # Set the confidence threshold
    conf = st.sidebar.slider("Confidence", min_value=0.0, max_value=1.0, value=0.5, step=0.1)

    # Select the video source
    video_source = st.sidebar.radio("Select Video Source", ("Webcam", "Upload Video"))

    if video_source == "Webcam":
        if st.sidebar.button('Detect Objects'):
            play_video(conf, model, "webcam")
    else:
        source_vid = st.sidebar.file_uploader("Choose a video...", type=["mp4", "avi", "mov"])
        if source_vid:
            st.video(source_vid)
            if st.sidebar.button('Detect Video Objects'):
                tfile = tempfile.NamedTemporaryFile(delete=False)
                tfile.write(source_vid.read())
                play_video(conf, model, tfile.name)

if __name__ == '__main__':
    main()