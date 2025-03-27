# Skeleton Detection Microservice

## Overview

This project is a **FastAPI-based backend microservice** that processes video files, detects human skeletons using the **RTMPose model**, and returns the processed video. The service:

- Receives a video file
- Extracts frames
- Applies skeleton detection
- Reconstructs the processed video

---

## Project Structure

```
pose-detect/
│── pose_detect/
│   ├── app.py                # FastAPI application entry point
│   ├── model.py              # Loads RTMPose model and runs skeleton detection
│   ├── video_processing.py   # Processes video: extracts frames, applies skeleton detection, reconstructs video
│   ├── performance_test.py   # Measures video processing speed and resource utilization
│── tests/
│   ├── app_test.py           # API endpoint tests
│── requirements.txt          # Required dependencies
│── README.md                 # Documentation
```

---

## Installation

### Prerequisites

- **Python 3.8+**
- **ffmpeg** installed and available in the system PATH
  ```sh
  sudo apt-get install ffmpeg
  ```

### Steps

#### 1. Clone the repository:

```sh
git clone https://github.com/your-repo/skeleton-detection-microservice.git
cd skeleton-detection-microservice
```

#### 2. Create and activate a virtual environment:

```sh
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

#### 3. Install dependencies:

```sh
pip install -r requirements.txt
```

#### 4. Install the project:

```sh
pip install .
```

---

## Running the Microservice

Start the **FastAPI** server with **Uvicorn**:

```sh
uvicorn app:app --host 0.0.0.0 --port 8000
```

The API will be available at: [**http://127.0.0.1:8000**](http://127.0.0.1:8000)

---

## API Endpoints

### Process Video

- **Endpoint:** `POST /process_video`
- **Description:** Accepts a video file, applies skeleton detection, and returns the processed video.
- **Request:**
  - Form-data with a video file.
- **Response:**
  - Processed video file (**video/mp4 format**).

---

## Running Tests

To run the tests:

```sh
pytest tests
```

---

## Performance Testing

To measure the processing speed and resource usage:

```sh
python performance_test.py
```

