var newContextItem = {
    "id": "highlightedText",
    "title": "Oread!",
    "contexts": ["selection"],

};
var base_url

chrome.runtime.onInstalled.addListener(
    onInstalledCallback,
)

function onInstalledCallback(details) {

    //setting base url.

    base_url = `https://tunnel.oread.pw`
    chrome.storage.sync.set({base_url: base_url}, function () {
        console.log('base_url is set to ' + base_url);
    });

}

chrome.contextMenus.removeAll(function () {
    chrome.contextMenus.create(newContextItem);
});

chrome.contextMenus.onClicked.addListener(function (info, tab) {
    var currentTime = new Date();
    var uname;
    console.log("time", (currentTime.getTime() / 1000).toFixed(0))
    console.log("selectionText", info.selectionText)
    console.log("url", info.pageUrl)

    chrome.storage.sync.get(['username'], function (result) {
        console.log('Value currently is ' + result.username);
        uname = result.username
        data = {
            username: uname,
            url: info.pageUrl,
            selection: info.selectionText
        }
        console.log({data})


        fetch(`${base_url}/extensionCallback/`, {
            method: 'POST', // *GET, POST, PUT, DELETE, etc.
            mode: 'cors', // no-cors, *cors, same-origin
            cache: 'no-cache', // *default, no-cache, reload, force-cache, only-if-cached
            credentials: 'same-origin', // include, *same-origin, omit
            headers: {
                'Content-Type': 'application/json'
                // 'Content-Type': 'application/x-www-form-urlencoded',
            },
            redirect: 'follow', // manual, *follow, error
            referrerPolicy: 'no-referrer', // no-referrer, *no-referrer-when-downgrade, origin, origin-when-cross-origin, same-origin, strict-origin, strict-origin-when-cross-origin, unsafe-url
            body: JSON.stringify(data) // body data type must match "Content-Type" header
        }).then(response => response.json()).then(d => {
            console.log("got valid response")

        }).catch(reason => {
            console.log("error!11")
            console.log(reason)
        })
    });

})
