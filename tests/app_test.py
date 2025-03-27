import os
import pytest
import shutil
from fastapi.testclient import TestClient
from pose_detect.app import app
from moviepy.editor import ColorClip

client = TestClient(app)

@pytest.fixture(scope="session", autouse=True)
def cleanup_temp_videos():
    """Automatically deletes the temp_videos folder after all tests."""
    yield  # Wait until all tests are done
    
    temp_folder = "temp_videos"
    if os.path.exists(temp_folder):
        shutil.rmtree(temp_folder)
        print(f"Deleted folder: {temp_folder}")

@pytest.fixture
def test_video():
    """Creates a dummy video file for testing."""

    # Create a single frame: a red color for 1 second
    frame = ColorClip(size=(640, 480), color=(255, 0, 0), duration=1)  # Red background, 1 second duration
    # Write the video to a file
    test_video_path = "test_video.mp4"
    frame.write_videofile(test_video_path, codec="libx264", fps=1)
 
    yield test_video_path
    os.remove(test_video_path)  # Cleanup after test

def test_process_video_success(test_video):
    """Test if the API successfully processes a valid video file."""
    with open(test_video, "rb") as video_file:
        files = {"video": ("test_video.mp4", video_file, "video/mp4")}
        response = client.post("/process_video", files=files)
    
    assert response.status_code == 200
    assert response.headers["content-type"] == "video/mp4"

def test_process_video_invalid_file_type():
    """Test if the API rejects a non-video file."""
    files = {"video": ("test.txt", b"This is not a video", "text/plain")}
    response = client.post("/process_video", files=files)

    assert response.status_code == 422  # FastAPI should reject this request

def test_process_video_processing_failure(mocker, test_video):
    """Test if the API handles processing errors gracefully."""
    mocker.patch("pose_detect.app.process_video", side_effect=Exception("Processing failed"))
    
    with open(test_video, "rb") as video_file:
        files = {"video": ("test_video.mp4", video_file, "video/mp4")}
        response = client.post("/process_video", files=files)
    
    assert response.status_code == 500
    assert "An error occurred during processing" in response.json()["detail"]
