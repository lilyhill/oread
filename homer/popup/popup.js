
var uname = document.getElementById('uname').value;
var res = document.getElementById('result');

//Setting base url
var base_url
chrome.storage.sync.get(['base_url'],function(result) {
    base_url = result.base_url
})


function saveData(event) {

    //get element name
    cur_uname = document.getElementById('uname').value
    document.cookie="uname="+cur_uname+";"; //add it to cookie

    //request body
    data = {
        username: cur_uname
    }


    fetch(`${base_url}/saveUsername/`,{
        method: 'POST',
        mode: 'cors',
        cache: 'no-cache',
        credentials: 'same-origin',
        headers: {
          'Content-Type': 'application/json'

        },
        redirect: 'follow',
        referrerPolicy: 'no-referrer',
        body: JSON.stringify(data)
      })
        .then(response => response.json())
        .then( d => {

            uname = cur_uname
            console.log("valid response");
            console.log(d);
            chrome.storage.sync.set({username: uname}, function() {
                console.log('Value is set to ' + uname);
            });

            let url = d.url
            res.innerHTML = `<a href=${url}>${url}</a>`
        }).catch( reason => {
            console.log("error!11")
            console.log(reason)})



    event.preventDefault();

}

function ifUsernamePresentcb (result){

    uname = result.username
    let url = `${base_url}/e/${uname}`
    res.innerHTML = `<a href=${url}>${url}</a>`

}


document.addEventListener('DOMContentLoaded', function(){

    //checking if we already have a username
    chrome.storage.sync.get(['username'], ifUsernamePresentcb)

    document.getElementById('uname-form').addEventListener('submit', (e) => {saveData(e)}, false);

});