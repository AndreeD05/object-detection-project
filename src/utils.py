import os, glob, random, shutil, yaml

from src.config import DATA_ROOT, SPLIT_RATIO

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