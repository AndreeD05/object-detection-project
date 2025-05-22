# Định nghĩa các đường dẫn và thông số dùng chung
MODEL_NAME     = "yolov8n.pt"
WEIGHTS_PATH   = "models/best.pt"
DATA_ROOT      = "data/dataset"             # nơi có images/ và labels/
DATA_YAML      = f"{DATA_ROOT}/data.yaml"
SPLIT_RATIO    = 0.2                        # 20% val, 80% train
EPOCHS         = 30
BATCH_SIZE     = 16
IMG_SIZE       = 640
LEARNING_RATE  = 0.005
PROJECT_DIR    = "models"
POLYGON_POINTS = [
    [435, 1079],
    [1022, 521],
    [612, 346],
    [56, 855]
]
