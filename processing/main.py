import sys
import cv2
import torch
from processing import VideoManager as vm
import numpy as np

if __name__ == '__main__':
    # if len(sys.argv):
    #    print("Usage: main.py <video> <point_lower_left> <point_upper_right> <frame_start> <frame_end> <frames_to_create> <model>")
    video = sys.argv[1]
    torch.set_grad_enabled(False)

    lower_left = [int(x) for x in sys.argv[2].split(",")]
    upper_right = [int(x) for x in sys.argv[3].split(",")]
    frame_start = int(sys.argv[4])
    frame_end = int(sys.argv[5])
    #torch.set_grad_enabled(False)
    frame_to_create = int(sys.argv[6])
    # model = int(sys.argv[7])
    # print(torch.cuda.is_available())
    video_manager = vm.VideoManager()
    video_manager.open_video(video)
    frames = video_manager.generate_frames(lower_left, upper_right, frame_start, frame_end, frame_to_create)
    for frame in frames:
        cv2.imshow("interpolated", frame)
        cv2.waitKey()

    print("termino uwu")
