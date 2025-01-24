#!/usr/bin/python3
import serial
import time
import brickpi3

BP = brickpi3.BrickPi3()
BP.set_sensor_type(BP.PORT_3, BP.SENSOR_TYPE.EV3_COLOR_COLOR)

# colors = ['none', 'Black', "Blue", 'Green', 'Yellow', 'Red', 'White', 'Yellow']
colors = ['none', 'Black', "Blue", 'Green', 'Yellow', 'Red', 'White', 'Brown']

ser = None

def initSerComm(baudRate):
    global ser
    port = "/dev/ttyUSB0"
    ser = serial.Serial(port, baudrate=baudRate, timeout=2)
    print("*** Press the GREEN button to start the robot ***")

    # wait to give time to press button
    time.sleep(2)

    while True:
        print("--- Sending out handshaking signal ---")
        ack = cmdSend(ser, 0)

        # not received any msg
        if not ack:
            print("*** Try again ***")
            print("*** Press the GREEN button to start the robot ***")

        # received msg
        else:
            print("!!! Connected to the robot !!!")
            ser.readall()
            break

def cmdSend(cmd, arg = None):
    global ser
    if(arg is not None):
        msg = str(cmd) + str(arg) + "\n"
    else:
        msg = str(cmd) + "\n"

    attempt = 0

    while attempt < 5:
        ser.write(msg.encode())
        ack_origin = ser.readline()

        if ack_origin:  # If data is received
            ack = ack_origin[:-2].decode("utf-8")
            return ack

        # If no data received, wait and retry
        attempt += 1
        print("Failed to connect, retrying in 1 second...")
        time.sleep(1)

    raise serial.SerialException("No data received from device after multiple attempts.")

def moveForward(power = 0):
    attempt = 0
    while attempt < 3:
        ack = cmdSend(1, power)
        if ack:
            # print("Move forward successful\n")
            return
        else:
            print("Failed to move forward, attempting again...\n")
            attempt += 1

def turnLeft(power = 0):
    attempt = 0
    while attempt < 3:
        ack = cmdSend(2, power)
        if ack:
            # print("Turn left successful\n")
            return
        else:
            print("Failed to turn left, attempting again...\n")
            attempt += 1

def turnRight(power = 0):
    attempt = 0
    while attempt < 3:
        ack = cmdSend(3, power)
        if ack:
            # print("Turn right successful\n")
            return
        else:
            print("Failed to turn right, attempting again...\n")
            attempt += 1

def moveBack(power = 0):
    attempt = 0
    while attempt < 3:
        ack = cmdSend(4, power)
        if ack:
            # print("Move back successful\n")
            return
        else:
            print("Failed to move back, attempting again...\n")
            attempt += 1

def brake():
    attempt = 0
    while attempt < 3:
        ack = cmdSend(5)
        if ack:
            # print("Brake successful\n")
            return
        else:
            print("Failed to brake, attempting again...\n")
            attempt += 1

def readSonicPortCM(port):
    attempt = 0
    while attempt < 3:
        ack = cmdSend(6, port)
        if ack:
            # print("Distance (CM): " + ack)
            return ack
        else:
            print("Failed to read sonic port" + port + ", attempting again...")
            attempt += 1


# Added this here, as it just makes sense, as it's a helper function.
def readColor():
    global BP, colors
    try:
        value = BP.get_sensor(BP.PORT_3)
        if value < len(colors):  # Check if the value is within the range of predefined colors
            color_name = colors[value]
            # print("Detected Color: %s" % (color_name))
            return color_name
        else:
            print("Unknown color detected")
            return 'none'
    except brickpi3.SensorError as error:
        print("Error reading color sensor: %s" % (error))