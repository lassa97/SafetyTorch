const URL = 'http://127.0.0.1:5000/check/';
const INCIBE = 'https://www.incibe.es/';

chrome.tabs.onCreated.addListener(async tab => {
    checkConnection(tab.url);
})


chrome.tabs.onUpdated.addListener(async (tabId, changeInfo, tab) => {
    checkConnection(tab.url);
})

async function checkConnection(url) {
    console.log(url);
    let response = await fetch(URL + btoa(url));
    let data = await response.json();

    if (data.blocked) {
        chrome.tabs.update({ url: INCIBE, active: true });
    }
}