let color = '#3aa757';

console.log(chrome.runtime.getURL('logo.png'));


chrome.runtime.onInstalled.addListener(e => {
  console.log("!!!!")

})

