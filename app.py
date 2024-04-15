# Python In-built packages
from pathlib import Path
import PIL
import cv2
import tempfile
# External packages
import streamlit as st
import PIL
# Local Modules
import configurations
import utilities

def set_page_config():
    st.set_page_config(
        page_title="Object Recognition with YOLOv8",
        page_icon="🔍",
        layout="wide",
        initial_sidebar_state="expanded"
    )

def load_custom_css():
    with open("styles.css") as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def set_sidebar_style():
    # Set the sidebar's background color to black
    st.markdown(
        """
        <style>
        .sidebar .sidebar-content {
            background: #000000;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Set the sidebar's width to 250px
    st.markdown(
        """
        <style>
        .sidebar {
            width: 250px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

def display_title():
    st.title("Object Detection And Tracking using YOLOv8")

def display_configurations():
    st.header("ML Model Config")
    with st.expander("Help"):
        st.write("**Select Task**: Choose whether you want to perform object detection or segmentation.")
        st.write("**Select Model Confidence**: Adjust the confidence threshold for detecting objects. Higher values lead to more confident predictions.")
        st.write("**Select Model**: Choose the pre-trained model to use for the selected task.")
        st.write('yolov8n: A smaller and faster variant of YOLOv8 with relatively fewer parameters. Suitable for real-time applications with moderate accuracy.')
        st.write('yolov8s: - A small-sized variant optimized for speed. It sacrifices some accuracy for faster inference.')
        st.write('yolov8m: - A medium-sized variant offering a balance between speed and accuracy. Suitable for general-purpose object detection tasks.')
        st.write('yolov8l: - A large-sized variant with more parameters, providing higher accuracy but slower inference compared to smaller variants.')
        st.write('yolov8x: - The largest variant with the most parameters, offering the highest accuracy but slower inference speed.')

def select_model():
    model_type = st.radio("Select Task", ['Detection', 'Segmentation'])
    confidence = float(st.slider("Select Model Confidence", min_value=0, max_value=100, value=40, step=1, format="%d%%", help="Recommended range: 30-60")) / 100

    if model_type == 'Detection':
        model_type = st.selectbox("Select Model", configurations.DETECTION_MODEL_LIST)
        model_path = Path(configurations.MODEL_DIR, 'detection', str(model_type))
    elif model_type == 'Segmentation':
        model_type = st.selectbox("Select Model", configurations.SEGMENTATION_MODEL_LIST)
        model_path = Path(configurations.MODEL_DIR, 'segmentation', str(model_type))

    st.write("**Note:** Models are listed from less detailed and fastest to slowest and most detailed.")

    try:
        model = utilities.load_model(model_path)
    except Exception as ex:
        st.error(f"Unable to load model. Check the specified path: {model_path}")
        st.error(ex)

    return model, confidence

def select_source():
    st.header("Image/Video Config")
    with st.expander("Help"):
        st.write("**Select Source**: Choose the input source for the detection task - image, video, or webcam.")

    source_radio = st.radio("Select Source", configurations.SOURCES_LIST)
    return source_radio

def process_image(model, confidence):
    col1, col2 = st.columns(2)

    with col1:
        source_img = st.sidebar.file_uploader("Choose an image...", type=("jpg", "jpeg", "png", 'bmp', 'webp'))
        try:
            if source_img is None:
                default_image_path = str(configurations.DEFAULT_IMAGE) 
                default_image = PIL.Image.open(default_image_path)
                st.image(default_image, caption="Default Image", use_column_width=True)
            else:
                uploaded_image = PIL.Image.open(source_img)
                st.image(uploaded_image, caption="Uploaded Image", use_column_width=True)
        except Exception as ex:
            st.error("Error occurred while opening the image.")
            st.error(ex)

    with col2:
        try:
            if source_img is None:
                default_detected_image_path = str(configurations.DEFAULT_DETECT_IMAGE)
                default_detected_image = PIL.Image.open(default_detected_image_path)
                st.image(default_detected_image, caption='Detected Image', use_column_width=True)
            else:
                if st.sidebar.button('Detect Objects'):
                    res = model.predict(uploaded_image, conf=confidence)
                    boxes = res[0].boxes
                    res_plotted = res[0].plot()[:, :, ::-1]
                    st.image(res_plotted, caption='Detected Image', use_column_width=True)
                    try:
                        with st.expander("Detection Results"):
                            for box in boxes:
                                st.write(box.data)
                    except Exception as ex:
                        st.write("No image is uploaded yet!")
        except Exception as ex:
            st.error("Error occurred while processing the image.")
            st.error(ex)

def process_video(model, confidence):
    #st.markdown('<style>div.row-widget.stFileUploader>div{width:100% !important;}</style>', unsafe_allow_html=True)

    source_vid = st.sidebar.file_uploader("Choose a video...", type=["mp4", "avi", "mov"])
    col1, col2 = st.columns(2)

    with col1:
        try:
            if source_vid is None:
                default_video_path = str(configurations.DEFAULT_VIDEO)
                st.video(default_video_path, format='video/mp4', start_time=0)
            else:
                st.video(source_vid)
        except Exception as ex:
            st.error("Error occurred while opening the video.")
            st.error(ex)

    with col2:
        try:
            if source_vid is None:
                default_detect_video_path = str(configurations.DEFAULT_DETECT_VIDEO)
                st.video(default_detect_video_path, format='video/mp4', start_time=0)
            else:
                if st.sidebar.button('Detect Objects'):
                    tfile = tempfile.NamedTemporaryFile(delete=False)
                    tfile.write(source_vid.read())
                    vid_cap = cv2.VideoCapture(tfile.name)

                    st_frame = st.empty()
                    while vid_cap.isOpened():
                        success, image = vid_cap.read()
                        if success:
                            utilities.display_detected_frames(confidence, model, st_frame, image)
                        else:
                            vid_cap.release()
                            tfile.close()
                            break
        except Exception as ex:
            st.error("Error occurred while processing the video.")
            st.error(ex)
            
def main():

    set_page_config()
    load_custom_css()
    display_title()
    display_configurations()

    model, confidence = select_model()
    source_radio = select_source()

    if source_radio == configurations.IMAGE:
        process_image(model, confidence)
    elif source_radio == configurations.VIDEO:
        process_video(model, confidence)
    elif source_radio == configurations.WEBCAM:
        utilities.play_video(confidence, model, video_source="webcam")
    else:
        st.error("Please select a valid source type!")

if __name__ == '__main__':
    main()