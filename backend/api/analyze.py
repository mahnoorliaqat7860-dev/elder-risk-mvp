print("ANALYZE HIT")

from fastapi import APIRouter, UploadFile, File, HTTPException
from concurrent.futures import ThreadPoolExecutor, TimeoutError
from backend.utils.runtime import ENABLE_BACKEND_TIMEOUT

executor = ThreadPoolExecutor(max_workers=1)
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

    face_score = None
    voice_score = None

    try:
        frames, audio_path = extract_frames_and_audio(video_path)
    except Exception:
        frames, audio_path = [], None

    # --- Face analysis ---
    try:
        if frames:
            face_score = analyze_face(frames)
    except Exception:
        face_score = None

    # --- Voice analysis ---
    try:
        if audio_path:
            voice_score = analyze_voice(audio_path)
    except Exception:
        voice_score = None

    # --- HARD GUARD (MVP RULE) ---
    if face_score is None and voice_score is None:
        return {
            "risk": "Low",
            "face_score": None,
            "voice_score": None,
            "note": "Insufficient signal, default low risk"
        }

    face_score = analyze_face(frames)
    voice_score = analyze_voice(audio_path)

    face_detected = isinstance(face_score, (int, float))
    voice_detected = isinstance(voice_score, (int, float))
    
    risk = fuse_scores(
        face_score,
        voice_score,
        face_detected,
        voice_detected
    )
    return {
    "face_score": face_score,
    "voice_score": voice_score,
    "risk": risk
    }
