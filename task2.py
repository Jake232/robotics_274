import task1
import Lib
import struct
import random

"""
State Control
"""

#Puts the robot in Start mode
def start():
    task1.write(Lib.START)


#Puts the robot in Stop mode
def stop():
    task1.write(Lib.STOP)


#Resets the Robot
def reset():
    task1.write(Lib.RESTART)


#Puts the robot in Passive mode
def passive():
    task1.write(Lib.START)


#Puts the robot in Safe mode
def safe():
    task1.write(Lib.SAFE)


#Puts the robot in Full mode
def full():
    task1.write(Lib.FULL)


#Changes the state of the robot
def state_control(state):
    if state == 128:
        start()
    elif state == 7:
        reset()
    elif state == 173:
        stop()
    elif state == 131:
        safe()
    elif state == 132:
        full()


"""
Read Sensors
"""


#Default, allows you to put in a sensor id and will return one byte of data on that sensors state
def read_sensors(sensor_id):
    task1.write(Lib.SENSOR_START)
    task1.wait()
    task1.write(sensor_id)
    task1.wait()
    data = task1.read()
    task1.wait()
    data = unpack(data)
    if data is not None:
        return data
    else:
        return -1


def read_sensors_2_bytes(sensor_id):
    task1.write(Lib.SENSOR_START)
    task1.wait()
    task1.write(sensor_id)
    task1.wait()
    data = task1.read()
    task1.wait()
    data = unpack_2_bytes(data)
    if data is not None:
        return data
    else:
        return -1

#Prints the state of the buttons
def write_buttons():
    buttons = read_sensors(Lib.BUTTONS)
    if buttons == 1:
        print "Clean"
    elif buttons == 2:
        print "Spot"
    elif buttons == 4:
        print "Dock"
    elif buttons == 8:
        print "Minute"
    elif buttons == 16:
        print "Hour"
    elif buttons == 32:
        print "Day"
    else:
        print "Nothing"
    task1.wait()


#Returns the state of the buttons
def read_buttons():
    buttons = read_sensors(Lib.BUTTONS)
    return buttons


#Prints the state of the Bumpers and wheel drops
def read_bumpers_and_wheel_drops():
    bumps_wd = read_sensors(Lib.BUMP_WD)
    if bumps_wd == 1:
        print "Right"
    elif bumps_wd == 2:
        print "Left"
    elif bumps_wd == 3:
        print "Front"
    elif bumps_wd == 4:
        print "Right Wheel"
    elif bumps_wd == 8:
        print "Left Wheel"
    task1.wait()


#Prints the state of the cliff sensors
def read_cliff():
    left_cliff = read_sensors(Lib.LEFT_CLIFF)
    print "Left: ", left_cliff
    left_front_cliff = read_sensors(Lib.LEFT_FRONT_CLIFF)
    print "Front Left: ", left_front_cliff
    right_cliff = read_sensors(Lib.RIGHT_CLIFF)
    print "Right: ", right_cliff
    right_front_cliff = read_sensors(Lib.RIGHT_FRONT_CLIFF)
    print "Front Right: ", right_front_cliff


#Returns a boolean based on the state of the clean button
def clean_pressed():
    is_it_pressed = False
    clean = read_sensors(Lib.BUTTONS)
    if clean == 1:
        is_it_pressed = True
    return is_it_pressed


#Returns a boolean based on if the wheels have dropped or not
def wheel_dropped():
    wheel_drop = read_sensors(Lib.BUMP_WD)
    if wheel_drop == 4 or wheel_drop == 8 or (wheel_drop == 4 and wheel_drop == 8):
        return True
    else:
        return False


#Returns the state of the left bumper
def left_bumper():
    bumper = read_sensors(Lib.BUMP_WD)
    if bumper == 2:
        return True
    else:
        return False


#Returns the state of the right bumper
def right_bumper():
    bumper = read_sensors(Lib.BUMP_WD)
    if bumper == 1:
        return True
    else:
        return False


#Returns the state of the front bumper
def front_bumper():
    bumper = read_sensors(Lib.BUMP_WD)
    if bumper == 3:
        return True
    else:
        return False


#Returns the state of the left cliffs
def left_cliffs():
    left_cliff = read_sensors(Lib.LEFT_CLIFF)
    left_front_cliff = read_sensors(Lib.LEFT_FRONT_CLIFF)
    if left_cliff == 1 or left_front_cliff == 1:
        return True
    else:
        return False


#Returns the state of the right cliffs
def right_cliffs():
    right_cliff = read_sensors(Lib.RIGHT_CLIFF)
    right_front_cliff = read_sensors(Lib.RIGHT_FRONT_CLIFF)
    if right_cliff == 1 or right_front_cliff == 1:
        return True
    else:
        return False


#Gets the distance since it was last called
def get_distance():
    distance = read_sensors_2_bytes(Lib.DIST)
    return distance


#Gets the angle since it was last called
def get_angle():
    angle = read_sensors_2_bytes(Lib.ANGLE)
    return angle


"""
Drive Setups
"""


#Drive based on sending the same high byte and low byte to both wheels and a radius to differentiate that
def drive(velocity_high, velocity_low, radius_high, radius_low):
    task1.write(Lib.DRIVE_START)
    task1.wait()
    task1.write(velocity_high)
    task1.wait()
    task1.write(velocity_low)
    task1.wait()
    task1.write(radius_high)
    task1.wait()
    task1.write(radius_low)
    task1.wait()


#Drive based on sending different velocities to both wheels
def drive_direct(right_high, right_low, left_high, left_low):
    task1.write(Lib.DRIVE_DIRECT)
    task1.write(right_high)
    task1.write(right_low)
    task1.write(left_high)
    task1.write(left_low)


"""
Drive Commands
"""


#Drives forward using the first drive function
def drive_forward():
    drive(1, 2, 0, 0)


#Stops the robot using the drive direct function by sending a velocity of 0 to the wheels
def stop_robot():
    drive_direct(0, 0, 0, 0)


#Turns the robot counter clockwise by giving one motor velocity the the other motor none
def turn_in_place():
    drive_direct(1, 2, 0, 0)


#Makes the robot turn in place clockwise
def turn_right():
    drive_direct(1, 2, 0, 14)


#Makes the robot turn in place counter-clockwise
def turn_left():
    drive_direct(0, 14, 1, 2)


#Picks a random way to turn
def turn_random():
    decision = random.randint(0, 1)
    if decision == 0:
        turn_left()
    else:
        turn_right()


"""
Misc
"""


#Unpacks one byte of data from a packet
def unpack(packet):
    if len(packet) == 1:
        return struct.unpack('>B', packet)[0]


def unpack_2_bytes(packet):
    if len(packet) == 2:
        return struct.unpack('>BB', packet)[0]
    else:
        print "Need two bytes"


#A simple song for the robot to play
def warning_song():
    task1.write(Lib.SONG)
    task1.write(0)
    task1.write(3)
    task1.write(45)
    task1.write(32)
    task1.write(47)
    task1.write(32)
    task1.write(48)
    task1.write(32)


#Drives the song above
def play_song(song_number):
    task1.write(Lib.PLAY)
    task1.write(song_number)
