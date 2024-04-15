from pathlib import Path
import sys

# Get the absolute path of the current file
FILE = Path(__file__).resolve()
# Get the parent directory of the current file
ROOT = FILE.parent
# Add the root path to the sys.path list if it is not already there
if ROOT not in sys.path:
    sys.path.append(str(ROOT))
# Get the relative path of the root directory with respect to the current working directory
ROOT = ROOT.relative_to(Path.cwd())

# Sources
IMAGE = 'Image'
VIDEO = 'Video'
WEBCAM = 'Webcam'
SOURCES_LIST = [IMAGE, VIDEO, WEBCAM]

# Images config
IMAGES_DIR = ROOT / 'images'
DEFAULT_IMAGE = IMAGES_DIR / 'default_image.jpg'
DEFAULT_DETECT_IMAGE = IMAGES_DIR / 'default_image_detected.jpg'

# Videos config
VIDEO_DIR = ROOT / 'videos'
DEFAULT_VIDEO = VIDEO_DIR / 'default_video.mp4'
DEFAULT_DETECT_VIDEO = VIDEO_DIR / 'default_video_detected.mp4'
VIDEOS_DICT = {
    'video_1': VIDEO_DIR / 'video_1.mp4',
    'video_2': VIDEO_DIR / 'video_2.mp4',
    'video_3': VIDEO_DIR / 'video_3.mp4',
}

# ML Model config
MODEL_DIR = ROOT / 'weights'

# Detection models
DETECTION_MODEL_DIR = MODEL_DIR / 'detection'
DETECTION_MODELS = {
    'yolov8n': DETECTION_MODEL_DIR / 'yolov8n.pt',
    'yolov8s': DETECTION_MODEL_DIR / 'yolov8s.pt',
    'yolov8m': DETECTION_MODEL_DIR / 'yolov8m.pt',
    'yolov8l': DETECTION_MODEL_DIR / 'yolov8l.pt',
    'yolov8x': DETECTION_MODEL_DIR / 'yolov8x.pt',
}
DETECTION_MODEL_LIST = list(DETECTION_MODELS.keys())

# Segmentation models
SEGMENTATION_MODEL_DIR = MODEL_DIR / 'segmentation'
SEGMENTATION_MODELS = {
    'yolov8n-seg': SEGMENTATION_MODEL_DIR / 'yolov8n-seg.pt',
    'yolov8s-seg': SEGMENTATION_MODEL_DIR / 'yolov8s-seg.pt',
    'yolov8m-seg': SEGMENTATION_MODEL_DIR / 'yolov8m-seg.pt',
    'yolov8l-seg': SEGMENTATION_MODEL_DIR / 'yolov8l-seg.pt',
    'yolov8x-seg': SEGMENTATION_MODEL_DIR / 'yolov8x-seg.pt',
}
SEGMENTATION_MODEL_LIST = list(SEGMENTATION_MODELS.keys())

# Webcam
WEBCAM_PATH = 0