"""
video_processing.py – Video processing by breaking it into frames, calculating FPS,
skeleton detection, and reassembling into an ffmpeg-compatible video.
"""

import cv2
import time
import os
import subprocess
import shutil

from pose_detect.model import detect_skeleton


def process_video(input_path, output_path, model):
    """
    Processes the input video by breaking it into frames, running skeleton detection on each,
    drawing the current FPS value, and then reassembling the results into a video.
    
    Args:
        input_path (str): The input video file path.
        output_path (str): The output video file path.
        model: The loaded rtmpose model.
    
    Returns:
        output_path (str): The path to the processed video.
    """
    cap = cv2.VideoCapture(input_path)
    if not cap.isOpened():
        raise IOError("Failed to open the video: {}".format(input_path))

    # Retrieve video parameters
    fps = cap.get(cv2.CAP_PROP_FPS)

    # Save each frame to a temporary folder
    temp_frames_dir = "temp_frames"
    if not os.path.exists(temp_frames_dir):
        os.makedirs(temp_frames_dir)

    frame_count = 0
    start_time = time.time()
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Skeleton detection on the frame
        processed_frame = detect_skeleton(frame, model)
        
        # Calculate the current FPS
        frame_count += 1
        elapsed_time = time.time() - start_time
        current_fps = frame_count / elapsed_time if elapsed_time > 0 else 0
        
        # Draw the FPS value on the frame
        cv2.putText(processed_frame, f"FPS: {current_fps:.2f}", (10, 30), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        
        # Save the processed frame temporarily
        frame_filename = os.path.join(temp_frames_dir, f"frame_{frame_count:06d}.png")
        cv2.imwrite(frame_filename, processed_frame)

    cap.release()

    # Use ffmpeg to assemble the video with original parameters
    ffmpeg_command = [
        "ffmpeg",
        "-y",
        "-framerate", str(fps),
        "-i", os.path.join(temp_frames_dir, "frame_%06d.png"),
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        output_path
    ]
    
    subprocess.run(ffmpeg_command, check=True)
    
    # Delete temporary files
    shutil.rmtree(temp_frames_dir)
    
    return output_path
