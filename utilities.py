import tempfile
from ultralytics import YOLO
import streamlit as st
import cv2

import configurations

def initialize_detector(detector_path):
    """
    Initialize the YOLO object detection model.

    Args:
        detector_path (str): Path to the YOLO model weights.

    Returns:
        YOLO: Initialized YOLO model.
    """
    return YOLO(detector_path)


def show_detection_results(confidence, detector, streamlit_frame, frame):
    """
    Show object detection results on the given frame.

    Args:
        confidence (float): Detection confidence threshold.
        detector (YOLO): YOLO object detection model.
        streamlit_frame: Streamlit frame for displaying the results.
        frame: Input frame for object detection.
    """
    # Adjust the frame size
    frame = cv2.resize(frame, (720, int(720 * (9 / 16))))

    # Use the detector to identify objects in the frame
    detection_results = detector.predict(frame, conf=confidence)

    # Display the results on the frame
    plotted_results = detection_results[0].plot()
    streamlit_frame.image(plotted_results,
                        caption='Detection Output',
                        channels="BGR",
                        use_column_width=True)


def play_video(confidence, model, video_source):
    """
    Play video and perform object detection on each frame.

    Args:
        confidence (float): Detection confidence threshold.
        model (YOLO): YOLO object detection model.
        video_source (str): Source of the video ('webcam' or file path).
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
                show_detection_results(confidence, model, st_frame, image)
            else:
                vid_cap.release()
                break
    except Exception as e:
        st.sidebar.error(f"Error loading video: {str(e)}")


def main():
    # Initialize the detector with a specific model
    detector = initialize_detector(configurations.DETECTION_MODELS['yolov8n'])

    # Allow user to set the detection confidence
    detection_confidence = st.sidebar.slider("Detection Confidence", min_value=0.0, max_value=1.0, value=0.5, step=0.1)

    # Option to choose between webcam and video upload
    video_choice = st.sidebar.radio("Choose Video Input", ("Webcam", "Upload Video"))

    if video_choice == "Webcam":
        if st.sidebar.button('Start Webcam Detection'):
            play_video(detection_confidence, detector, "webcam")
    else:
        uploaded_video = st.sidebar.file_uploader("Upload a video file", type=["mp4", "avi", "mov"])
        if uploaded_video:
            st.video(uploaded_video)
            if st.sidebar.button('Analyze Uploaded Video'):
                temp_file = tempfile.NamedTemporaryFile(delete=False)
                temp_file.write(uploaded_video.read())
                play_video(detection_confidence, detector, temp_file.name)

if __name__ == '__main__':
    main()
