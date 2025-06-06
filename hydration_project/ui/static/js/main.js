// Just for fun — show a splash sound when prediction appears (can be improved later)
document.addEventListener("DOMContentLoaded", function () {
  const result = document.querySelector(".fs-1");
  if (result) {
    const audio = new Audio("https://www.soundjay.com/button/sounds/water-drop-1.mp3");
    audio.play();
    result.classList.add("animate-result");
  }

  // Bounce the form on load
  const form = document.querySelector("form");
  if (form) {
    form.classList.add("animate-bounce-in");
  }
});
