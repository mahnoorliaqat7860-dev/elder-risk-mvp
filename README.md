# ElderRisk MVP

A minimal prototype that detects elder risk signals from a 30 to 60 second selfie video using face tension and voice stress features.

## What It Does

1. Records one continuous selfie video
2. Extracts facial landmarks and voice features
3. Computes face stress score
4. Computes voice stress score
5. Outputs a combined risk label: Low, Medium, High

## Why This Exists

The goal is to validate a single thesis:

A short selfie video contains enough signal to flag meaningful elder risk.

This is not a medical product and makes no clinical claims.

## Tech Stack

- FastAPI backend
- OpenCV for facial landmarks
- Librosa for voice features
- Simple rule based fusion logic
- Local storage and synchronous processing

## How To Run

pip install -r requirements.txt
uvicorn backend.main:app --reload

css
Copy code

Open the frontend and upload a video between 30 and 60 seconds.

## Output Example

{
"face_stress": 0.62,
"voice_stress": 0.71,
"risk": "High"
}

pgsql
Copy code

## Design Principles

- Single endpoint
- No dashboards
- No training pipelines
- No medical language
- Speed over complexity

## Roadmap

Only one goal: prove signal validity with real caregiver feedback.

## Disclaimer

This MVP is for research and demonstration only. It does not provide medical diagnosis or healthcare advice.