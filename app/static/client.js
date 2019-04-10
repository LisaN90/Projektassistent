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
                    addToMessageBox('Positive', 'Alles in Ordnung, keine Unterstützung notwendig');
                    break;
                case 'Gelb':
                    addToMessageBox('Warning', 'Abweichungen vom Plan vorhanden, aber mit Maßnahmen kann der Plan erreicht werden. Bitte bei der Durchführung unterstützen.');
                    break;
                case 'Rot':
                    addToMessageBox('Negative', 'Abweichungen vom Plan vorhanden, der Plan kann nicht mehr erreicht werden. Sofort bei der Lösungssuche unterstützen, Maßnahmen definieren, oder den Plan anpassen!');
                    break;
            }
            addToMessageBox('Information', `Berechneter Projektfortschritt: ${response.computed_status}`);
        }
        el('analyze-button').innerHTML = 'Analysieren';
    };
    xhr.send();
}
