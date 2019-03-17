const el = x => document.getElementById(x);

function analyze() {
    const inputTitle = el('title').value;
    const inputText = el('statustext').value;
    if (inputTitle.length === 0 || inputText.length === 0) {
        alert('Titel und Status müssen gefüllt sein!');
        return;
    }
    el('analyze-button').innerHTML = 'Analysiere...';
    const xhr = new XMLHttpRequest();
    const loc = window.location;
	const url = encodeURI(`${loc.protocol}//${loc.hostname}/analyze?title=${inputTitle}&text=${inputText}`);
    xhr.open('GET', url, true);
    xhr.onerror = function() {alert (xhr.responseText);}
    xhr.onload = function(e) {
		console.log('--this');
		console.log(this);
        if (this.readyState === 4 && this.status === 200) {
            console.log('--responseText: '); console.log(e.target.responseText);
            const response = JSON.parse(e.target.responseText);
            el('status').innerHTML = response.computed_status;
			switch (response.computed_trafficlight) {
				case 'Grün':
					el('traffic-light').src = '../static/Green.png';
					break;
				case 'Gelb':
					el('traffic-light').src = '../static/Yellow.png';
					break;
				case 'Rot':
					el('traffic-light').src = '../static/Red.png';
					break;
			}
			el('results').style.visibility = 'visible';
        }
        el('analyze-button').innerHTML = 'Analysieren';
    }
    xhr.send();
}
