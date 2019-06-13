const trafficLight = {
  green: 'Grün',
  yellow: 'Gelb',
  red: 'Rot',
};

const messageType = {
  positive: 'Positive',
  warning: 'Warning',
  negative: 'Negative',
  information: 'Information',
};

const xhr = new XMLHttpRequest();

function el(id) {
  return document.getElementById(id);
}

function clearMessageBox() {
  el('messagebox').innerHTML = '';
}

function addToMessageBox(type, text) {
  const addHtml = `<ui5-messagestrip type="${type}" hide-close-button>\
                   ${text}</ui5-messagestrip>`;
  el('messagebox').innerHTML = el('messagebox').innerHTML + addHtml;
}

function setAnalyzeButtonText(text) {
  el('analyze-button').innerHTML = text;
}

xhr.onerror = function() {
  addToMessageBox(messageType.negative, 'Netzwerkfehler');
};

xhr.onload = function(event) {
  if (this.status !== 200) {
    return;
  }
  const response = JSON.parse(event.target.responseText);
  switch (response.trafficlight) {
    case trafficLight.green:
      addToMessageBox(messageType.positive, 'Alles in Ordnung, keine\
        Unterstützung notwendig');
      break;
    case trafficLight.yellow:
      addToMessageBox(messageType.warning, 'Abweichungen vom Plan vorhanden,\
        aber mit Maßnahmen kann der Plan erreicht werden. Bitte bei der\
        Durchführung unterstützen.');
      break;
    case trafficLight.red:
      addToMessageBox(messageType.negative, 'Abweichungen vom Plan vorhanden,\
        der Plan kann nicht mehr erreicht werden. Sofort bei der Lösungssuche\
        unterstützen, Maßnahmen definieren, oder den Plan anpassen!');
      break;
  }
  addToMessageBox(messageType.information, `Berechneter Fertigstellungsgrad:\
                                            ${response.status}%`);
};

document.addEventListener('DOMContentLoaded', function() {
  el('analyze-button').addEventListener('press', function() {
    clearMessageBox();
    const inputText = el('statustext').value;
    if (inputText.length === 0) {
      addToMessageBox(messageType.negative, 'Status muss gefüllt sein!');
      return;
    }
    setAnalyzeButtonText('Analysiere...');
    const protocol = window.location.protocol;
    const hostname = window.location.hostname;
    const url = `${protocol}//${hostname}/analyze?text=${inputText}`;
    xhr.open('GET', encodeURI(url), true);
    xhr.send();
    setAnalyzeButtonText('Analysieren');
  });
});
