import time
import json
import asyncio

# Pip modules
import websockets

# Custom modules
from media import controller as media

RECONNECT_TIME = 5

# Message constants
MEDIA_CONTROL = 'media'

# Configuration
with open("config.json") as f:
    config = json.load(f)

URI = config['uri']
TOKEN = config['token']
DEVICE = config['device']
DEBUG = config['debug']

print(f"Connecting to '{URI}'")
print(f"Starting as '{DEVICE}', listening for '{TOKEN}'")


def handle_action(data):
    if DEBUG:
        print("handle_action", json.dumps(data, indent=2))
    message_type = data['message_type']

    if message_type == MEDIA_CONTROL:
        action = data['action']

        if action.startswith('_'):
            return json.dumps({
                "error": 1,
                "message": f"Function '{action}' does not exist"
            })

        if hasattr(media, action):
            func = getattr(media, action)
            func()
        else:
            print(f"Media action '{action}' does not exist")

        return json.dumps({
            "error": 0,
            "message": "Passed"
        })
    else:
        print('Unhandled message:')
        print(json.dumps(data))

async def register(websocket):
    await websocket.send(json.dumps({
        'action': "register_receiver",
        'client_id': TOKEN,
        'device': DEVICE
    }))

async def main():
    async with websockets.connect(URI) as websocket:
        await register(websocket)

        while True:
            msg = await websocket.recv()
            data = json.loads(msg)
            handle_action(data)

while True:
    try:
        asyncio.get_event_loop().run_until_complete(main())
    except ConnectionRefusedError:
        print("Connection refused", time.time())
        time.sleep(RECONNECT_TIME)
    except Exception as e:
        print(e)
