#các hàm hỗ trợ (prep dataset, split, sinh data.yaml)

import os, glob, random, shutil, yaml
from src.config import DATA_ROOT, SPLIT_RATIO
from playsound import playsound
import threading
import csv
from datetime import datetime
import cv2, json, os

LOG_CSV = "logs/violations.csv"


def init_log():
    os.makedirs(os.path.dirname(LOG_CSV), exist_ok=True)
    if not os.path.exists(LOG_CSV):
        with open(LOG_CSV, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["timestamp", "x", "y", "confidence"])

def log_violation(x, y, confidence):
    with open(LOG_CSV, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([datetime.now().isoformat(), x, y, f"{confidence:.2f}"])

# src/utils.py (phần trên cùng)
def play_alert_sound(mp3_path="alert.mp3"):
    """Phát âm thanh báo động không block quá trình xử lý."""
    threading.Thread(target=lambda: playsound(mp3_path, block=False), daemon=True).start()

def select_zone_from_video(video_path, save_path="zone.json"):
    """
    Mở video, lấy frame đầu tiên, cho phép click chọn polygon,
    nhấn 's' để lưu (các điểm sẽ được lưu vào JSON), 'q' để hủy.
    """
    cap = cv2.VideoCapture(video_path)
    ret, frame = cap.read()
    cap.release()
    if not ret:
        raise RuntimeError(f"Không đọc được frame từ {video_path}")

    pts = []
    temp = frame.copy()
    win = "Select Zone"
    cv2.namedWindow(win)

    def on_mouse(evt, x, y, flags, param):
        if evt == cv2.EVENT_LBUTTONDOWN:
            pts.append((x, y))
            cv2.circle(temp, (x, y), 4, (0, 0, 255), -1)
            cv2.imshow(win, temp)

    cv2.setMouseCallback(win, on_mouse)
    print("Click để chọn các điểm vùng cấm (ít nhất 3 điểm).")
    print("Nhấn 's' để lưu, 'q' để thoát không lưu.")

    while True:
        cv2.imshow(win, temp)
        key = cv2.waitKey(0) & 0xFF
        if key == ord('s') and len(pts) >= 3:
            os.makedirs(os.path.dirname(save_path) or ".", exist_ok=True)
            with open(save_path, "w") as f:
                json.dump(pts, f)
            print(f"Đã lưu vùng cấm vào {save_path}")
            break
        elif key == ord('q'):
            print("Đã hủy chọn vùng cấm.")
            break

    cv2.destroyWindow(win)
    return pts

def load_zone(path="zone.json"):
    """Đọc polygon từ file JSON"""
    with open(path, "r") as f:
        pts = json.load(f)
    return pts

def prepare_dataset():
    """
    Hỗ trợ 2 kiểu cấu trúc dữ liệu:
      1) cổ điển: DATA_ROOT/images + DATA_ROOT/labels
      2) mới:       DATA_ROOT/train/images + DATA_ROOT/train/label
    Sau đó chia ngẫu nhiên thành train/val và sinh data.yaml.
    """
    # --- 1. Xác định thư mục ảnh và nhãn gốc ---
    if os.path.isdir(os.path.join(DATA_ROOT, "train", "images")):
        img_dir = os.path.join(DATA_ROOT, "train", "images")
        lbl_dir = os.path.join(DATA_ROOT, "train", "label")   # hoặc "labels" tùy bạn đặt
    else:
        img_dir = os.path.join(DATA_ROOT, "images")
        lbl_dir = os.path.join(DATA_ROOT, "labels")

    # --- 2. Tạo thư mục đích cho train/val ---
    for sub in ("train", "val"):
        os.makedirs(os.path.join(DATA_ROOT, "images", sub), exist_ok=True)
        os.makedirs(os.path.join(DATA_ROOT, "labels", sub), exist_ok=True)

    # --- 3. Lấy list tất cả ảnh trong img_dir ---
    imgs = glob.glob(os.path.join(img_dir, "*.jpg")) + glob.glob(os.path.join(img_dir, "*.png"))
    if not imgs:
        raise RuntimeError(f"Không tìm thấy ảnh trong {img_dir}")

    random.seed(0)
    random.shuffle(imgs)
    split_idx = int(len(imgs) * (1 - SPLIT_RATIO))
    train_imgs, val_imgs = imgs[:split_idx], imgs[split_idx:]

    # --- 4. Di chuyển (hoặc copy) ảnh & nhãn vào đúng folder ---
    def _move_list(img_list, sub):
        for img_path in img_list:
            fname = os.path.basename(img_path)
            name, ext = os.path.splitext(fname)
            # ảnh
            dst_img = os.path.join(DATA_ROOT, "images", sub, fname)
            shutil.move(img_path, dst_img)
            # nhãn
            src_lbl = os.path.join(lbl_dir, name + ".txt")
            if os.path.exists(src_lbl):
                dst_lbl = os.path.join(DATA_ROOT, "labels", sub, name + ".txt")
                shutil.move(src_lbl, dst_lbl)

    _move_list(train_imgs, "train")
    _move_list(val_imgs,   "val")

    # --- 5. Sinh data.yaml ---
    cfg = {
        "path": DATA_ROOT,
        "train": "images/train",
        "val":   "images/val",
        "names": {0: "person"}
    }
    with open(os.path.join(DATA_ROOT, "data.yaml"), "w") as f:
        yaml.dump(cfg, f)
    print(f"Dataset prepared under {DATA_ROOT} (train/val, data.yaml).")