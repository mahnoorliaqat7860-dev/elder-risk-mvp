def risk_label(score: float) -> str:
    if score >= 0.7:
        return "High"
    elif score >= 0.4:
        return "Medium"
    else:
        return "Low"


def fuse_scores(face_score, voice_score, face_detected, voice_detected):
    if face_detected and voice_detected:
        score = (float(face_score) + float(voice_score)) / 2
    elif face_detected:
        score = float(face_score)
    elif voice_detected:
        score = float(voice_score)
    else:
        return "Low"

    if score >= 0.7:
        return "High"
    elif score >= 0.4:
        return "Medium"
    else:
        return "Low"
