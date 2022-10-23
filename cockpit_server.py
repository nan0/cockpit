#!/usr/bin/env python

import subprocess
import os
import asyncio
import websockets
import logging

logging.basicConfig(level=logging.INFO)

msfs_running = False


# Starts MSFS and all its related programs
def toggle_MSFS():
    global msfs_running
    if not msfs_running:
        logging.info('Starting MSFS...')

        mods = [
            r"C:\Program Files\Air Manager\Bootloader.exe",
            r"C:\Program Files (x86)\FSRealistic\FSRealistic.exe",
            r"D:\msfs\Community\touchingcloud-tools-kineticassistant\Kinetic Assistant.exe",
            r"C:\Users\nansp\cockpit\SDVfrSimLinkerNext.exe",
            r"C:\Program Files\MSFS2020 Map Enhancement\MSFS2020 Map Enhancement.exe",
        ]

        for mod in mods:
            subprocess.Popen(mod, shell=True)

        # Removing the MSFS lock file that shows the warning on startup
        lock_file = "C:\\Users\\nansp\\AppData\\Roaming\\Microsoft Flight Simulator\\running.lock"
        if os.path.isfile(lock_file):
            os.remove(lock_file)

        # Starting MSFS through steam (also avoids the warning message)
        os.system("start \"\" steam://rungameid/1250410")
        msfs_running = True
    else:
        logging.info('Stopping MSFS...')
        processNames = ["SDVfrSimLinkerNext.exe", "javaw.exe", "Kinetic Assistant.exe",
                        "FlightSimulator.exe", "FSRealistic.exe", "MSFS2020 Map Enhancement.exe"]
        for process in processNames:
            os.system('taskkill /f /im  "' + process + '"')
        msfs_running = False


# Shuts down the PC
def stop_PC():
    logging.info('Will stop PC')
    return os.system("shutdown /s /t 1")


# Handles every command
async def handle_command(websocket):
    async for cmd in websocket:
        if cmd == 'TOGGLE_MSFS':
            toggle_MSFS()
        elif cmd == 'STOP_PC':
            stop_PC()


# Starts the server
async def main():
    async with websockets.serve(handle_command, "0.0.0.0", 8765):
        logging.debug('Server started !')
        await asyncio.Future()  # run forever


asyncio.run(main())
