// countdown.js

var countdownElement = document.getElementById('countdown');
var judgeDetails = JSON.parse(document.currentScript.getAttribute('data-judge-details'));
var countdownTicks = judgeDetails.countdown_ticks;

function updateCountdown() {
    countdownElement.innerText = countdownTicks + ' seconds remaining';
    countdownTicks--;

    if (countdownTicks < 0) {
        countdownElement.innerText = "Time's up!";
    } else {
        setTimeout(updateCountdown, 1000);
    }
}

updateCountdown();
