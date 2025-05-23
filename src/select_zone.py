# src/select_zone.py
from src.utils import select_zone_from_video
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--video", required=True, help="path to input video")
    parser.add_argument("--out",   default="zone.json", help="output JSON for polygon")
    args = parser.parse_args()
    select_zone_from_video(args.video, args.out)
