#!/usr/bin/python3
import serial
import time
from mySerCommLib import *
from random import randint, uniform

def main():
    debug = True

    if debug:
        print("\ninitSerComm from driver...\n")
    initSerComm(9600)
    time.sleep(.5)

    start_time = time.time()
    end_time = start_time + 180 # 3 Minutes
    in_green = False
    in_red = False
    in_yellow = False

    TURN_SPEED = 12
    MOVE_SPEED = 12

    prev_color = None

    while time.time() < end_time:
        distance = int(readSonicPortCM(3))
        color = readColor()
        
        if (color == "Blue" or color == "Green") and in_yellow:  //The blue tape often reads as green for us
            print("Found water!")
            break
        
        if distance <= 20:
            print("Obstacle!")
            if distance <= 10: # Obstacle, move back
                moveBack(MOVE_SPEED)
            else: # Obstacle distance greater than 10, turn
                turnLeft(TURN_SPEED)
                randsleep()
                continue
        
        
        # 1st, on line, move forward
        # 2nd, now off line, in green
        # 3rd, if back on line, but is in_green, get off the line

        if color == "White" and not in_green: # Pretty sure this condition, and following other color duplicates can be removed completely. Leave for now.
            moveForward(MOVE_SPEED)
        elif color != "White" and prev_color == "White" and not in_green:
            print("In White") 
            # break
            in_green = True
        elif color == "White" and in_green:
            if in_red:
                print("Not in Red")
            in_red = False # If somehow wandered back into green from red
            turnLeft(TURN_SPEED)
            randsleep(True)

        if color == "Red" and not in_red:
            moveForward(MOVE_SPEED)
        elif color != "Red" and prev_color == "Red" and not in_red: 
            print("In Red")
            in_red = True
        elif color == "Red" and in_red:
            moveBack(MOVE_SPEED)
            time.sleep(0.5)

            if in_yellow:
                print("Not In Yellow")
            in_yellow = False
            turnLeft(TURN_SPEED)
            randsleep(True)

        # Should just keep randomly moving around till it finds blue
        elif color == "Yellow" and not in_yellow:
            moveForward(8)
        elif color != "Yellow" and prev_color == "Yellow" and not in_yellow:
            print("In Yellow")
            in_yellow = True
        elif color == "Yellow" and in_yellow:
            moveBack(8)
            time.sleep(0.5)
            
            if(randint(0, 500) % 3):
                turnRight(TURN_SPEED)
            else:
                turnLeft(TURN_SPEED)

            randsleep(True)

        prev_color = color
        moveForward(MOVE_SPEED)
        time.sleep(0.01)

    brake()
    print(end_time - start_time)

def randsleep(on_line = False):
    if not on_line: 
        time.sleep(randfloat()) # Randomly sleeping to introduce randomness, not ideal but avoids being stuck in a loop
    else:
        time.sleep(randfloat(on_line)) # Randomly sleeping to introduce randomness, not ideal but avoids being stuck in a loop

def randfloat(on_line = False):
    if not on_line:
        return round(uniform(0.5, 2.2), 1) # 0.5 seconds to 2.2 seconds, rounded to first decimal
    else:
        return round(uniform(1.5, 3.0), 1)


if __name__ == "__main__":
    main()
