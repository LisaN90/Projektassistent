var el = x => document.getElementById(x);

function showPicker(inputId) { el('file-input').click(); }

function showPicked(input) {
    el('upload-label').innerHTML = input.files[0].name;
    var reader = new FileReader();
    reader.onload = function (e) {
        el('image-picked').src = e.target.result;
        el('image-picked').className = '';
    }
    reader.readAsDataURL(input.files[0]);
}

function analyze() {
    var title = el('title').innerText;
    var statustext = el('statustext').innerText;
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
        el('analyze-button').innerHTML = 'Analyze';
    }
}

