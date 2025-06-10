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

- **Phát hiện thời gian thực** trên video hoặc luồng webcam  
- **Tùy chỉnh vùng cấm** qua tọa độ đa giác  
- **Dataset tự động chuẩn bị**: chia train-val 80/20 & sinh `data.yaml`  
- **Cấu hình huấn luyện linh hoạt** với data augmentation và siêu tham số  
- **Cảnh báo âm thanh & hình ảnh** khi phát hiện xâm nhập  
- **Ghi log chi tiết**: lưu CSV logs và ảnh chụp tại `logs/`  
- **Kiến trúc mô-đun** dễ mở rộng và bảo trì  
---

## 📂 Project Structure

```
your-project/
├── models/ # Trained weights (best.pt)
├── data/ # Raw + prepared dataset
│ └── dataset/
│ ├── images/ # images/train + images/val
│ └── labels/ # labels/train + labels/val
├── src/ # Source code
│ ├── config.py # Đường dẫn & siêu tham số
│ ├── utils.py # Dataset prep & YAML generation
│ ├── train.py # Script huấn luyện
│ └── infer.py # Inference & alert logic
├── logs/ # CSV logs & ảnh snapshot
├── requirements.txt # Thư viện Python
├── README.md # Hướng dẫn dự án
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

#Nếu .\.venv\Scripts\Activate.ps1 bị lỗi
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

## 🗂  Chuẩn Bị Dataset

1. Đặt ảnh gốc vào `data/dataset/images/` và nhãn `.txt` vào `data/dataset/labels/`.
2. Chạy script `data.yaml`:
   ```bash
   python -c "from src.utils import prepare_dataset; prepare_dataset()"
   ```
3. Xác nhận cấu trúc:
   ```text
   data/dataset/
   ├── images/train
   ├── images/val
   ├── labels/train
   └── labels/val
   ```
4. Cấu trúc trong data.yaml
   ```text
   path: data/person-3
   train: images/train    # <-- chuỗi, không phải list
   val:   images/val      # <-- chuỗi
   names:
      0: person
   ```

5. Chạy Bằng GPU
```bash
   pip uninstall torch torchvision torchaudio
   pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```
---




## 🏋️‍♂️ Huấn Luyện

Train with YOLOv8:

Run training using the script in `src/train.py` with configuration from `src/config.py`:

```bash
python -m src.train --data_yaml data\person-3\data.yaml --model yolov8n.pt --name custom_train
```

- Weights tốt nhất lưu tại `models/custom_train/weights/best.pt`.

---
=======

## 🎥 Inference & Cảnh Báo

<<<<<<< HEAD
Run detection on a video or webcam:

1. Chọn vùng cấm:
```bash
python -m src.select_zone --video data_test/Stealing009_x264.mp4 --out zone.json
```
2. Chạy phát hiện:
Sau khi xác nhận zone.json đúng, bạn chạy:
```bash
python -m src.infer --video data_test/Stealing009_x264.mp4 --out logs/output.mp4
```


3. Webcam (camera 0):
```bash
python -c "from src.utils import select_zone_from_video; select_zone_from_video(0, 'zone.json')"
```
```bash
python -m src.infer --video 0 --out logs/webcam.mp4
```

- Cảnh báo và ảnh snapshot được lưu trong logs/, cùng file CSV log.

---

## ⚙️  Cấu Hình

Chỉnh trong `src/config.py`:

- `POLYGON_POINTS`: Tọa độ đa giác vùng cấm
- `DATA_ROOT`, `EPOCHS`, `BATCH_SIZE`, `IMG_SIZE`, `LEARNING_RATE`, etc.

---

## 🛠️ Tinh Chỉnh & Mở Rộng

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


