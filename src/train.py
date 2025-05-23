# src/train.py
from ultralytics import YOLO
import src.config as cfg

def main():
    model = YOLO(cfg.MODEL_NAME)
    model.train(
        data=cfg.DATA_YAML,
        epochs=cfg.EPOCHS,
        batch=cfg.BATCH_SIZE,
        imgsz=cfg.IMG_SIZE,
        lr0=cfg.LEARNING_RATE,
        lrf=cfg.LR_F,
        optimizer=cfg.OPTIMIZER,
        augment=cfg.AUGMENT,
        **cfg.HSV_PARAMS,
        **cfg.TRANSFORM_PARAMS,
        mosaic=cfg.MOSAIC,
        mixup=cfg.MIXUP,
        patience=cfg.PATIENCE,
        close_mosaic=cfg.CLOSE_MOSAIC,
        project=cfg.PROJECT_DIR,
        name="custom_train",
        exist_ok=True
    )

if __name__ == "__main__":
    main()
