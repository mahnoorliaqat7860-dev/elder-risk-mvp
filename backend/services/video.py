import subprocess
import os
import uuid
import cv2
import shutil

def extract_frames_and_audio(video_path):
    frames = []
    frames_dir = f"/tmp/frames_{uuid.uuid4()}"
    audio_path = f"/tmp/{uuid.uuid4()}.wav"

    os.makedirs(frames_dir, exist_ok=True)

    try:
        # Extract frames
        subprocess.run(
            [
                "ffmpeg",
                "-y",
                "-i", video_path,
                "-vf", "fps=1,scale=640:-1",
                f"{frames_dir}/frame_%03d.jpg"
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            timeout=20
        )

        for fname in sorted(os.listdir(frames_dir)):
            frame = cv2.imread(os.path.join(frames_dir, fname))
            if frame is not None:
                frames.append(frame)

        # Extract audio
        result = subprocess.run(
            [
                "ffmpeg",
                "-y",
                "-i", video_path,
                "-ac", "1",
                "-ar", "16000",
                audio_path
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            timeout=20
        )

        if result.returncode != 0 or not os.path.exists(audio_path):
            audio_path = None

        return frames, audio_path

    finally:
        shutil.rmtree(frames_dir, ignore_errors=True)

