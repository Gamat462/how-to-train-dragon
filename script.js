const display = document.getElementById("display");
const status = document.getElementById("status");
const inputsBox = document.getElementById("inputs");
const hoursInput = document.getElementById("hours");
const minutesInput = document.getElementById("minutes");
const secondsInput = document.getElementById("seconds");
const startBtn = document.getElementById("startBtn");
const pauseBtn = document.getElementById("pauseBtn");
const resetBtn = document.getElementById("resetBtn");
const presetButtons = document.querySelectorAll(".presets button");

let remainingSeconds = 0;
let intervalId = null;

function formatTime(totalSeconds) {
  const h = Math.floor(totalSeconds / 3600);
  const m = Math.floor((totalSeconds % 3600) / 60);
  const s = totalSeconds % 60;
  return [h, m, s].map((n) => String(n).padStart(2, "0")).join(":");
}

function updateDisplay() {
  display.textContent = formatTime(remainingSeconds);
}

function getInputSeconds() {
  const h = Number(hoursInput.value) || 0;
  const m = Number(minutesInput.value) || 0;
  const s = Number(secondsInput.value) || 0;
  return h * 3600 + m * 60 + s;
}

function playAlarm() {
  const ctx = new (window.AudioContext || window.webkitAudioContext)();
  const now = ctx.currentTime;
  [0, 0.4, 0.8].forEach((offset) => {
    const osc = ctx.createOscillator();
    const gain = ctx.createGain();
    osc.type = "sine";
    osc.frequency.value = 880;
    gain.gain.setValueAtTime(0.2, now + offset);
    gain.gain.exponentialRampToValueAtTime(0.001, now + offset + 0.3);
    osc.connect(gain).connect(ctx.destination);
    osc.start(now + offset);
    osc.stop(now + offset + 0.3);
  });
}

function tick() {
  remainingSeconds -= 1;
  updateDisplay();
  if (remainingSeconds <= 0) {
    stopTimer();
    display.classList.add("done");
    status.textContent = "Waktu habis!";
    playAlarm();
    if (document.title !== "⏰ Waktu habis!") {
      document.title = "⏰ Waktu habis!";
    }
  }
}

function startTimer() {
  if (intervalId) return;

  if (remainingSeconds <= 0) {
    remainingSeconds = getInputSeconds();
    if (remainingSeconds <= 0) {
      status.textContent = "Set waktu terlebih dahulu.";
      return;
    }
  }

  display.classList.remove("done");
  status.textContent = "Berjalan...";
  inputsBox.querySelectorAll("input").forEach((el) => (el.disabled = true));
  startBtn.disabled = true;
  pauseBtn.disabled = false;

  intervalId = setInterval(tick, 1000);
}

function stopTimer() {
  clearInterval(intervalId);
  intervalId = null;
  startBtn.disabled = false;
  pauseBtn.disabled = true;
}

function pauseTimer() {
  stopTimer();
  status.textContent = "Dijeda.";
}

function resetTimer() {
  stopTimer();
  remainingSeconds = 0;
  display.classList.remove("done");
  status.textContent = "";
  document.title = "Timer";
  inputsBox.querySelectorAll("input").forEach((el) => (el.disabled = false));
  updateDisplay();
}

startBtn.addEventListener("click", startTimer);
pauseBtn.addEventListener("click", pauseTimer);
resetBtn.addEventListener("click", resetTimer);

presetButtons.forEach((btn) => {
  btn.addEventListener("click", () => {
    resetTimer();
    remainingSeconds = Number(btn.dataset.seconds);
    updateDisplay();
  });
});

[hoursInput, minutesInput, secondsInput].forEach((input) => {
  input.addEventListener("change", () => {
    if (!intervalId) {
      remainingSeconds = getInputSeconds();
      updateDisplay();
    }
  });
});

updateDisplay();
