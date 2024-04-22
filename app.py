# Python built-in packages
from pathlib import Path
import tempfile
# External packages
import streamlit as st
import cv2
from PIL import Image
# Local Modules
import configurations
import utilities

def setup_page():
    """
    Set up the Streamlit page configuration and load custom styles.
    """
    st.set_page_config(
        page_title="Object Recognition App",
        page_icon="🔍",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    load_custom_styles()

def load_custom_styles():
    """
    Load custom CSS styles for the Streamlit app.
    """
    with open("styles.css") as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

    st.markdown(
        """
        <style>
        .sidebar .sidebar-content {
            background: #000000;
        }
        .sidebar {
            width: 250px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

def display_header():
    """
    Display the header of the application.
    """
    st.title("Object Detection And Segmentation App")

def show_model_info():
    """
    Display information about model configuration and options.
    """
    st.header("Model Configuration")
    with st.expander("Help"):
        st.write("**Select Task**: Choose between object detection or segmentation.")
        st.write("**Select Model Confidence**: Adjust the confidence threshold for object detection. Higher values give more confident predictions.")
        st.write("**Select Model**: Choose a pre-trained model for the selected task. Models are sorted from least to most computationally expensive.")
        st.write('yolov8n: Smaller and faster model with relatively fewer parameters. Suitable for real-time applications with moderate accuracy.')
        st.write('yolov8s: Small-sized model optimized for speed. Sacrifices some accuracy for faster inference.')
        st.write('yolov8m: Medium-sized model offering a balance between speed and accuracy. Suitable for general-purpose object detection tasks.')
        st.write('yolov8l: Large-sized model with more parameters, providing higher accuracy but slower inference compared to smaller variants.')
        st.write('yolov8x: The largest model with the most parameters, offering the highest accuracy but slower inference speed.')

def select_model_and_confidence():
    """
    Select the model and confidence level for object detection or segmentation.
    """
    task = st.radio("Select Task", ['Detection', 'Segmentation'])
    confidence = float(st.slider("Select Model Confidence", min_value=0, max_value=100, value=40, step=1, format="%d%%")) / 100

    if task == 'Detection':
        model_name = st.selectbox("Select Model", configurations.DETECTION_MODEL_LIST)
        model_path = Path(configurations.MODEL_DIR, 'detection', str(model_name))
    elif task == 'Segmentation':
        model_name = st.selectbox("Select Model", configurations.SEGMENTATION_MODEL_LIST)
        model_path = Path(configurations.MODEL_DIR, 'segmentation', str(model_name))

    st.write("**Note:** Models are listed from less detailed and fastest to slowest and most detailed.")

    try:
        model = utilities.initialize_detector(model_path)
    except Exception as e:
        st.error(f"Unable to load model. Check the specified path: {model_path}")
        st.error(e)

    return model, confidence

def select_input_source():
    """
    Select the input source for object detection (image, video, or webcam).
    """
    st.header("Input Configuration")
    with st.expander("Help"):
        st.write("**Select Source**: Choose the input source for the detection task - image, video, or webcam.")

    source_type = st.radio("Select Source", configurations.MEDIA_TYPES)
    return source_type

def process_image_input(model, confidence):
    """
    Process image input for object detection.
    """
    col1, col2 = st.columns(2)

    with col1:
        image_file = st.sidebar.file_uploader("Choose an image...", type=("jpg", "jpeg", "png", 'bmp', 'webp'))
        if image_file:
            input_image = Image.open(image_file)
        else:
            input_image = Image.open(str(configurations.DEFAULT_IMAGE))
        st.image(input_image, caption="Input Image", use_column_width=True)

    with col2:
        if image_file:
            if st.sidebar.button('Detect Objects'):
                results = model.predict(input_image, conf=confidence)
                detected_image = results[0].plot()[:, :, ::-1]  # Convert from RGB to BGR
                st.image(detected_image, caption='Detected Image', use_column_width=True)
                display_detection_results(results)
        else:
            default_detected_image = Image.open(str(configurations.DEFAULT_DETECT_IMAGE))
            st.image(default_detected_image, caption='Detected Image', use_column_width=True)

def display_detection_results(results):
    """
    Display detection results.
    """
    try:
        with st.expander("Detection Results"):
            for box in results[0].boxes:
                st.write(box.data)
    except Exception as e:
        st.write("No detection results available.")

def process_video_input(model, confidence):
    """
    Process video input for object detection.
    """
    video_file = st.sidebar.file_uploader("Choose a video...", type=["mp4", "avi", "mov"])
    col1, col2 = st.columns(2)

    with col1:
        if video_file:
            st.video(video_file)
        else:
            st.video(str(configurations.DEFAULT_VIDEO))

    with col2:
        if video_file:
            if st.sidebar.button('Detect Objects'):
                temp_file = process_video_file(video_file)
                if temp_file:
                    detect_objects_in_video(model, confidence, temp_file)
        else:
            default_detect_video_path = str(configurations.DEFAULT_DETECT_VIDEO)
            st.video(default_detect_video_path, format='video/mp4', start_time=0)


def process_video_file(video_file):
    """
    Process video file.
    """
    try:
        temp_file = tempfile.NamedTemporaryFile(delete=False)
        temp_file.write(video_file.read())
        return temp_file.name
    except Exception as e:
        st.error("Error occurred while processing the video file.")
        st.error(e)
        return None

def detect_objects_in_video(model, confidence, video_path):
    """
    Perform object detection in a video.
    """
    vid_cap = cv2.VideoCapture(video_path)
    st_frame = st.empty()
    while vid_cap.isOpened():
        success, image = vid_cap.read()
        if success:
            utilities.show_detection_results(confidence, model, st_frame, image)
        else:
            vid_cap.release()
            break

def main():
    """
    Main function to run the application.
    """
    setup_page()
    display_header()
    show_model_info()

    model, confidence = select_model_and_confidence()
    source_type = select_input_source()

    if source_type == configurations.MEDIA_SOURCES['IMAGE']:
        process_image_input(model, confidence)
    elif source_type == configurations.MEDIA_SOURCES['VIDEO']:
        process_video_input(model, confidence)
    elif source_type == configurations.MEDIA_SOURCES['WEBCAM']:
        utilities.play_video(confidence, model, video_source="webcam")
    else:
        st.error("Please select a valid source type!")

if __name__ == '__main__':
    main()
