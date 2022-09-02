const BASEURL = "http://127.0.0.1:8000/";

chrome.webRequest.onBeforeRequest.addListener(
    function(details) {
        console.log(JSON.stringify(details));
    }
    , {urls: ["<all_urls>"]}, ["requestBody"]
);

async function checkConnection(details) {
    console.log(details);
    let ip = "127.0.0.2";
    let response = await fetch(BASEURL + `check/ip/${ip}`);

    let message = await response.json();

    let warning = document.getElementById("warning");
    let advice = document.getElementById("advice");
    if (message.blocked) {
        warning.innerHTML = `<b>${ip}</b> es peligroso. <br>Categoría: <b>${message.category}</b><sup>1</sup>`;
        advice.innerHTML = `¿Qué es el <a href="https://www.youtube.com/watch?v=uhzV5-iFb5E&list=PLr5GsywSn9d8pUMODmSqxtJ27fGH6N4Z-&index=5" target="_blank">${message.category}</a>?`;
        advice.innerHTML += `<br><br>`
        advice.innerHTML += `[1]: Aparece en la lista <i>${message.blocklist}</i>.`
        document.getElementById("result").innerHTML = "&#10007;";
        document.getElementById("color-box").style.backgroundColor = "#e01818";
        document.getElementsByClassName("notfound-404")[0].style.boxShadow = "0px 0px 0px 10px #e01818 inset, 0px 0px 0px 20px #fff inset";
    }
}

// checkConnection();