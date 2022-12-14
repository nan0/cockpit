# Home flight simulator cockpit

## Architecture
![Architecture](https://drive.google.com/uc?export=view&id=1HWA0QZlIibJhXi94NdxQkQTR877IzZA3)

## Development Configuration
- The client and server script are developed in remote (SFTP) from PyCharm
- Both client and server are in the same github repo : [nan0/cockpit (github.com)](https://github.com/nan0/cockpit)
- Venv 
  - RPi.GPIO cannot be installed. Maybe try that later: [GPIOSimulator · PyPI](https://github.com/nan0/cockpit)
  - Save requirements : pip freeze > requirements.txt
  - Install requirements:
  - on Pi: : sudo python3 -m pip install -r /home/nan0/cockpit/requirements.txt
  - Python venv tuto [here](https://www.javatpoint.com/how-to-create-requirements-txt-file-in-python)
  - Mayb try [PyWebOSTV](https://github.com/supersaiyanmode/PyWebOSTV) to control TVs

## Pi Configuration
- python client located in /home/nan0/cockpit/cockpit.py (with wol byte file alongside)
- A systemd service starts automatically with the pi
 - location /etc/systemd/system/cockpit.service
 - usage : sudo systemctl [start | stop | restart] cockpit.service
 - log: journalctl -f -u cockpit.service -p info (ctrl+c to exit)
 - if service file is updated, run : sudo systemctl daemon-reload
 - Systemd tuto [here](https://medium.com/codex/setup-a-python-script-as-a-service-through-systemctl-systemd-f0cc55a42267)

## Gaming PC Configuration
- python server located in startup scripts (windows+r and shell:startup)
- Task Scheduler will start automatically the python server
  - Task name : "Start cockpit"
  - To open task scheduler : win + r / taskschd.msc
  - The task is visible in the "Display active tasks" dection
- Incoming / Outgoing port 8765 open in windows firewall
- nansp user is automatically connected

## Broadlink configuration
 - Using the [repo's](https://github.com/mjg59/python-broadlink) doc works fine 
 - Connect the broadlink to the wifi network with the Android app
 - / ! \ Unlock the RM3 from the app, otherwise the auth() function will not work. Toggle the related switch in the device properties
 - Follow the documenttion to learn and discover devices
 
## Web sockets events:
| Command     | Description              |
|-------------|--------------------------|
| TOGGLE_MSFS | *Toggles MSFS on or off* |
| STOP_PC     | *Shutdowns the PC*       |

## CLI
To use the commands in "one shot", a CLI is available for every action.

```sudo python3 cockpit_client.py toggle [tv|pc|msfs]```

Without argument, the script will serve and listen to the Pi GPIO.

## TODO List
 - Stop / Start MSFS with [steamcmd](https://developer.valvesoftware.com/wiki/SteamCMD)
