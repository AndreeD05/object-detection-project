<<<<<<< HEAD
# Object Detection for Intruder Alert

![Workflow](https://img.shields.io/badge/Workflow-YOLOv8-blue) ![License](https://img.shields.io/badge/License-MIT-green)

> **Real-time** detection of unauthorized intruders in restricted zones using YOLOv8 and OpenCV, with automatic alerts and logging.
=======
**Object Detection Project: Phát hiện người xâm nhập vùng cấm thời gian thực**

**Mô tả**

**Dự án này sử dụng YOLOv8 và OpenCV để phát hiện người xâm nhập vào khu vực cấm trong video và webcam theo thời gian thực, đồng thời cảnh báo và ghi log vi phạm.**
**Cấu trúc thư mục**
>>>>>>> 2abce3a95a493c3b3b84cf388ec6bac8ed0160f2

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
python3 -m venv .venv
source .venv/bin/activate  # Linux/macOS
\.venv\Scripts\activate   # Windows

# Install dependencies
=======
**Yêu cầu:**
Python 3.7+
Virtual environment (venv) khuyến khích
Các thư viện: ultralytics, opencv-python, numpy, playsound


**Cài đặt**
**1.Tạo và kích hoạt virtual environment (tùy chọn nhưng khuyến khích):**
python -m venv .venv
source .venv/bin/activate   # Linux/macOS
.\.venv\Scripts\activate  # Windows

**2.Cài dependencies:**
>>>>>>> 2abce3a95a493c3b3b84cf388ec6bac8ed0160f2
pip install --upgrade pip
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

```bash
python -c "from ultralytics import YOLO; model = YOLO('yolov8n.pt'); model.train(   data='data/dataset/data.yaml',   epochs=30,   batch=16,   imgsz=640,   project='models',   name='custom_train',   exist_ok=True )"
```

- Best weights saved at `models/custom_train/weights/best.pt`.

---
=======
**Chuẩn bị dataset**

1.Đặt toàn bộ ảnh gốc vào data/dataset/images/ và nhãn .txt vào data/dataset/labels/.
2.Chạy hàm prepare_dataset() trong src/utils.py để tự động chia 80% train, 20% val và sinh file data.yaml:
**python -c "from src.utils import prepare_dataset; prepare_dataset()"**

**Huấn luyện model**
Chạy lệnh sau để train bằng YOLOv8:
python -c "from ultralytics import YOLO; model=YOLO('yolov8n.pt'); model.train(data='data/dataset/data.yaml', epochs=30, imgsz=640, batch=16, project='models', name='custom_train', exist_ok=True)"

_Kết quả weights best.pt sẽ nằm trong runs/detect/custom_train/weights/, bạn nên copy về thư mục models/._

**Inference & Cảnh báo**
Dùng script src/infer.py để phát hiện trên video hoặc webcam:
python src/infer.py --video path/to/input.mp4 --out path/to/output.mp4

_Kết quả video có bounding box và polygon vùng cấm sẽ được lưu tại output.mp4._

**# Video file**
python src/infer.py --video data/test_video.mp4 --out logs/output.mp4

**# Hoặc real-time từ webcam**
python src/infer.py --video 0 --out logs/webcam_output.mp4
Các cảnh báo, log vi phạm sẽ được ghi trong thư mục logs/.
>>>>>>> 2abce3a95a493c3b3b84cf388ec6bac8ed0160f2

## 🎥 Inference & Alerts

<<<<<<< HEAD
Run detection on a video or webcam:

```bash
python src/infer.py   --video path/to/input.mp4   --out logs/output.mp4
```

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

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.
=======
**Tinh chỉnh & Mở rộng**
Thay đổi tọa độ vùng cấm trong src/config.py.
Chuyển sang real-time webcam: --video 0.
Tích hợp cảnh báo âm thanh, Telegram/Zalo thông qua hàm trong utils.py

>>>>>>> 2abce3a95a493c3b3b84cf388ec6bac8ed0160f2
