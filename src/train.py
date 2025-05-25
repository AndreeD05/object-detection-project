# src/train.py
import os
import yaml
import argparse
from ultralytics import YOLO
import src.config as cfg

def resolve_path(root: str, rel_path: str) -> str:
    """
    Nếu rel_path không phải đường dẫn tuyệt đối, ghép với root để được đường dẫn đầy đủ.
    Thử các fallback:
      1. Thay 'valid' <-> 'val'
      2. Hoán vị hai thư mục nếu định dạng 'a/b'
    """
    # Xây dựng đường dẫn đầy đủ
    if os.path.isabs(rel_path):
        candidate = rel_path
    else:
        candidate = os.path.normpath(os.path.join(root, rel_path))
    # Nếu tồn tại, trả về
    if os.path.exists(candidate):
        return candidate
    # Fallback 1: 'valid' -> 'val'
    p2 = candidate.replace(f"{os.sep}valid{os.sep}", f"{os.sep}val{os.sep}")
    if os.path.exists(p2):
        return p2
    # Fallback 2: 'val' -> 'valid'
    p3 = candidate.replace(f"{os.sep}val{os.sep}", f"{os.sep}valid{os.sep}")
    if os.path.exists(p3):
        return p3
    # Fallback 3: hoán vị thư mục tương đối 'a/b' -> 'b/a'
    parts = rel_path.replace('\\', '/').split('/')
    if len(parts) == 2:
        swapped = os.path.normpath(os.path.join(root, parts[1], parts[0]))
        if os.path.exists(swapped):
            return swapped
    # Trả về candidate ban đầu nếu không tìm thấy
    return candidate

if __name__ == "__main__":
    # Khởi tạo parser để nhận tham số từ CLI
    parser = argparse.ArgumentParser(description="Huấn luyện YOLOv8 với YAML dataset linh hoạt")
    parser.add_argument("--data_yaml", type=str, default=cfg.DATA_YAML,
                        help="Đường dẫn tới file YAML dataset (train/val)")
    parser.add_argument("--model", type=str, default=cfg.MODEL_NAME,
                        help="Tên hoặc đường dẫn tới pretrained .pt model")
    parser.add_argument("--name", type=str, default="custom_train",
                        help="Tên experiment, lưu kết quả vào PROJECT_DIR/name")
    args = parser.parse_args()

    # Đọc file YAML định nghĩa dataset
    with open(args.data_yaml, 'r') as f:
        data_cfg = yaml.safe_load(f)
    root = os.path.dirname(os.path.abspath(args.data_yaml))

    # Chuyển đổi đường dẫn train/val thành tuyệt đối
    for key in ['train', 'val']:
        if key in data_cfg:
            data_cfg[key] = resolve_path(root, data_cfg[key])

    # Ghi đè file YAML với đường dẫn đã resolve
    with open(args.data_yaml, 'w') as f:
        yaml.dump(data_cfg, f)
    print(f"Đã cập nhật {args.data_yaml} với đường dẫn:")
    print(yaml.dump(data_cfg, sort_keys=False))

    # Khởi tạo và huấn luyện model
    model = YOLO(args.model)
    model.train(
        data         = args.data_yaml,      # Dùng file YAML (string) để YOLOv8 load dataset
        epochs       = cfg.EPOCHS,          # Số epoch từ config
        batch        = cfg.BATCH_SIZE,      # Batch size từ config
        imgsz        = cfg.IMG_SIZE,        # Kích thước ảnh
        lr0          = cfg.LEARNING_RATE,   # Learning rate ban đầu
        lrf          = cfg.LR_F,            # Tỉ lệ learning rate cuối
        optimizer    = cfg.OPTIMIZER,       # Optimizer (AdamW/SGD)
        augment      = cfg.AUGMENT,         # Bật augmentation
        mosaic       = cfg.MOSAIC,          # Xác suất mosaic
        mixup        = cfg.MIXUP,           # Xác suất mixup
        close_mosaic = cfg.CLOSE_MOSAIC,    # Epoch tắt mosaic
        patience     = cfg.PATIENCE,        # EarlyStopping patience
        **cfg.HSV_PARAMS,                  # Tham số HSV augment
        **cfg.TRANSFORM_PARAMS,            # Tham số transform augment
        project      = cfg.PROJECT_DIR,     # Thư mục lưu kết quả
        name         = args.name,           # Tên experiment
        exist_ok     = True                 # Cho phép ghi đè nếu đã tồn tại
    )