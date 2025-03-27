"""
performance_test.py – Performance test script that measures the speed of video processing and resource utilization.
"""

import time
import psutil
import GPUtil
from pose_detect.model import load_model
from pose_detect.video_processing import process_video

def run_performance_test(input_video_path: str):
    """
    Run the performance test with the provided video file.
    
    Args:
        input_video_path (str): The path to the test video.
    """
    model = load_model()
    
    output_video_path = input_video_path.replace(".", "_processed.")
    
    process = psutil.Process()
    process.cpu_percent()

    start_time = time.time()
    process_video(input_video_path, output_video_path, model)
    total_time = time.time() - start_time
    
    # Query CPU and memory usage
    
    cpu_usage = process.cpu_percent()
    mem_usage = process.memory_info().rss / (1024 * 1024)  # in MB
    
    gpu_load = GPUtil.getGPUs()[0].load * 100 if GPUtil.getGPUs() else "N/A"

    print(f"Total processing time: {total_time:.2f} seconds")
    print(f"CPU usage: {cpu_usage:.2f}%")
    print(f"Memory usage: {mem_usage:.2f}MB")
    print(f"GPU usage: {gpu_load if gpu_load != 'N/A' else 'Not available'}%")    

if __name__ == "__main__":
    test_video = "video-for-pose-detection.mp4"  # Replace with the path to your test video
    run_performance_test(test_video)
