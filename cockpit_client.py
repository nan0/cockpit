import asyncio
import logging
import multiprocessing
import time
import RPi.GPIO as GPIO
import broadlink
import websockets
from wakeonlan import send_magic_packet

TV_LED = 17
TV_BTN = 2
PC_LED = 27
PC_BTN = 3
MSFS_LED = 22
MSFS_BTN = 4
WS_URL = "ws://192.168.1.30:8765"

GPIO.setmode(GPIO.BCM)
GPIO.setup(TV_BTN, GPIO.IN)
GPIO.setup(PC_BTN, GPIO.IN)
GPIO.setup(MSFS_BTN, GPIO.IN)
GPIO.setup(TV_LED, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(PC_LED, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(MSFS_LED, GPIO.OUT, initial=GPIO.LOW)

logging.basicConfig(level=logging.INFO)


# Toggles the tv on or off
def toggle_tv(channel):
    logging.info("Connecting to the broadlink mini...")
    blink_led(TV_LED)

    # Broadlink RM3 mini connexion
    device = broadlink.hello('192.168.1.15')
    device.auth()
    with open("./tv_switch", "rb") as f:  # reading the tv on/off packet from the related file
        packet = f.read()
    device.send_data(packet)

    logging.info("TV toggled !")


# Toggles the PC on or off
def toggle_pc(channel):
    blink_led(PC_LED)
    logging.info("Checking the PC power status...")
    is_up = asyncio.run(send_message('DUMMY'))
    if not is_up:
        logging.info("PC is off. Starting it...")
        blink_led(PC_LED, 1)
        mac_addr = '50:EB:F6:94:53:01'
        send_magic_packet(mac_addr)
    else:
        logging.info("PC is on. Stopping it...")
        blink_led(PC_LED, 1)
        asyncio.run(send_message('STOP_PC'))


# Sends a message to make the server toggle MSFS
def toggle_msfs(channel):
    logging.info('Will toggle MSFS')
    blink_led(MSFS_LED)
    asyncio.run(send_message('TOGGLE_MSFS'))


# Blinks LED in another process (doesn't block the main thread)
def blink_led(num, duration=0.1):
    def blink_sync(num, duration=0.1):
        for i in range(3):
            GPIO.output(num, GPIO.HIGH)
            time.sleep(duration)
            GPIO.output(num, GPIO.LOW)
            time.sleep(duration)

    blink_proc = multiprocessing.Process(target=blink_sync, args=(num, duration))
    blink_proc.start()


# Sends a message to the server via the websocket
async def send_message(message):
    try:
        async with websockets.connect(WS_URL, open_timeout=2, close_timeout=1) as websocket:
            await websocket.send(message)
            return True
    except:
        return False


# Main
if __name__ == "__main__":
    try:
        GPIO.add_event_detect(TV_BTN, GPIO.RISING, callback=toggle_tv, bouncetime=1000)
        GPIO.add_event_detect(PC_BTN, GPIO.RISING, callback=toggle_pc, bouncetime=1000)
        GPIO.add_event_detect(MSFS_BTN, GPIO.RISING, callback=toggle_msfs, bouncetime=1000)
        while True:
            pass
    except:
        logging.error("Main loop stopped")
    finally:
        logging.error("Cleaning up GPIO")
        GPIO.cleanup()
