<<<<<<< HEAD
# Object Detection for Intruder Alert

> **Real-time** detection of unauthorized intruders in restricted zones using YOLOv8 and OpenCV, with automatic alerts and logging.
=======
**Object Detection Project: Phát hiện người xâm nhập vùng cấm thời gian thực**

**Mô tả**

**Dự án này sử dụng YOLOv8 và OpenCV để phát hiện người xâm nhập vào khu vực cấm trong video và webcam theo thời gian thực, đồng thời cảnh báo và ghi log vi phạm.**
**Cấu trúc thư mục**

---

## 🔍 Features

- **Real-time inference** on video files or webcam stream
- **Customizable restricted zone** via polygon coordinates
- **Automated dataset preparation**: 80/20 train-val split & `data.yaml` generation
- **Configurable training** with data augmentation and hyperparameters
- **Audio and visual alerts** when intruder detected
- **Comprehensive logging**: CSV logs and snapshot images saved to `logs/`
- **Modular structure** for easy maintenance and extension

---

## 📂 Project Structure

```
your-project/
├── models/             # Trained weights (best.pt)
├── data/               # Raw data & prepared dataset│   └── dataset/
│       ├── images/     # images/train + images/val
│       └── labels/     # labels/train + labels/val
├── src/                # Source code modules
│   ├── config.py       # Paths and hyperparameters
│   ├── utils.py        # Dataset prep & YAML generation
│   └── infer.py        # Inference & alert logic
├── logs/               # CSV logs and snapshots
├── requirements.txt    # Python dependencies
├── README.md           # Project guide
└── .gitignore
```

<<<<<<< HEAD
---

## 🚀 Getting Started

### 1. Prerequisites

- Python 3.7+
- Git
- (Optional) [Virtualenv](https://docs.python.org/3/library/venv.html)

### 2. Installation

```bash
# Clone repository
git clone https://github.com/AndreeD05/object-detection-project.git
cd object-detection-project

# (Optional) Create & activate virtual environment
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
.\.venv\Scripts\Activate.ps1  # Windows

#Nếu .\.venv\Scripts\Activate.ps1
#Mở PowerShell với quyền Administrator và thay đổi chính sách tạm thời
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process

# Install dependencies
=======
# Bước 1: Thêm pip vào virtualenv
python -m ensurepip --upgrade

# Bước 2: Giờ pip đã có, nâng cấp pip lên bản mới nhất
python -m pip install --upgrade pip

# Kiểm tra
python -m pip --version

pip install -r requirements.txt
```

<<<<<<< HEAD
---

## 🗂 Dataset Preparation

1. Place raw images in `data/dataset/images/` and corresponding `.txt` labels in `data/dataset/labels/`.
2. Run dataset prep script to split and generate `data.yaml`:
   ```bash
   python -c "from src.utils import prepare_dataset; prepare_dataset()"
   ```
3. Confirm structure:
   ```text
   data/dataset/
   ├── images/train
   ├── images/val
   ├── labels/train
   └── labels/val
   ```

---

## 🏋️‍♂️ Training

Train with YOLOv8:

Run training using the script in `src/train.py` with configuration from `src/config.py`:

```bash
python -m src.train
```

- Best weights saved at `models/custom_train/weights/best.pt`.

---
=======

## 🎥 Inference & Alerts

<<<<<<< HEAD
Run detection on a video or webcam:

```bash
<<<<<<< HEAD
python -m src.select_zone --video data_test/Stealing009_x264.mp4 --out zone.json
```

Sau khi xác nhận zone.json đúng, bạn chạy:
```bash
python -m src.infer --video data_test/Stealing009_x264.mp4 --out logs/output.mp4
```


=======
python src/infer.py   --video path/to/input.mp4   --out logs/output.mp4
```

>>>>>>> 1a416e67a02ce198a808b892800855958cc743de
For webcam (default camera):

```bash
python src/infer.py --video 0 --out logs/webcam.mp4
```

- Alerts logged in `logs/` with snapshots and CSV.

---

## ⚙️ Configuration

Adjust parameters in `src/config.py`:

- `POLYGON_POINTS`: Coordinates of restricted zone polygon
- `DATA_ROOT`, `EPOCHS`, `BATCH_SIZE`, `IMG_SIZE`, `LEARNING_RATE`, etc.

---

## 🛠️ Extending the Project

- Integrate Telegram/Zalo notifications
- Convert model to ONNX/TensorRT for edge deployment
- Wrap inference in a REST API (FastAPI/Flask)

---

## 📄 License
=======
**Tinh chỉnh & Mở rộng**
Thay đổi tọa độ vùng cấm trong src/config.py.
Chuyển sang real-time webcam: --video 0.
Tích hợp cảnh báo âm thanh, Telegram/Zalo thông qua hàm trong utils.py


