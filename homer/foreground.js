var txt = ''

// window.onmouseup = function getSelectedText() {
//   if (window.getSelection) {
//       txt = window.getSelection().toString();
//       url = window.location.href
//   }
//
//   chrome.runtime.sendMessage(txt)
//   console.log("$$$$$$$",txt)
//     console.log(url)
// }

chrome.runtime.onMessage.addListener(
      function(request, sender, sendResponse) {
        if( request.message === "start" ) {
            console.log("%%%%%%%%%")
             }
      }
    );

function start(){
    alert("started");
}