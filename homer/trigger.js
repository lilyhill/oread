console.log('debugg works!!')
var txt = ''
window.onmouseup = function getSelectedText() {
  if (window.getSelection) {
      txt = window.getSelection().toString();
  } 
  chrome.runtime.sendMessage(txt)
  console.log(txt)
}

// chrome.tabs.sendMessage(txt)