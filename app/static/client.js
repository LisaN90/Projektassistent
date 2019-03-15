var el = x => document.getElementById(x);

function analyze() {
    var title = el('title').value;
    var statustext = el('statustext').value;
    text = title + " " + statustext
    el('analyze-button').innerHTML = 'Analysiere...';
    var xhr = new XMLHttpRequest();
    var loc = window.location
    xhr.open('POST', `${loc.protocol}//${loc.hostname}:${loc.port}/analyze`, true);
    xhr.onerror = function() {alert (xhr.responseText);}
    xhr.onload = function(e) {
        if (this.readyState === 4) {
            var response = JSON.parse(e.target.responseText);
            el('status-label').innerHTML = `Result = ${response['result_status']}`;
            el('ampel-label').innerHTML = `Result = ${response['result_ampel']}`;
        }
        el('analyze-button').innerHTML = 'Analysiere...';
    }
    xhr.send(text);
}

