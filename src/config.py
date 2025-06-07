# src/config.py
# File cấu hình chung cho dự án YOLOv8

# Cấu hình mô hình
MODEL_NAME     = "yolov8n.pt"       # Tên model được pretrained (có thể chuyển sang yolov8s, yolov8m, yolov8l, yolov8x)
WEIGHTS_PATH   = "models/best.pt"   # Đường dẫn lưu weights tốt nhất sau huấn luyện

# Cấu hình dataset
SOURCE_ROOT    = "data/dataset"      # ← Nơi chứa dữ liệu gốc (đã chia)
DATA_ROOT      = "data/person-3"             # Thư mục gốc chứa dữ liệu images/ và labels/
DATA_YAML      = f"{DATA_ROOT}/data.yaml"   # Đường dẫn tới file YAML định nghĩa train/val
SPLIT_RATIO    = 0.2                          # Tỷ lệ validation (20%) và training (80%)

# Tham số huấn luyện
EPOCHS         = 30                   # Số epoch tối đa cho quá trình huấn luyện
BATCH_SIZE     = 16                   # Kích thước batch (giảm nếu thiếu GPU/CPU memory)
IMG_SIZE       = 640                  # Kích thước ảnh (pixel) dùng để train và infer
LEARNING_RATE  = 0.001                # Learning rate ban đầu (lr0)
LR_F           = 0.03                 # Tỉ lệ learning rate cuối (final lr = lr0 * lrf)
OPTIMIZER      = "AdamW"            # Optimizer: 'SGD' hoặc 'AdamW'

# Tham số augmentation
AUGMENT        = True                 # Bật tắt augmentation mặc định của YOLOv8
HSV_PARAMS     = {                     # Tham số augment màu sắc (HSV)
    "hsv_h": 0.05,                   # Độ thay đổi hue
    "hsv_s": 1.0,                    # Độ thay đổi saturation
    "hsv_v": 0.5                     # Độ thay đổi brightness (value)
}
TRANSFORM_PARAMS = {                   # Tham số biến đổi hình học
    "degrees": 10.0,                 # Góc xoay tối đa (độ)
    "shear": 3.0,                    # Góc shear tối đa (độ)
    "translate": 0.15,               # Tỷ lệ dịch chuyển tối đa (phần của ảnh)
    "scale": 0.5,                    # Tỷ lệ thay đổi kích thước tối đa
    "flipud": 0.2,                   # Xác suất lật dọc
    "fliplr": 0.5                    # Xác suất lật ngang
}
MOSAIC         = 0.8                  # Xác suất áp dụng mosaic augmentation
MIXUP          = 0.3                  # Xác suất áp dụng mixup augmentation
PATIENCE       = 20                   # Số epoch chờ khi không thấy cải thiện (early stopping)
CLOSE_MOSAIC   = 3                    # Epoch để tắt mosaic và chỉ fine-tune

# Cấu hình lưu kết quả
PROJECT_DIR    = "models"             # Thư mục chứa các run, logs và weights

# Cấu hình vùng cấm (polygon)
ZONE_PATH      = "zone.json"          # Đường dẫn tới file JSON chứa tọa độ polygon vùng cấm
POLYGON_POINTS = None                   # Biến lưu tọa độ polygon sau khi load từ ZONE_PATH