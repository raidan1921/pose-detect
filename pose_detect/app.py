"""
app.py – FastAPI-based backend microservice for video processing.
The endpoint receives the video, starts processing, and returns the processed video.
"""

import os
import uuid

from fastapi import FastAPI, File, UploadFile, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse

from pose_detect.model import load_model
from pose_detect.video_processing import process_video

app = FastAPI(title="Skeleton Detection Microservice")

model = load_model()


def safe_delete_file(file_path: str):
    """Safely delete a file, ignoring errors if it doesn't exist."""
    try:
        os.remove(file_path)
    except OSError:
        pass
    
@app.post("/process_video", summary="Process video with skeleton detection")
async def process_video_endpoint(background_tasks: BackgroundTasks, video: UploadFile = File(...)):
    """
    Processes the uploaded video, runs skeleton detection on frames, 
    and then returns the processed video.
    
    Args:
        video (UploadFile): The uploaded video file.
        
    Returns:
        FileResponse: The processed video.
    """
    if not video.content_type.startswith("video/"):
        raise HTTPException(
            status_code=422, 
            detail="Invalid file type. Please upload a video."
        )

    # Save to a temporary directory
    temp_dir = "temp_videos"
    os.makedirs(temp_dir, exist_ok=True)
    input_filename = os.path.join(temp_dir, f"{uuid.uuid4()}_{video.filename}")
    
    with open(input_filename, "wb") as f:
        content = await video.read()
        f.write(content)

    output_filename = input_filename.replace(".", "_processed.")
    
    try:
        process_video(input_filename, output_filename, model)
    except Exception as e:
        # Clean up temporary files in case of an error
        safe_delete_file(input_filename)
        safe_delete_file(output_filename)
        raise HTTPException(status_code=500, detail=f"An error occurred during processing: {e}")
    
    # Clean up temporary files
    safe_delete_file(input_filename)
    background_tasks.add_task(safe_delete_file, output_filename)
    
    return FileResponse(path=output_filename, filename=os.path.basename(output_filename), media_type="video/mp4")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
