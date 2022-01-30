const RECONNECT_TIMEOUT = 2500;

let ws;
const URI = config['server_uri'];

function connectToWebSocket() {
    ws = new WebSocket(URI);

    // Connect to websockets
    ws.addEventListener('open', (event) => {
        console.log("Connected");
    });

    ws.addEventListener('message', (event) => {
        console.log("Message: ", event.data);
        const jsonData = JSON.parse(event.data);

        if (jsonData['message_type'] == 'connection_established') {
            send({
                'action': 'register_transmitter',
                'client_id': tokenInput.value
            })
        } else if (jsonData['message_type'] == 'device_list_update') {
            const devices = jsonData['devices'];
            rebuildClientSelection(devices);
            onReadyToUse();
        }
    });

    ws.addEventListener('close', (event) => {
        console.log("WebSocket close");
        onDisconnected();

        setTimeout(() => {
            console.log("Trying to reconnect...")
            connectToWebSocket()
        }, RECONNECT_TIMEOUT);
    });

    ws.addEventListener('error', (event) => {
        console.log("Websocket error connecting.");
    });
}

function send(sendData) {
    // sendData['client_id'] = clientID; // TODO implement client_id?
    try {
        ws.send(JSON.stringify(sendData));
    } catch (error) {
        console.log("Error when sending via WebSocket", error)
        return false;
    }
    return true;
}

function reconnect() {
    onDisconnected();
    connectToWebSocket();
}


function onReadyToUse() {
    wrapper.classList.remove('disconnected')
}

function onDisconnected() {
    wrapper.classList.add('disconnected');
}
