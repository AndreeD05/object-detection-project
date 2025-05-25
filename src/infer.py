from ultralytics import YOLO
import cv2, numpy as np
from src.config import WEIGHTS_PATH, POLYGON_POINTS, ZONE_PATH
import os
from src.utils import play_alert_sound, init_log, log_violation, load_zone

def run_inference(video_path, output_path="output.mp4"):
    init_log()
     # Load polygon từ JSON
    POLYGON_POINTS = load_zone(ZONE_PATH)
    original_polygon = np.array(POLYGON_POINTS, dtype=np.float32)
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS) or 25
    w   = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h   = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    out = cv2.VideoWriter(output_path,
                          cv2.VideoWriter_fourcc(*'mp4v'),
                          fps, (w,h))

    model = YOLO(WEIGHTS_PATH)
    original_polygon = np.array(POLYGON_POINTS, dtype=np.float32)

    cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
    ret, first = cap.read()
    prev_gray = cv2.cvtColor(first, cv2.COLOR_BGR2GRAY)
    orb = cv2.ORB_create(500)
    bf  = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

    cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
    while True:
        ret, frame = cap.read()
        if not ret: break
        curr_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # estimate affine transform for polygon
        kp1, des1 = orb.detectAndCompute(prev_gray, None)
        kp2, des2 = orb.detectAndCompute(curr_gray, None)
        poly = original_polygon.copy()
        if des1 is not None and des2 is not None and len(kp1)>=4 and len(kp2)>=4:
            m = bf.match(des1, des2)
            m = sorted(m, key=lambda x:x.distance)[:50]
            if len(m)>=4:
                src = np.float32([kp1[mm.queryIdx].pt for mm in m]).reshape(-1,1,2)
                dst = np.float32([kp2[mm.trainIdx].pt for mm in m]).reshape(-1,1,2)
                M, _ = cv2.estimateAffinePartial2D(src, dst)
                if M is not None:
                    poly = cv2.transform(poly[None,:,:], M)[0]

        intruded = False
        # run detection
        for r in model(frame):
            for b in r.boxes.data:
                x1,y1,x2,y2,conf,cls = b.tolist()
                if int(cls)==0:
                    # always draw label
                    label = f"person {conf:.2f}"
                    cv2.putText(frame, label, (int(x1), int(y1)-10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,255), 2)

                    foot = (int((x1+x2)/2), int(y2))
                    inside = cv2.pointPolygonTest(poly.astype(np.int32),
                                                  foot, False)
                    color = (0,0,255) if inside>=0 else (0,255,0)
                    if inside >= 0:
                        intruded = True
                        play_alert_sound("alert.mp3")
                        log_violation(foot[0], foot[1], conf)
                        cv2.putText(frame, "Intruder!",
                                    (int(x1), int(y2)+25),
                                    cv2.FONT_HERSHEY_SIMPLEX,
                                    0.9, (0,0,255), 2)
                    cv2.rectangle(frame,
                                  (int(x1),int(y1)),
                                  (int(x2),int(y2)),
                                  color, 2)

        # draw restricted-zone polygon
        cv2.polylines(frame,
                      [poly.astype(np.int32)],
                      isClosed=True,
                      color=(0,0,255) if intruded else (255,0,0),
                      thickness=3)
        
        # --- Hiển thị live và phát âm thanh theo playsound() đã gọi bên trên ---
        cv2.imshow("Detection", frame)
        # Nhấn ESC (27) để dừng sớm
        if cv2.waitKey(1) & 0xFF == 27:
                break

        out.write(frame)
        prev_gray = curr_gray

    cap.release()
    out.release()
    cv2.destroyAllWindows()
    print(f"Inference done → {output_path}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--video", required=True,
                        help="path to input video or 0 for webcam")
    parser.add_argument("--out", default="output.mp4",
                        help="output video path")
    args = parser.parse_args()
    run_inference(args.video, args.out)
