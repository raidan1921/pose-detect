# pose-detectsudo apt-get install ffmpeg

Skeleton Detection Microservice

Overview

This project is a FastAPI-based backend microservice that processes video files, detects human skeletons using the RTMPose model, and returns the processed video. The service receives a video file, extracts frames, applies skeleton detection, and then reconstructs the processed video.

Project Structure

pose-detect/
│── pose_detect/
    │── app.py                    # FastAPI application entry point
    │── model.py                  # Loads RTMPose model and runs skeleton detection
    │── video_processing.py        # Processes video: extracts frames, applies skeleton detection, reconstructs video
    │── performance_test.py        # Measures video processing speed and resource utilization
│── tests/
│   ├── app_test.py            # API endpoint tests
│── requirements.txt           # Required dependencies
│── README.md                  # Documentation

Installation

Prerequisites

Python 3.8+

ffmpeg installed and available in the system PATH

Steps

Clone the repository:

git clone https://github.com/your-repo/skeleton-detection-microservice.git
cd skeleton-detection-microservice

Create and activate a virtual environment:

python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

Install dependencies:

pip install -r requirements.txt

Install the project:

pip install .

Running the Microservice

Start the FastAPI server with Uvicorn:

uvicorn app:app --host 0.0.0.0 --port 8000

The API will be available at: http://127.0.0.1:8000

API Endpoints

Process Video

Endpoint:

POST /process_video

Description: Accepts a video file, applies skeleton detection, and returns the processed video. Request:

Form-data with a video file. Response:

Processed video file (video/mp4 format).

Running Tests

To run the tests:

pytest

Performance Testing

To measure the processing speed and resource usage:

python performance_test.py

Future Improvements

Support for real-time video streams

GPU acceleration for faster processing

Parallelized processing for large-scale workloads