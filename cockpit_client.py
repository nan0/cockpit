import RPi.GPIO as GPIO
import broadlink
import multiprocessing
import socketio
import time
from wakeonlan import send_magic_packet
import logging

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(2, GPIO.IN)
GPIO.setup(3, GPIO.IN)
GPIO.setup(4, GPIO.IN)
GPIO.setup(17, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(27, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(22, GPIO.OUT, initial=GPIO.LOW)

sio = socketio.Client()
wsUrl = "http://192.168.1.30:8765"

logging.basicConfig(level=logging.INFO)

@sio.event
def connect():
    toggleLed(27, True)

@sio.event
def connect_error(data):
    toggleLed(27, False)
    sio.connect(wsUrl)


@sio.event
def disconnect():
    toggleLed(27, False)


# Switches the tv on or off
def switchTV():
    # Broadlink RM3 mini connexion
    device = broadlink.hello('192.168.1.15')
    device.auth()
    with open("./tv_switch", "rb") as f:  # reading the tv on/off packet from the related file
        packet = f.read()
    device.send_data(packet)


# Wakes up the gaming pc
def wakeUpPC():
    blinkProc = multiprocessing.Process(target=infiniteBlink, args=(27,))
    blinkProc.start()
    macAddr = '50:EB:F6:94:53:01'
    send_magic_packet(macAddr)
    sio.connect(wsUrl)
    blinkProc.terminate()


# Toggles the pc led on or off
def toggleLed(num, on):
    if on:
        GPIO.output(num, GPIO.HIGH)
    else:
        GPIO.output(num, GPIO.LOW)


# Blinks a led
def blinkLed(num, duration=0.2):
    for i in range(3):
        toggleLed(num, True)
        time.sleep(duration)
        toggleLed(num, False)
        time.sleep(duration)


# Blinks a led infinitly
def infiniteBlink(num):
    while True:
        blinkLed(num, 0.05)


# Watching for board I/O
def main():
    while True:
        tvBtnState = GPIO.input(2)
        pcBtnState = GPIO.input(3)
        msfsBtnState = GPIO.input(4)

        if not tvBtnState:
            blinkLed(17)
            switchTV()
            logging.info("Flight simulator TV switched !")
        if not pcBtnState:
            if not sio.connected:
                proc = multiprocessing.Process(target=wakeUpPC)
                proc.start()
            else:
                blinkLed(27)
                toggleLed(27, True)
                sio.emit('STOP_PC')
                logging.info("Flight simulator PC shut down !")
        if not msfsBtnState:
            logging.info('Will start MSFS')

            blinkLed(22)
            sio.emit('START_MSFS')
        time.sleep(0.1)


# Main
if __name__ == "__main__":
    main()
