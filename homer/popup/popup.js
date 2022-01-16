

function saveData(event) {
    console.log("$$$$$$$$$$$$$$$")
  document.cookie="uname="+document.getElementById('uname').value+";";
  console.log(document.getElementById('uname').value);
    uname = document.getElementById('uname').value;
    console.log(document.cookie);
   //  chrome.tabs.query({currentWindow: true, active: true}, function (tabs){
   //  var activeTab = tabs[0];
   //  console.log("!!!!!!!")
   //  chrome.tabs.sendMessage(activeTab.id, {"message": "start", "uname":uname});
   // });

    fetch('https://web-romance-raise-occur.trycloudflare.com/saveUsername/',{
        method: "GET"
    }).then(response => console.log("hi"))
    // var req = new XMLhttpRequest();
    // req.method = "GET";
    // req.url = "https://example.com/api?parameter=value";

    //create callback for success containing the response
    // req.success = function(response) {
    //     console.log("response",response);
    // };

    //and a fail callback containing the error
    // req.fail = function(error) {
    //     console.log("error",error);
    // };

    //and finally send it away
    // request.send();

    event.preventDefault();

}


document.addEventListener('DOMContentLoaded', function(){

    document.getElementById('uname-form').addEventListener('submit', (e) => {saveData(e)}, false);

});