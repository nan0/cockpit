#!/usr/bin/env python

import subprocess
import os
import asyncio
import websockets
import logging

logging.basicConfig(level=logging.INFO)

pids = []


# Starts MSFS and all its related programs
def toggle_MSFS():
    logging.info('Starting MSFS...')
    global pids
    if pids is None:
        pids = []
        # r"C:\Program Files\MSFS2020 Map Enhancement\MSFS2020 Map Enhancement.exe",
        appPaths = [
            r"C:\Users\nansp\Desktop\SDVfrSimLinkerNext.exe",
            r"C:\Program Files\Air Manager\Bootloader.exe",
            r"D:\msfs\Community\touchingcloud-tools-kineticassistant\Kinetic Assistant.exe",
            r"D:\SteamLibrary\steamapps\common\MicrosoftFlightSimulator\FlightSimulator.exe"]
        for app in appPaths:
            try:
                pid = subprocess.Popen(app, shell=True)
                pids.append(pid)
            except OSError as e:
                logging.warning("Execution failed:", e, file=sys.stderr)
    else:
        logging.info('Killing MSFS...')
        for process in pids:
            process.kill()
        pids = None


# Shuts down the PC
def stop_PC():
    logging.info('Will stop PC')
    return os.system("shutdown /s /t 1")


# Handles every command
async def handle_command(websocket):
    async for cmd in websocket:
        logging.debug(cmd)
        if cmd == 'TOGGLE_MSFS':
            toggle_MSFS()
        elif cmd == 'STOP_PC':
            stop_PC()


# Starts the server
async def main():
    async with websockets.serve(handle_command, "0.0.0.0", 8765):
        logging.debug('Server started !')
        await asyncio.Future()  # run forever


if __name__ == '__main__':
    asyncio.run(main())
