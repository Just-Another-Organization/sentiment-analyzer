const BASE_URL = window.location.origin + '/api/v1'

RECENT_MODE = 'recent'
POPULAR_MODE = 'popular'

MODES = [
    RECENT_MODE,
    POPULAR_MODE
]

NO_TIMEFRAME = 'None'
ONE_HOUR = '1h'
TWO_HOURS = '2h'
FOUR_HOURS = '4h'
SIX_HOURS = '6h'
EIGHT_HOURS = '8h'
TWELVE_HOURS = '12h'
EIGHTEEN_HOURS = '18h'
ONE_DAY = '1d'
TWO_DAYS = '2d'
THREE_DAYS = '3d'
FOUR_DAYS = '4d'
FIVE_DAYS = '5d'
SIX_DAYS = '6d'
A_WEEK = '1w'
TWO_WEEKS = '2w'

DEFAULT_TIMEFRAME = ONE_HOUR

TIMEFRAMES = [
    ONE_HOUR,
    TWO_HOURS,
    FOUR_HOURS,
    SIX_HOURS,
    EIGHT_HOURS,
    TWELVE_HOURS,
    EIGHTEEN_HOURS,
    ONE_DAY,
    THREE_DAYS,
    FIVE_DAYS,
    A_WEEK,
    TWO_WEEKS,
]

let currentMode = RECENT_MODE
const MODES_NUMBER = MODES.length;
let currentTimeframe = ONE_HOUR

let intervalListElement
let intervalPickerElement
let modeElement
let inputSearchElement
let chipsWrapperElement
let messagesWrapperElement
let helpWrapperElement
let intervalButton
let ignoreNeutralButton
let combineButton
let helpButton
let helpShowed = false
let timeFrameShowed = false
let ignoreNeutralOption = false
let combineOption = false
let keywords = []

function submitSearch() {
    const input = inputSearchElement.value.trim()
    let query = ''

    if (keywords.length > 0) {
        query = keywords[0]
        for (let i = 1; i < keywords.length; i++) {
            const keyword = keywords[i]
            query += ',' + keyword
        }
    }

    if (input.length > 0) {
        if (combineOption) {
            query += ' ' + input
        } else if (keywords.length > 0) {
            query += ',' + input
        } else {
            query += input
        }
    }

    query = query.trim()
    if (query.length <= 0) {
        showError('Please insert a valid input')
        return false
    }

    cleanMessages()
    showInfo('Searching')
    let url = BASE_URL
        + '/analyze-keywords?keywords=' + encodeURIComponent(query)
        + '&ignore_neutral=' + ignoreNeutralOption
        + '&combine=' + combineOption

    if (currentTimeframe !== NO_TIMEFRAME) {
        url += '&interval=' + currentTimeframe
    }

    fetch(url)
        .then((response) => {
            if (!response.ok) {
                if (response.status === 429) {
                    showError('Request limit reached, try again later.')
                } else {
                    showError('No data available. Try different topics, time interval or sentiment mode.')
                }
                return false
            }
            return response.json()
        })
        .then(data => showResult(data.result))
        .catch()
}

function showInfo(text) {
    showMessage(text, 'info-message')
}

function showError(text) {
    showMessage(text, 'error-message')
}

function showResult(result) {
    let resultMessage = ''
    for (const key of Object.keys(result)) {
        const value = result[key].charAt(0).toUpperCase() + result[key].substr(1).toLowerCase();
        resultMessage += key + ': ' + value + ' '
    }
    showInfo(resultMessage)
    highlight()
}

function showMessage(text, type) {
    cleanMessages()
    messagesWrapperElement.style.display = 'flex'
    const chip = document.createElement("div");
    chip.appendChild(document.createTextNode(text));
    chip.classList.add('message')
    chip.classList.add(type)
    messagesWrapperElement.appendChild(chip)
}

function cleanMessages() {
    messagesWrapperElement.innerHTML = ''
    messagesWrapperElement.style.display = 'none'
}

