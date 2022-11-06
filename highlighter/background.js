/* eslint-disable no-unused-vars */

// NOTE: This file must be in the top-level directory of the extension according to the docs

import {executeInCurrentTab} from './src/background/utils.js';

const DEFAULT_COLOR_TITLE = "yellow";

const base = "https://tunnel.oread.pw";

var uname = "";

setUsername();


// Add option when right-clicking
chrome.runtime.onInstalled.addListener(async () => {
    // remove existing menu items
    chrome.contextMenus.removeAll();

    chrome.contextMenus.create({ title: 'Highlight', id: 'highlight', contexts: ['selection'] });
    chrome.contextMenus.create({ title: 'Toggle Cursor', id: 'toggle-cursor' });
    chrome.contextMenus.create({ title: 'Highlighter color', id: 'highlight-colors' });
    chrome.contextMenus.create({ title: 'Yellow', id: 'yellow', parentId: 'highlight-colors', type: 'radio' });
    chrome.contextMenus.create({ title: 'Blue', id: 'blue', parentId: 'highlight-colors', type: 'radio' });
    chrome.contextMenus.create({ title: 'Green', id: 'green', parentId: 'highlight-colors', type: 'radio' });
    chrome.contextMenus.create({ title: 'Pink', id: 'pink', parentId: 'highlight-colors', type: 'radio' });
    chrome.contextMenus.create({ title: "Dark", id: "dark", parentId: "highlight-colors", type: "radio" });

    // Get the initial selected color value
    const { title: colorTitle } = await getCurrentColor();
    chrome.contextMenus.update(colorTitle, { checked: true });
});

chrome.contextMenus.onClicked.addListener(({ menuItemId, parentMenuItemId }) => {
    if (parentMenuItemId === 'highlight-color') {
        changeColorFromContext(menuItemId);
        return;
    }

    switch (menuItemId) {
        case 'highlight':
            highlightTextFromContext();
            break;
        case 'toggle-cursor':
            toggleHighlighterCursorFromContext();
            break;
    }
});


function setUsername () {
    //setting base url
    chrome.storage.sync.set({baseUrl: base}, (e) => {
        console.log(`base_url is set to ${base}, ${e}`);
    });
    chrome.storage.sync.get(['username'], (e) => {
        uname = e.username;
    });
}


chrome.runtime.onInstalled.addListener(onInstalledCallback);

function onInstalledCallback(details) {
setUsername();
}
chrome.runtime.onStartup.addListener(() => {
setUsername();
});

// Add Keyboard shortcuts
chrome.commands.onCommand.addListener((command) => {
    switch (command) {
        case 'execute-highlight':
            highlightText();
            break;
        case 'toggle-highlighter-cursor':
            toggleHighlighterCursor();
            break;
        case 'change-color-to-yellow':
            changeColor('yellow');
            break;
        case 'change-color-to-cyan':
            changeColor('cyan');
            break;
        case 'change-color-to-lime':
            changeColor('lime');
            break;
        case 'change-color-to-magenta':
            changeColor('magenta');
            break;
        case 'change-color-to-dark':
            changeColor('dark');
            break;
    }
});

// Listen to messages from content scripts
/* eslint-disable consistent-return */
chrome.runtime.onMessage.addListener((request, _sender, sendResponse) => {
    if (!request.action) return;

    switch (request.action) {
        case 'highlight':
            highlightText();
            return;
        case 'track-event':
            return;
        case 'remove-highlights':
            removeHighlights();
            return;
        case 'remove-highlight':
            removeHighlight(request.highlightId);
            return;
        case 'change-color':
            changeColor(request.color);
            return;
        case 'edit-color':
            editColor(request.colorTitle, request.color, request.textColor);
            return;
        case 'toggle-highlighter-cursor':
            toggleHighlighterCursor();
            return;
        case 'get-highlights':
            getHighlights().then(sendResponse);
            return true; // return asynchronously
        case 'get-lost-highlights':
            getLostHighlights().then(sendResponse);
            return true; // return asynchronously
        case 'show-highlight':
            return showHighlight(request.highlightId);
        case 'get-current-color':
            getCurrentColor().then(sendResponse);
            return true; // return asynchronously
        case 'get-color-options':
            getColorOptions().then(sendResponse);
            return true; // return asynchronously
        case 'save-highlight':
            saveHighlight(request).then(sendResponse);
            return true;
        case 'save-url':
            saveUrl(request).then(sendResponse);
            return true;
    }
});
/* eslint-enable consistent-return */

function saveHighlight(request) {

    const data = {
        'highlight': request.data,
        'username' : uname,
    };
    callExtension(data, 'extensionCallback').then((r) => "saved").catch();
    return data;
}

/* eslint-enable consistent-return */
function saveUrl(request) {
    console.log("!!!!!!!!!!!")
    console.log(request.url)
    const data = {
        'url': request.url,
        'username': uname,
    }
    callExtension(data, 'extensionSaveUrl').then((r) => "saved").catch();

    return data;
}



