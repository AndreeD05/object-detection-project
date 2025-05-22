# src/config.py
# Định nghĩa các đường dẫn và thông số dùng chung

# Model
MODEL_NAME     = "yolov8n.pt"              # Pretrained model name
WEIGHTS_PATH   = "models/best.pt"           # Path to saved weights after training

# Dataset
DATA_ROOT      = "data/dataset"             # Root folder containing images/ and labels/
DATA_YAML      = f"{DATA_ROOT}/data.yaml"   # YOLOv8 config file
SPLIT_RATIO    = 0.2                        # Fraction for validation (20% val, 80% train)

# Training hyperparameters
EPOCHS         = 30                         # Number of training epochs
BATCH_SIZE     = 16                         # Batch size
IMG_SIZE       = 640                        # Image size for training
LEARNING_RATE  = 0.005                      # Initial learning rate
LR_F           = 0.1                        # Final learning rate fraction (lrf)
OPTIMIZER      = "SGD"                     # Optimizer: SGD or Adam

# Augmentation parameters
AUGMENT        = True                       # Whether to enable automatic augmentations
HSV_PARAMS     = {                           
    "hsv_h": 0.015,                        # HSV hue augmentation
    "hsv_s": 0.7,                         # HSV saturation augmentation
    "hsv_v": 0.4                          # HSV value augmentation
}
TRANSFORM_PARAMS = {
    "degrees": 5.0,                       # Rotation degrees
    "shear": 2.0,                         # Shear angle
    "translate": 0.1,                     # Translation fraction
    "scale": 0.5,                         # Scale variation
    "flipud": 0.0,                        # Vertical flip probability
    "fliplr": 0.5                         # Horizontal flip probability
}
MOSAIC         = 1.0                        # Mosaic augmentation strength
MIXUP          = 0.2                        # Mixup augmentation strength
PATIENCE       = 10                         # Early stopping patience
CLOSE_MOSAIC   = 10                         # Epoch to stop mosaic before end

# Project
PROJECT_DIR    = "models"                  # Directory to save training outputs

# Restricted zone polygon (x, y) points
POLYGON_POINTS = [
    [435, 1079],
    [1022, 521],
    [612, 346],
    [56, 855]
]
