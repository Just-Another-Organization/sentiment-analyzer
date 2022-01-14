const BASE_URL = window.location.origin + '/api'

RECENT_MODE = 'recent'
POPULAR_MODE = 'popular'

MODES = [
    RECENT_MODE,
    POPULAR_MODE
]

ONE_HOUR = '1h'
FOUR_HOUR = '4h'
ONE_DAY = '1d'
THREE_DAYS = '3d'

TIMEFRAMES = [
    ONE_HOUR,
    FOUR_HOUR,
    ONE_DAY,
    THREE_DAYS
]

let currentMode = RECENT_MODE
const MODES_NUMBER = MODES.length;
let currentTimeframe = ONE_HOUR

let timeframeListElement
let modeElement
let inputSearchElement
let timeframeButton
let timeFrameShowed = false

function submitSearch() {
    const input = inputSearchElement.value
    fetch(BASE_URL + '/analyze-keywords?keywords=' + input + '&ignore_neutral=true')
        .then((response) => response.json())
        .then(data => console.log(data));
}

function changeMode() {
    const nextModeNumber = MODES.indexOf(currentMode) + 1
    if (nextModeNumber >= MODES_NUMBER) {
        currentMode = MODES[0]
    } else {
        currentMode = MODES[nextModeNumber]
    }
    setMode(currentMode)
}

function setMode(modeName) {
    currentMode = modeName
    setModeText(modeName)
    checkModeOptions()
    animate()
}

function setModeText(text) {
    modeElement.textContent = text;
}

function animate() {
    modeElement.innerHTML = modeElement.textContent.replace(/\S/g, "<span class='letter'>$&</span>");
    anime.timeline({loop: true})
        .add({
            targets: '#search-mode .letter',
            scale: [0.3, 1],
            opacity: [0, 1],
            translateZ: 0,
            easing: "easeOutExpo",
            duration: 4000,
            delay: (el, i) => 80 * (i + 1)
        })
}

function setTimeframe(timeframe) {
    currentTimeframe = timeframe;
    showTimeframes()
}

function showTimeframes() {
    if (timeFrameShowed) {
        timeframeListElement.style.display = 'none';
    } else {
        timeframeListElement.style.display = 'block';
        timeframeListElement.innerHTML = '';
        for (const timeframe of TIMEFRAMES) {
            const li = document.createElement("li");
            li.appendChild(document.createTextNode(timeframe));
            li.onclick = () => setTimeframe(timeframe)
            timeframeListElement.appendChild(li);
        }
    }
    timeFrameShowed = !timeFrameShowed;
}

function checkModeOptions() {
    if (inputSearchElement.value.length > 0) {
        if (currentMode === RECENT_MODE) {
            inputSearchElement.style.width = '78rem';
            timeframeButton.style.display = 'block';
        } else {
            inputSearchElement.style.width = '84rem';
            timeframeButton.style.display = 'none';
        }
    } else {
        inputSearchElement.style.width = '90rem';
        timeframeButton.style.display = 'none';
    }
}

function checkInput() {
    checkModeOptions()
}

function init() {
    modeElement = document.getElementById('search-mode')
    inputSearchElement = document.getElementById('search')
    timeframeListElement = document.getElementById('timeframes-list')
    timeframeButton = document.getElementById('timeframe-btn')
    setMode(currentMode)
}