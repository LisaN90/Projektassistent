const el = (x) => document.getElementById(x);

document.addEventListener('DOMContentLoaded', function() {
    el('analyze-button').addEventListener('press', function(oEvent) {
        analyze();
    });
});

function clearMessageBox() {
    el('messagebox').innerHTML = '';
}

function addToMessageBox(messageType, messageText) {
    const messageStripText = `<ui5-messagestrip type="${messageType}" hide-close-button>${messageText}</ui5-messagestrip>`;
    el('messagebox').innerHTML = el('messagebox').innerHTML + messageStripText;
}

function analyze() {
    const inputText = el('statustext').value;
    clearMessageBox();
    if ( inputText.length === 0) {
        addToMessageBox('Negative', 'Status muss gefüllt sein!');
        return;
    }
    el('analyze-button').innerHTML = 'Analysiere...';
    const xhr = new XMLHttpRequest();
    const loc = window.location;
    const url = encodeURI(`${loc.protocol}//${loc.hostname}/analyze?text=${inputText}`);
    xhr.open('GET', url, true);
    xhr.onerror = function() {
        alert(xhr.responseText);
    };
    xhr.onload = function(e) {
        if (this.readyState === 4 && this.status === 200) {
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
    };
    xhr.send();
}
