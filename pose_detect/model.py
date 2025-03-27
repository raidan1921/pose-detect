"""
model.py – Loading the Rtmpose model and skeleton detection functions
"""
from rtmlib import Wholebody, draw_skeleton

def load_model():
    """
    Loads the Rtmpose model using the rmlib library.
    
    Returns:
        model: An instance of the loaded model.
    """
    wholebody = Wholebody(
        to_openpose=False,
        mode='performance',
        backend='onnxruntime',
        device='cuda'
    )

    return wholebody


def detect_skeleton(frame, model):
    """
    Runs skeleton detection on the given frame using the loaded model.
    
    Args:
        frame (np.array): The input image.
        model: The loaded Rtmpose model.
        
    Returns:
        output_frame (np.array): The output image with drawn skeletons.
    """

    keypoints, scores = model(frame)
    output_frame = draw_skeleton(frame, keypoints, scores, kpt_thr=0.5)
    
    return output_frame
