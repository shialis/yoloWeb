from pathlib import Path
import sys

# Get the absolute path of the current script
SCRIPT_PATH = Path(__file__).resolve()

# Get the parent directory of the current script
ROOT = SCRIPT_PATH.parent

# Add the root path to the sys.path list if it is not already there
if ROOT not in sys.path: 
    sys.path.append(str(ROOT))

# Get the relative path of the root directory with respect to the current working directory
ROOT_RELATIVE = ROOT.relative_to(Path.cwd())

# Define different media sources
MEDIA_SOURCES = {
    'IMAGE': 'Image',
    'VIDEO': 'Video',
    'WEBCAM': 'Webcam'
}
MEDIA_TYPES = list(MEDIA_SOURCES.values())

# Images configuration
IMAGES_DIR = ROOT / 'images'
DEFAULT_IMAGE = IMAGES_DIR / 'default_image.jpg'
DEFAULT_DETECT_IMAGE = IMAGES_DIR / 'default_image_detected.jpg'

# Videos configuration
VIDEO_DIR = ROOT / 'videos'
DEFAULT_VIDEO = VIDEO_DIR / 'default_video.mp4'
DEFAULT_DETECT_VIDEO = VIDEO_DIR / 'default_video_detected.mp4'

# Machine Learning Model configuration
MODEL_DIR = ROOT / 'weights'

# Detection models configuration
OBJ_DETECT_FOLDER = MODEL_DIR / 'detection'
DETECTION_MODELS = {
    'yolov8n': OBJ_DETECT_FOLDER / 'yolov8n.pt',
    'yolov8s': OBJ_DETECT_FOLDER / 'yolov8s.pt',
    'yolov8m': OBJ_DETECT_FOLDER / 'yolov8m.pt',
    'yolov8l': OBJ_DETECT_FOLDER / 'yolov8l.pt',
    'yolov8x': OBJ_DETECT_FOLDER / 'yolov8x.pt',
}
DETECTION_MODEL_LIST = list(DETECTION_MODELS.keys())

# Segmentation models configuration
SEGMENT_FOLDER = MODEL_DIR / 'segmentation'
SEGMENTATION_MODELS = {
    'yolov8n-seg': SEGMENT_FOLDER / 'yolov8n-seg.pt',
    'yolov8s-seg': SEGMENT_FOLDER / 'yolov8s-seg.pt',
    'yolov8m-seg': SEGMENT_FOLDER / 'yolov8m-seg.pt',
    'yolov8l-seg': SEGMENT_FOLDER / 'yolov8l-seg.pt',
    'yolov8x-seg': SEGMENT_FOLDER / 'yolov8x-seg.pt',
}
SEGMENTATION_MODEL_LIST = list(SEGMENTATION_MODELS.keys())

# Webcam configuration
WEBCAM_PATH = 0