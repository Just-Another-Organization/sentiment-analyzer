RECENT_MODE = 'recent'
POPULAR_MODE = 'popular'

MODES = [
    RECENT_MODE,
    POPULAR_MODE
]

let currentMode = RECENT_MODE
const MODES_NUMBER = MODES.length;
let modeElement
let inputSearchElement
const BASE_URL = window.location.origin + '/api'

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
    animate()
}

function setModeText(text) {
    modeElement.textContent = text;
}

function init() {
    modeElement = document.getElementById('search-mode')
    inputSearchElement = document.getElementById('search')
    setMode(currentMode)
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