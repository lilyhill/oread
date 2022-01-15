console.log('debugg works!!')
var txt = ''

window.onmouseup = function getSelectedText() {
  if (window.getSelection) {
      txt = window.getSelection().toString();
      url = window.location.href
  }

  chrome.runtime.sendMessage(txt)
  console.log("$$$$$$$",txt)
    console.log(url)
}

searchUrbanDict = function(word){
    var query = word.selectionText;
    chrome.tabs.create({url: "http://www.urbandictionary.com/define.php?term=" + query});
 };

chrome.contextMenus.create({
 title: "Search in UrbanDictionary",
 contexts:["selection"],  // ContextType
 onclick: searchUrbanDict // A callback function
});