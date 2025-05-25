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
    - Giải nén dataset nếu cần (bỏ cell unzip)
    - Chia images/ và labels/ thành train/ val/
    - Sinh file data.yaml
    """
    img_dir = os.path.join(DATA_ROOT, "images")
    lbl_dir = os.path.join(DATA_ROOT, "labels")
    # Tạo folder con
    for sub in ("train","val"):
        os.makedirs(os.path.join(img_dir, sub), exist_ok=True)
        os.makedirs(os.path.join(lbl_dir, sub), exist_ok=True)

    # Lấy tất cả ảnh (jpg, png)
    imgs = glob.glob(os.path.join(img_dir, "*.jpg")) + glob.glob(os.path.join(img_dir, "*.png"))
    random.seed(0); random.shuffle(imgs)
    split = int(len(imgs) * (1 - SPLIT_RATIO))
    train, val = imgs[:split], imgs[split:]

    def _mv(lst, sub):
        for path in lst:
            fn  = os.path.basename(path)
            ext = os.path.splitext(fn)[1]
            # move ảnh
            shutil.move(path, os.path.join(img_dir, sub, fn))
            # move nhãn nếu có
            lbl = os.path.join(lbl_dir, fn.replace(ext, ".txt"))
            if os.path.exists(lbl):
                shutil.move(lbl, os.path.join(lbl_dir, sub, os.path.basename(lbl)))

    _mv(train, "train")
    _mv(val,   "val")

    # Sinh data.yaml
    cfg = {
        "path": DATA_ROOT,
        "train": "images/train",
        "val":   "images/val",
        "names": {0: "person"}
    }
    with open(os.path.join(DATA_ROOT, "data.yaml"), "w") as f:
        yaml.dump(cfg, f)
    print(f"Dataset prepared under {DATA_ROOT} (train/val, data.yaml).")

if __name__ == "__main__":
    prepare_dataset()