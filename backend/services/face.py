import cv2
import numpy as np

face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

def analyze_face(frames):
    tensions = []

    for frame in frames:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        if len(faces) > 0:
            x, y, w, h = faces[0]
            roi = gray[y:y+h, x:x+w]
            tension = np.std(roi) / 255.0
            tensions.append(tension)

    if not tensions:
        return None

    return float(np.mean(tensions))