async function callExtension(data, path) {

    const response = await fetch(`${base}/${path}/`, {
        method: 'POST', // *GET, POST, PUT, DELETE, etc.
        mode: 'cors', // no-cors, *cors, same-origin
        cache: 'no-cache', // *default, no-cache, reload, force-cache, only-if-cached
        credentials: 'same-origin', // include, *same-origin, omit
        headers: {
            'Content-Type': 'application/json',
            // 'Content-Type': 'application/x-www-form-urlencoded',
        },
        redirect: 'follow', // manual, *follow, error
        referrerPolicy: 'no-referrer', // no-referrer, *no-referrer-when-downgrade, origin, origin-when-cross-origin, same-origin, strict-origin, strict-origin-when-cross-origin, unsafe-url
        body: JSON.stringify(data), // body data type must match "Content-Type" header
    }).then((backendResponse) => backendResponse.json()).catch((reason) => "backend issue");
    return true;
}

async function getCurrentColor() {
    const { color } = await chrome.storage.sync.get("color");
    const colorTitle = color || DEFAULT_COLOR_TITLE;
    const colorOptions = await getColorOptions();
    return colorOptions.find((colorOption) => colorOption.title === colorTitle);
}

function highlightTextFromContext() {
    highlightText();
}

function toggleHighlighterCursorFromContext() {
    toggleHighlighterCursor();
}

function changeColorFromContext(menuItemId) {
    changeColor(menuItemId);
}

function highlightText() {
    executeInCurrentTab({ file: 'src/contentScripts/highlight.js' });
}

function toggleHighlighterCursor() {
    executeInCurrentTab({ file: 'src/contentScripts/toggleHighlighterCursor.js' });
}

function removeHighlights() {
    executeInCurrentTab({ file: 'src/contentScripts/removeHighlights.js' });
}

function removeHighlight(highlightId) {

    function contentScriptRemoveHighlight(highlightIndex) {
        const highlightError = window.highlighter_lostHighlights.get(highlightIndex);
        clearTimeout(highlightError?.timeout);
        window.highlighter_lostHighlights.delete(highlightIndex);
        removeHighlight(highlightIndex, window.location.hostname + window.location.pathname, window.location.pathname);
    }

    executeInCurrentTab({ func: contentScriptRemoveHighlight, args: [highlightId] });
}

function showHighlight(highlightId) {

    function contentScriptShowHighlight(highlightId) { // eslint-disable-line no-shadow
        const highlightEl = document.querySelector(`[data-highlight-id="${highlightId}"]`);
        if (highlightEl) {
            highlightEl.scrollIntoViewIfNeeded(true);
            const boundingRect = highlightEl.getBoundingClientRect();
            onHighlightMouseEnterOrClick({
                'type': 'click',
                'target': highlightEl,
                'clientX': boundingRect.left + (boundingRect.width / 2),
            });
        }
    }

    executeInCurrentTab({ func: contentScriptShowHighlight, args: [highlightId] });
}

function getHighlights() {
    return executeInCurrentTab({ file: 'src/contentScripts/getHighlights.js' });
}

function getLostHighlights() {
    function contentScriptGetLostHighlights() {
        const lostHighlights = [];
        window.highlighter_lostHighlights.forEach((highlight, index) => lostHighlights.push({ string: highlight?.string, index }));
        return lostHighlights;
    }

    return executeInCurrentTab({ func: contentScriptGetLostHighlights });
}

function changeColor(colorTitle) {
    if (!colorTitle) return;

    chrome.storage.sync.set({ color: colorTitle });

    // Also update the context menu
    chrome.contextMenus.update(colorTitle, { checked: true });
}

async function editColor(colorTitle, color, textColor) {

    const colorOptions = await getColorOptions();
    const colorOption = colorOptions.find((option) => option.title === colorTitle);
    colorOption.color = color;
    colorOption.textColor = textColor;

    if (!textColor) {
        delete colorOption.textColor;
    }

    chrome.storage.sync.set({ colors: colorOptions });
}

function getColorOptions() {
    return new Promise((resolve, _reject) => {
        chrome.storage.sync.get({
            colors: [ // Default value
                {
                    title: 'yellow',
                    color: 'rgb(255, 246, 21)',
                },
                {
                    title: 'green',
                    color: 'rgb(68, 255, 147)',
                },
                {
                    title: 'blue',
                    color: 'rgb(66, 229, 255)',
                },
                {
                    title: 'pink',
                    color: 'rgb(244, 151, 255)',
                },
                {
                    title: 'dark',
                    color: 'rgb(52, 73, 94)',
                    textColor: 'rgb(255, 255, 255)',
                },
            ],
        }, ({ colors }) => resolve(colors));
    });
}
