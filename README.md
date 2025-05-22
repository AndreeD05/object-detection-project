**Object Detection Project: Phát hiện người xâm nhập vùng cấm thời gian thực**

**Mô tả**

**Dự án này sử dụng YOLOv8 và OpenCV để phát hiện người xâm nhập vào khu vực cấm trong video và webcam theo thời gian thực, đồng thời cảnh báo và ghi log vi phạm.**
**Cấu trúc thư mục**

your-project/
├── models/            # Chứa file weights (best.pt)
├── data/              # Chứa dataset gốc và video test
│   └── dataset/
│       ├── images/    # images/train, images/val
│       └── labels/    # labels/train, labels/val
├── src/               # Chứa code nguồn
│   ├── config.py      # Cấu hình đường dẫn, tham số
│   ├── utils.py       # Hàm chuẩn bị dataset, split, sinh data.yaml
│   └── infer.py       # Script inference + logic vùng cấm
├── logs/              # Lưu các file CSV log và ảnh snapshot
├── requirements.txt   # List dependencies
├── README.md          # Hướng dẫn này
└── .gitignore

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
pip install --upgrade pip
pip install -r requirements.txt

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


**Tinh chỉnh & Mở rộng**
Thay đổi tọa độ vùng cấm trong src/config.py.
Chuyển sang real-time webcam: --video 0.
Tích hợp cảnh báo âm thanh, Telegram/Zalo thông qua hàm trong utils.py

