# src/config.py
# Định nghĩa các đường dẫn và thông số dùng chung

# Model
MODEL_NAME     = "yolov8s.pt"             # Đổi sang mô hình small để thử nghiệm
WEIGHTS_PATH   = "models/best.pt"

# Dataset
DATA_ROOT      = "data/dataset"
DATA_YAML      = f"{DATA_ROOT}/data.yaml"
SPLIT_RATIO    = 0.2

# Training hyperparameters
EPOCHS         = 30                        # Số epoch
BATCH_SIZE     = 16                        # Batch size (giảm nếu GPU nhỏ)
IMG_SIZE       = 640                       # Kích thước ảnh
LEARNING_RATE  = 0.001                     # Giữ LR ban đầu
LR_F           = 0.03                      # LR cuối cho cosine-annealing
SCHEDULER      = "cosine"                 # Thêm biến scheduler để sử dụng cosine-annealing
OPTIMIZER      = "AdamW"                  # Optimizer

# Augmentation parameters
AUGMENT        = True                      # Bật augmentation
HSV_PARAMS     = {
    "hsv_h": 0.05,                       # Tăng hue
    "hsv_s": 1.0,                        # Tăng saturation
    "hsv_v": 0.5                         # Tăng value
}
TRANSFORM_PARAMS = {
    "degrees": 10.0,                     # Rotation
    "shear": 3.0,                        # Shear
    "translate": 0.15,                   # Translation
    "scale": 0.5,                        # Scale
    "flipud": 0.2,                       # Vertical flip
    "fliplr": 0.5                        # Horizontal flip
}
MOSAIC         = 0.8                       # Xác suất mosaic
MIXUP          = 0.3                       # Xác suất mixup
PATIENCE       = 20                        # EarlyStopping patience
CLOSE_MOSAIC   = 3                         # Tắt mosaic sau epoch 3

# Project
PROJECT_DIR    = "models"                 # Thư mục lưu kết quả

# Restricted zone polygon (x, y) points
ZONE_PATH      = "zone.json"
POLYGON_POINTS = None
