var newContextItem = {
  "id": "highlightedText",
  "title": "Oread!",
  "contexts": ["selection"],

};

chrome.contextMenus.create(newContextItem);

chrome.contextMenus.onClicked.addListener(function(info,tab){
  var currentTime = new Date();
  console.log("time",(currentTime.getTime()/1000).toFixed(0))
  console.log("selectionText", info.selectionText)
  console.log("url",info.pageUrl)
})
