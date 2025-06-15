import cv2
from skimage.metrics import peak_signal_noise_ratio
import numpy as np
import argparse
import os

def calculate_video_psnr(baseline_video_path, test_video_path):


    cap_baseline = cv2.VideoCapture(baseline_video_path)
    cap_test = cv2.VideoCapture(test_video_path)

    baseline_frame_count = int(cap_baseline.get(cv2.CAP_PROP_FRAME_COUNT))
    test_frame_count = int(cap_test.get(cv2.CAP_PROP_FRAME_COUNT))
    baseline_fps = cap_baseline.get(cv2.CAP_PROP_FPS)
    test_fps = cap_test.get(cv2.CAP_PROP_FPS)
    baseline_width = int(cap_baseline.get(cv2.CAP_PROP_FRAME_WIDTH))
    baseline_height = int(cap_baseline.get(cv2.CAP_PROP_FRAME_HEIGHT))
    test_width = int(cap_test.get(cv2.CAP_PROP_FRAME_WIDTH))
    test_height = int(cap_test.get(cv2.CAP_PROP_FRAME_HEIGHT))


    psnr_values = []
    processed_frames = 0
    min_frames = min(baseline_frame_count, test_frame_count)

    for frame_num in range(min_frames):
        ret_baseline, frame_baseline = cap_baseline.read()
        ret_test, frame_test = cap_test.read()

        if frame_baseline.shape[:2] != frame_test.shape[:2]:
            frame_test_resized = cv2.resize(frame_test, (frame_baseline.shape[1], frame_baseline.shape[0]))
            current_psnr = peak_signal_noise_ratio(frame_baseline, frame_test_resized, data_range=255)
        else:
            current_psnr = peak_signal_noise_ratio(frame_baseline, frame_test, data_range=255)

        psnr_values.append(current_psnr)
        processed_frames += 1


    cap_baseline.release()
    cap_test.release()

    average_psnr = np.mean(psnr_values)
    return average_psnr

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="計算兩個 MP4 影片之間的平均 PSNR。")
    parser.add_argument("baseline_video")
    parser.add_argument("test_video")

    args = parser.parse_args()

    avg_psnr = calculate_video_psnr(args.baseline_video, args.test_video)

    if avg_psnr is not None:
        print(f"'{args.baseline_video}' 與 '{args.test_video}' 之間的平均 PSNR 為: {avg_psnr:.2f} dB")