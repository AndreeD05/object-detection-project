import os, glob, random, shutil, yaml
from src.config import DATA_ROOT, SPLIT_RATIO, SOURCE_ROOT
from playsound import playsound
import threading
import csv
from datetime import datetime
import cv2, json

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

def play_alert_sound(mp3_path="alert.mp3"):
    threading.Thread(target=lambda: playsound(mp3_path, block=False), daemon=True).start()

def select_zone_from_video(video_path, save_path="zone.json"):
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
    print("Click để chọn các điểm vùng cấm (ít nhất 3 điểm). Nhấn 's' để lưu, 'q' để hủy.")

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
    with open(path, "r") as f:
        return json.load(f)

def prepare_dataset():
    """
    Copy dữ liệu đã chia từ SOURCE_ROOT → DATA_ROOT (images/train, val + labels/train, val)
    và sinh file data.yaml.
    """
    print(f"Copy dữ liệu từ {SOURCE_ROOT} → {DATA_ROOT}...")

    src_img_train = os.path.join(SOURCE_ROOT, "images", "train")
    src_img_val   = os.path.join(SOURCE_ROOT, "images", "val")
    src_lbl_train = os.path.join(SOURCE_ROOT, "labels", "train")
    src_lbl_val   = os.path.join(SOURCE_ROOT, "labels", "val")

    # Kiểm tra tồn tại thư mục nguồn
    for p in [src_img_train, src_img_val, src_lbl_train, src_lbl_val]:
        if not os.path.isdir(p):
            raise RuntimeError(f"Thiếu thư mục: {p}")

    # Tạo thư mục đích
    for sub in ["images/train", "images/val", "labels/train", "labels/val"]:
        os.makedirs(os.path.join(DATA_ROOT, sub), exist_ok=True)

    def copy_files(src_dir, dst_dir, exts):
        for ext in exts:
            for file in glob.glob(os.path.join(src_dir, f"*.{ext}")):
                shutil.copy(file, os.path.join(dst_dir, os.path.basename(file)))

    # Copy ảnh và nhãn
    copy_files(src_img_train, os.path.join(DATA_ROOT, "images/train"), ["jpg", "png"])
    copy_files(src_img_val,   os.path.join(DATA_ROOT, "images/val"),   ["jpg", "png"])
    copy_files(src_lbl_train, os.path.join(DATA_ROOT, "labels/train"), ["txt"])
    copy_files(src_lbl_val,   os.path.join(DATA_ROOT, "labels/val"),   ["txt"])

    # Sinh data.yaml
    cfg = {
        "path": DATA_ROOT,
        "train": "images/train",
        "val":   "images/val",
        "nc":    1,
        "names": {0: "person"}
    }
    with open(os.path.join(DATA_ROOT, "data.yaml"), "w") as f:
        yaml.dump(cfg, f)
    print(f"Dataset đã chuẩn bị xong tại {DATA_ROOT}. File data.yaml đã được tạo.")
