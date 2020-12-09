# System
import asyncio
import json
import time

# Pip
import websockets

# Configuration
with open("config.json") as f:
    config = json.load(f)

URL = config['host']
PORT = config['port']


# Members
open_connections = set()
transmitters_by_client_id = {}

transmitters_by_websocket = {}  # For easier lookup
receivers_by_websocket = {}  # For easier lookup
attempt_ts_by_ip = {}  # Prevent brute-force attempts


# Constants
TYPE_DEVICE_LIST_UPDATE = 'device_list_update'
TYPE_CONNECTION_ESTABLISHED = 'connection_established'
BASE_DELAY = 3


class Transmitter:
    def __init__(self, websocket=None, client_id=None):
        self.websocket = websocket
        self.receivers = {}
        self.client_id = client_id


class Receiver:
    def __init__(self, websocket, device, client_id):
        self.websocket = websocket
        self.device = device  # Device name
        self.client_id = client_id


async def handle_action(websocket, data):
    action = data['action']
    client_id = data['client_id']

    # Prevent brute force attacks
    ip_address = websocket.remote_address[0]
    attempt_ts_by_ip[ip_address] = time.time()

    if action == 'register_transmitter':
        print("Adding transmitter")
        if client_id not in transmitters_by_client_id:
            print("Creating new transmitter")
            transmitters_by_client_id[client_id] = Transmitter()

        transmitter = transmitters_by_client_id[client_id]
        transmitters_by_websocket[websocket] = transmitter
        transmitter.websocket = websocket
        transmitter.client_id = client_id

        await update_devices_for_transmitter(client_id)
    elif action == 'register_receiver':
        device = data['device']
        print(f"Adding receiver: {device}")

        if client_id not in transmitters_by_client_id:
            print("Creating new transmitter")
            transmitters_by_client_id[client_id] = Transmitter()

        receiver = Receiver(websocket, device, client_id)
        receivers_by_websocket[websocket] = receiver

        transmitters_by_client_id[client_id].receivers[device] = receiver
        await update_devices_for_transmitter(client_id)

    else:  # Media action
        target = data['target_device']

        message_type = data['message_type']

        tr = transmitters_by_client_id[client_id]
        receiver = tr.receivers[target]

        await receiver.websocket.send(json.dumps({
            'action': action,
            'message_type': message_type
        }))


async def update_devices_for_transmitter(client_id):
    transmitter = transmitters_by_client_id[client_id]
    websocket = transmitter.websocket

    if websocket:
        devices = [x.device for x in transmitter.receivers.values()]

        await websocket.send(json.dumps({
            'message_type': TYPE_DEVICE_LIST_UPDATE,
            'devices': devices
        }))


async def handle_messages(websocket, path):  # Will be called once per established connection
    try:
        await register(websocket)
        async for message in websocket:
            data = json.loads(message)
            await handle_action(websocket, data)
    except websockets.exceptions.ConnectionClosedOK:
        print("websockets.exceptions.ConnectionClosedOK")
    except asyncio.IncompleteReadError:
        print("IncompleteReadError")
    except websockets.exceptions.ConnectionClosedError:  # Disconnect with error
        print("ConnectionClosedError")
    except websockets.exceptions.ConnectionClosed:  # Disconnect without error
        print("ConnectionClosed")
    finally:
        await unregister(websocket)


# TODO check if only necessary for transmitters?
def should_delay(websocket):
    ip = websocket.remote_address[0]
    if ip in attempt_ts_by_ip:
        last_attempt_ts = attempt_ts_by_ip[ip]

        if time.time() - last_attempt_ts < BASE_DELAY:
            print("Delaying calls")
            return True

    return False


async def register(websocket):
    if should_delay(websocket):
        print("Waiting for delay: ", BASE_DELAY)
        await asyncio.sleep(BASE_DELAY)

    open_connections.add(websocket)

    await websocket.send(json.dumps({
        'message_type': TYPE_CONNECTION_ESTABLISHED
    }))


async def unregister(websocket):
    text = "Unknown device"
    if websocket in transmitters_by_websocket:
        transmitter = transmitters_by_websocket[websocket]
        client_id = transmitter.client_id

        text = f"Transmitter: {transmitter}"
        del transmitters_by_websocket[websocket]

        # Clean transmitter
        transmitter.websocket = None
        transmitter.client_id = None

        # Remove transmitter completely if unused
        if len(transmitter.receivers) == 0:
            print(">>> Removing Transmitter because transmitter left")
            del transmitters_by_client_id[client_id]

    elif websocket in receivers_by_websocket:
        receiver = receivers_by_websocket[websocket]
        client_id = receiver.client_id
        device = receiver.device

        text = f"Receiver: {device}"
        del receivers_by_websocket[websocket]

        transmitter = transmitters_by_client_id[client_id]
        del transmitter.receivers[device]

        if transmitter.websocket is None and len(transmitter.receivers) == 0:
            del transmitters_by_client_id[client_id]
            print(">>> Removing Transmitter because last receiver left")
        else:
            await update_devices_for_transmitter(client_id)

    open_connections.remove(websocket)
    print(f"{text} disconnected")


# Start server loop
print("Starting server on port " + str(PORT))
asyncio.get_event_loop().run_until_complete(websockets.serve(handle_messages, URL, PORT))

print("Server running.")
asyncio.get_event_loop().run_forever()
