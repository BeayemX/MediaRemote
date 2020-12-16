// HTML elements
var clientSelect;
var tokenInput;

function onLoad() {
    //document.body.onclick = (e) => false;
    //document.body.onmousedown = (e) => false;
    document.body.onselectstart = (e) => false;
    document.body.oncontextmenu = (e) => false;

    // Get references to HTML nodes
    clientSelect = document.querySelector('#clientselect');
    tokenInput = document.querySelector('#token');

    // Set default values
    tokenInput.value = localStorage.getItem('token');

    // tokenInput.onkeydown = updateToken;
    tokenInput.onchange = updateToken;
    tokenInput.onblur = updateToken;

    connectToWebSocket();
}

function updateToken(e) {
    localStorage.setItem('token', tokenInput.value);
    reconnect();
}

function makePostRequest(data, callback) {
    clientURL = clientSelect.value;

    if (!clientURL)
        return;

    var xhr = new XMLHttpRequest();
    const isAsync = true;
    xhr.open("POST", "http://" + clientURL + ":7999/post", isAsync);
    xhr.setRequestHeader('Content-Type', 'application/json');

    const response = xhr.send(data);

    xhr.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            const data = JSON.parse(xhr.responseText);
            callback(data);
        }
    }
}

function call(action) {
    const data = {
        action: action,
        target_device: clientSelect.value,
        client_id: tokenInput.value,
        message_type: 'media'
    };

    // console.log(data)
    send(data);
}

function clientAddressChanged(value) {
    console.log("clientAddressChanged", value)
    if (value) {
        console.log("Switching to ", value)
    }
}

function rebuildClientSelection(clients) {
    clientSelect.innerHTML = '';

    if (clients) {
        clients.forEach(device => {
            console.log("Adding device: ", device);
            let opt = document.createElement('option');
            opt.innerText = device;
            opt.setAttribute('value', device)
            clientSelect.appendChild(opt);
        });
    }
}