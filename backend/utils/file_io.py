import uuid
from pathlib import Path

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

def save_upload(file):
    suffix = file.filename.split(".")[-1] if "." in file.filename else "webm"

    path = UPLOAD_DIR / f"{uuid.uuid4()}.{suffix}"

    with open(path, "wb") as f:
        f.write(file.file.read())

    return str(path)
