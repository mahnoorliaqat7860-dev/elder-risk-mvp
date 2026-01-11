print("ANALYZE HIT")

from fastapi import APIRouter, UploadFile, File, HTTPException
from backend.utils.file_io import save_upload
from backend.services.video import extract_frames_and_audio
from backend.services.face import analyze_face
from backend.services.voice import analyze_voice
from backend.services.risk import fuse_scores

MIN_FRAMES = 10

router = APIRouter()

@router.post(
    "/analyze",
    summary="Analyze short selfie video",
    description="""
Upload a 30–60 second selfie video.
Requirements:
- Continuous video
- Face and/or voice must be present
- Images are NOT supported
"""
)
def analyze(video: UploadFile = File(...)):
    video_path = save_upload(video)

    try:
        frames, audio_path = extract_frames_and_audio(video_path)

        if frames is None or len(frames) < MIN_FRAMES:
            raise HTTPException(
                status_code=400,
                detail="Invalid input. Please upload a short video, images are not supported."
            )

        face_score, face_detected = analyze_face(frames)
        voice_score, voice_detected = analyze_voice(audio_path)

    except HTTPException:
        raise

    except Exception as e:
        print("ANALYSIS ERROR:", e)
        raise HTTPException(
            status_code=500,
            detail="Video processing failed"
        )


    result = fuse_scores(
        face_score=face_score,
        voice_score=voice_score,
        face_detected=face_detected,
        voice_detected=voice_detected
    )

    return result
