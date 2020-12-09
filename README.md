# Introduction
**Media Remote** makes it possible to send media key inputs to your PC from any other device via a website. This means that you can use your smartphone as a remote control for your sound system connected to your PC.

# Requirements
**Python**  
The scripts are written in Python therefore Python must be installed on your system. For Linux systems this should already be the case.

Additionally there are some python packages required, which can be installed with 
```
python3 -m pip install -r requirements.txt --user
```

**xdotool**  
The receiver script uses `xdotool` to send keycodes to the pc.

Depending on the linux distribution it can be installed with something along the lines of:

```
sudo apt install xdotool
```

# Workflow
## Receiver
The receiver is your device where your music is playing and which will react to the media key inputs.
To start listening for input you have to start it like this:

```
cd ./src/receiver/
python3 ./receiver.py
```

## Website
Host the `src/website/` anywhere so it exposes the website to the device you want to use as the remote.
The website also works as a Progressive Web App.

When accessing the url via a browser it should look like this:
![Website](documentation/images/Website.png)

## Server
The server serves as a relay server. Its only purpose is to register receivers and send inputs to the correct device.
One server can be used to route multiple receivers. It must be available on an address that the receiver and website can connect to.

Start the server like this: 
```
cd ./src/server/
python3 ./server.py
```

# Configuration
Copy (or rename) the example files to their actual paths
```
cp ./examples/server_config.json ./src/server/config.json 
cp ./examples/receiver_config.json ./src/receiver/config.json 
cp ./examples/website_config.js ./src/website/scripts/config.js 
```

## Receiver
The `token` you use in your `receiver/config.json` must be entered in the website to connect your devices.
The `device` in the config file will be used as the value in the select-field of the website.
Depending on where you host the `server.py` you may have to adjust the `uri` in the config file.

## Website
Depending on where you host the `server.py` you may have to adjust the `URI` in the `src/website/scripts/config.js`.

## Server
The server should run just fine with the default configuration. But if there is a need to define a specific network address or another port, this is possible in `src/server/config.json`. 
