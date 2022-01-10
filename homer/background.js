
var newContextItem = {
  "id": "highlightedText",   // <-- mandatory with event-pages
  "title": "my_Note!",
  "contexts": ["selection"],

};

chrome.contextMenus.create(newContextItem);

chrome.contextMenus.onClicked.addListener(function(info,tab){
  console.log(info.selectionText)
  console.log(info.pageUrl)
})

