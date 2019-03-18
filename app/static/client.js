const el = x => document.getElementById(x);

document.addEventListener('DOMContentLoaded', function() {
    el('analyze-button').addEventListener('press', function(oEvent) {
        analyze();
    });
});

function clearMessageBox() {
    el('messagebox').innerHTML = '';
}

function addToMessageBox(messageType, messageText) {
    const messageStripText = `<ui5-messagestrip type="${messageType}" style="margin-bottom: 0.5rem" hide-close-button>${messageText}</ui5-messagestrip>`;
    el('messagebox').innerHTML = el('messagebox').innerHTML + messageStripText;
}

function analyze() {
    const inputTitle = el('title').value;
    const inputText = el('statustext').value;
    clearMessageBox();
    if (inputTitle.length === 0 || inputText.length === 0) {
        addToMessageBox('Negative', 'Titel und Status müssen gefüllt sein!');
        return;
    }
    el('analyze-button').innerHTML = 'Analysiere...';
    const xhr = new XMLHttpRequest();
    const loc = window.location;
    var url = '';
    if (loc.hostname === '') { // used for local development
        url = encodeURI(`https://projektassistent-af.onrender.com/analyze?title=${inputTitle}&text=${inputText}`);
    } else {
        url = encodeURI(`${loc.protocol}//${loc.hostname}/analyze?title=${inputTitle}&text=${inputText}`);
    }
    xhr.open('GET', url, true);
    xhr.onerror = function() {alert (xhr.responseText);}
    xhr.onload = function(e) {
        console.log('--this');
        console.log(this);
        if (this.readyState === 4 && this.status === 200) {
            console.log('--responseText: '); console.log(e.target.responseText);
            const response = JSON.parse(e.target.responseText);
            switch (response.computed_trafficlight) {
                case 'Grün':
                    addToMessageBox('Positive', 'Projekt läuft positiv');
                    break;
                case 'Gelb':
                    addToMessageBox('Warning', 'Projekt läuft mit Warungen');
                    break;
                case 'Rot':
                    addToMessageBox('Negative', 'Projekt läuft schlecht');
                    break;
            }
            addToMessageBox('Information', `Berechneter Projektfortschritt: ${response.computed_status}`);
        }
        el('analyze-button').innerHTML = 'Analysieren';
    }
    xhr.send();
}