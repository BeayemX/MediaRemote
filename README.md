# Introduction
**Media Remote** makes it possible to send media key inputs to your PC from any other device via a website. This means that you can use your smartphone as a remote control for your sound system connected to your PC.


# Workflow
Run `src/receiver/receiver.py` on the PC you want to send the media key commands to.
Host the `src/website/` anywhere so it exposes the website to the device you want to use as the remote.
Run `src/server/server.py` on any PC your receiver and website can connect to.


# Requirements
The receiver uses `xdotool` to send keycodes to the pc.

Depending on the linux distribution it can be installed with something along the lines of:

```
sudo apt install --install xdotool
```

The required python modules can be installed with 
```
python3 -m pip install -r requirements.txt --user
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


# Features
The website also works as a Progressive Web App.
