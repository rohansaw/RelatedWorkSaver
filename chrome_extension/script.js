async function save() {
    let category = document.getElementById('categoryInput').value
    if (category == "" || category == null){
        category = "none"
    }
    let summary = document.getElementById('summaryInput').value

    var worksheet = document.querySelector('input[name="worksheet"]:checked').value;

    chrome.tabs.query({'active': true, 'windowId': chrome.windows.WINDOW_ID_CURRENT}, function(tabs){
	    var taburl = tabs[0].url;
        let data = new FormData();
        data.append("link", taburl);
        data.append("category", category)
        data.append("worksheet", worksheet)
        if (summary != null && summary != "") {
            data.append("summary", summary)
        }
        fetch('http://127.0.0.1:5000/save-pdf', {
            method: 'POST',
            body: data
        })
       .then(response => response.json())
       .then(data =>  {
            document.getElementById("response").innerHTML = JSON.stringify(data);
        })
    });
}

async function loadWorksheets() {
    let res = await fetch('http://127.0.0.1:5000/worksheets', {
        method: 'GET',
    })
    data = await res.json()
    await chrome.storage.local.set({ "worksheets": data});
    return data
}

function renderWorksheetSelection(worksheets) {
    worksheets.sort(function(a,b) {return ('' + a["title"]).localeCompare(b["title"]);})
    var out = ""
    for (var i = 0; i < worksheets.length; i++) {
        out += `<div class="form-check">
        <input class="form-check-input" type="radio" name="worksheet" id="radio${i}" value="${worksheets[i]["title"]}">
        <label class="form-check-label" for="radio${i}">
            ${worksheets[i]["title"]}
        </label>
        </div>`
    }
    document.getElementById("worksheets").innerHTML = out;
}

function displayAll(worksheets) {
    renderWorksheetSelection(worksheets)
    var btn = document.getElementById("saveBtn");
    btn.addEventListener("click", save);
    document.getElementById("main").classList.remove('d-none');
}

window.onload = function() {
    chrome.storage.local.get(["worksheets"], function(res){
        if (Object.keys(res).length === 0 || res["worksheets"].length == 0){
            loadWorksheets().then((worksheetsNew) => {
                displayAll(worksheetsNew)
            })
        } else {
            displayAll(res["worksheets"])
            loadWorksheets().then((worksheetsNew) => {
                displayAll(worksheetsNew)
            })
        }
    });
};