function highlight() {
    const words = messagesWrapperElement.innerText.split(" ");
    messagesWrapperElement.innerHTML = '';
    const paragraph = document.createElement("p");
    words.forEach((word) => {
        const span = document.createElement('span');
        switch (word) {
            case 'Negative':
                span.classList.add('negative');
                span.textContent += word;
                break;
            case 'Neutral':
                span.classList.add('neutral');
                span.textContent += word;
                break;
            case 'Positive':
                span.classList.add('positive');
                span.textContent += word;
                break;
            case 'No_data_available':
                span.classList.add('no-data-available');
                word = "No data available"
                span.textContent += word;
                break;
            default:
                word = word + ' '
                break
        }
        if (span.textContent.length > 0) {
            paragraph.appendChild(span)
            const linebreak = document.createElement("br");
            paragraph.appendChild(linebreak)
        } else {
            const node = document.createTextNode(word);
            paragraph.appendChild(node)
        }
    })
    messagesWrapperElement.classList.add('message')
    const newLine = paragraph.querySelectorAll('br');
    paragraph.removeChild(newLine[newLine.length - 1]);
    messagesWrapperElement.appendChild(paragraph)
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

function showHelp(status = null) {
    if (status) {
        helpShowed = status
    } else {
        helpShowed = !helpShowed
    }
    if (helpShowed) {
        helpWrapperElement.style.display = 'flex';
        helpButton.classList.add('active-btn')
    } else {
        helpWrapperElement.style.display = 'none';
        helpButton.classList.remove('active-btn')
    }
}

function setIgnoreNeutralOption(status = null) {
    if (!status) {
        status = !ignoreNeutralOption
    }
    ignoreNeutralOption = status
    if (ignoreNeutralOption) {
        ignoreNeutralButton.classList.add('active-btn')
    } else {
        ignoreNeutralButton.classList.remove('active-btn')
    }
}

function setCombineOption(status = null) {
    if (!status) {
        status = !combineOption
    }
    combineOption = status
    if (combineOption) {
        combineButton.classList.add('active-btn')
    } else {
        combineButton.classList.remove('active-btn')
    }
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

function setTimeframe(interval) {
    currentTimeframe = interval;
    showTimeframes(false)
}

function showTimeframes(status = null) {
    if (timeFrameShowed || status === false) {
        intervalListElement.style.display = 'none';
        intervalPickerElement.style.display = 'none';
    } else {
        intervalListElement.style.display = 'flex';
        intervalPickerElement.style.display = 'block';
        intervalListElement.innerHTML = '';
        for (const interval of TIMEFRAMES) {
            const li = document.createElement("li");
            li.classList.add('interval-item')

            if (interval === currentTimeframe) {
                li.classList.add('active-interval')
            }
            li.appendChild(document.createTextNode(interval));
            li.onclick = () => setTimeframe(interval)
            intervalListElement.appendChild(li);
        }
    }
    timeFrameShowed = !timeFrameShowed;
}

function checkModeOptions() {
    if (inputSearchElement.value.length > 0 || keywords.length > 0) {
        if (currentMode === RECENT_MODE) {
            setRecentInputMode()
            intervalButton.style.display = 'block';
            setTimeframe(ONE_HOUR)
        } else {
            setPopularInputMode()
            intervalButton.style.display = 'none';
            setTimeframe(NO_TIMEFRAME)
        }
    } else {
        setUnsearchableInputMode()
        intervalButton.style.display = 'none';
        setTimeframe(NO_TIMEFRAME)
    }
}

function checkInput() {
    const value = inputSearchElement.value
    if (value.trim() === '' || value[value.length - 1] === ' ') {
        if (value[value.length - 1] === ' ') {
            inputSearchElement.value = value.trim() + ' '
        }
        return false
    }
    checkModeOptions()
    checkChips()
}

function setUnsearchableInputMode() {
    inputSearchElement.style.width = '90rem'
}

function setPopularInputMode() {
    inputSearchElement.style.width = '84rem'
}

function setRecentInputMode() {
    inputSearchElement.style.width = '78rem'
}

function checkChips() {
    let input = inputSearchElement.value
    input = input.trim()
    const chips = input.split(',');

    if (chips[chips.length - 1].length <= 0) {
        chips.pop()
    }

    if (input && input[input.length - 1].length > 0 && input[input.length - 1] !== ',') {
        inputSearchElement.value = chips[chips.length - 1]
        chips.pop();
    } else {
        inputSearchElement.value = ''
    }

    for (const chip of chips) {
        if (chip.length > 0) {
            createChip(chip.trim())
        }
    }
}

function removeChip(keyword) {
    const position = keywords.indexOf(keyword)
    chipsWrapperElement.removeChild(chipsWrapperElement.children[position]);
    keywords.splice(position, 1)
    checkModeOptions()
}

function createChip(text) {
    keywords.push(text)
    chipsWrapperElement.innerHTML = ''
    if (keywords.length > 0) {
        chipsWrapperElement.style.display = 'flex'
        for (const keyword of keywords) {
            const chip = document.createElement("div");
            chip.appendChild(document.createTextNode(keyword));
            chip.classList.add('chip')
            chip.onclick = () => removeChip(keyword)
            chipsWrapperElement.appendChild(chip)
        }
    }
}

function init() {
    modeElement = document.getElementById('search-mode')
    inputSearchElement = document.getElementById('search')
    intervalListElement = document.getElementById('intervals-list')
    intervalPickerElement = document.getElementById('intervals-picker')
    intervalButton = document.getElementById('interval-btn')
    ignoreNeutralButton = document.getElementById('ignore-neutral-btn')
    combineButton = document.getElementById('combine-btn')
    helpButton = document.getElementById('help-btn')
    chipsWrapperElement = document.getElementById('chips-wrapper')
    messagesWrapperElement = document.getElementById('messages-wrapper')
    helpWrapperElement = document.getElementById('help-wrapper')
    setMode(currentMode)
    setIgnoreNeutralOption(true)
}