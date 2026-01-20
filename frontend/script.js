"use strict";

document.addEventListener("DOMContentLoaded", () => {

  let mediaRecorder = null;
  let mediaStream = null;
  let recordedChunks = [];
  let autoStopTimer = null;

  const statusEl = document.getElementById("status");
  const resultEl = document.getElementById("result");
  const preview = document.getElementById("preview");
  const stopBtn = document.getElementById("stopBtn");
  const uploadInput = document.getElementById("videoUpload");

  function speak(text) {
    if (!("speechSynthesis" in window)) return;
    const u = new SpeechSynthesisUtterance(text);
    u.rate = 0.9;
    speechSynthesis.speak(u);
  }

  function resetUI() {
    statusEl.innerText = "";
    resultEl.innerText = "";
    resultEl.className = "";
    resultEl.style.display = "block";
  }

  function showResult(risk) {
    resultEl.className = "";
    resultEl.classList.add(risk.toLowerCase());

    if (risk === "Low") resultEl.innerText = "Stress Signal: Low";
    else if (risk === "Medium") resultEl.innerText = "Stress Signal: Medium";
    else if (risk === "High") resultEl.innerText = "Stress Signal: High";
    else resultEl.innerText = "Result unavailable";
  }
  function startLiveCheckin() {
  console.log("Recording started");
}


  async function startLiveCheckin() {
    try {
      resetUI();
      recordedChunks = [];
      stopBtn.disabled = false;

      mediaStream = await navigator.mediaDevices.getUserMedia({ video: true, audio: true });
      preview.srcObject = mediaStream;

      mediaRecorder = new MediaRecorder(mediaStream, { mimeType: "video/webm" });

      mediaRecorder.ondataavailable = e => {
        if (e.data && e.data.size > 0) recordedChunks.push(e.data);
      };

      mediaRecorder.onstop = handleRecordingStop;

      mediaRecorder.start();
      statusEl.innerText = "Recording…";

      speak("How are you feeling today?");
      setTimeout(() => speak("Did you feel more tired than usual today?"), 12000);

      autoStopTimer = setTimeout(stopAndAnalyzeLive, 30000);

    } catch (err) {
      console.error(err);
      statusEl.innerText = "Camera or microphone access failed";
    }
  }

  function stopEarly() {
    stopAndAnalyzeLive();
  }

  function stopAndAnalyzeLive() {
    if (!mediaRecorder || mediaRecorder.state !== "recording") return;

    clearTimeout(autoStopTimer);
    stopBtn.disabled = true;
    statusEl.innerText = "Analyzing video…";
    mediaRecorder.stop();
  }

  async function handleRecordingStop() {
    if (mediaStream) mediaStream.getTracks().forEach(t => t.stop());
    if (!recordedChunks.length) return;

    const videoBlob = new Blob(recordedChunks, { type: "video/webm" });
    sendVideoForAnalysis(videoBlob, "live.webm");

  }

  function uploadExistingVideo() {
  const input = document.getElementById("videoUpload");

  if (!input.files || !input.files[0]) {
    alert("Please select a video first");
    return;
  }

  sendVideoForAnalysis(input.files[0], input.files[0].name);
}

  async function sendVideoForAnalysis(videoBlob, filename) {
  const formData = new FormData();
  formData.append("video", videoBlob, filename);

  const statusEl = document.getElementById("status");
  const resultEl = document.getElementById("result");

  statusEl.innerText = "Analyzing video…";
  resultEl.style.display = "none";
  resultEl.innerText = "";
  resultEl.className = "";

  try {
    const res = await fetch("/analyze", {
      method: "POST",
      body: formData
    });

    if (!res.ok) {
      throw new Error("Backend error");
    }

    const data = await res.json();

    if (!data || !data.risk) {
      throw new Error("Invalid response");
    }

    // ✅ SUCCESS UI
    statusEl.innerText = "Analysis complete";

    resultEl.style.display = "block";
    resultEl.className = data.risk.toLowerCase();
    resultEl.innerText = `Stress Signal: ${data.risk}`;

  } catch (err) {
    console.error(err);
    statusEl.innerText = "Unable to analyze video";
    resultEl.innerText = "Please try again";
    resultEl.style.display = "block";
  }
}


  window.uploadExistingVideo = uploadExistingVideo;
  window.startLiveCheckin = startLiveCheckin;
  window.stopEarly = stopEarly;

});
