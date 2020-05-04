import Lib
import serial
import time
import random


'''Used to connect, send commands, and read data from the robot.
Opens a serial connection'''
sc = serial.Serial('/dev/ttyUSB0', baudrate=115200, timeout=1)


#Reads a byte the robot
def read():
    return sc.read(1)


#Sends a command to the console
def write(command):
    sc.write(chr(command))


#Sets a time to wait
def wait(times=0.015):
    time.sleep(times)


#Connects your laptop to the robot
def connect():
    sc.close()
    wait(1)
    sc.open()
    wait(1)
    write(173)
    wait(1)
    write(Lib.INIT)
    wait(1)
    write(Lib.SAFE)
    wait(1)


#Closes the connection to the robot
def close():
    sc.close()
    exit()


#Amount of time it takes to drive forward 30 cm.
def drive_straight_time():
    time.sleep(1.1)


#Amount of time it takes to turn 70 degrees.
def turn_time():
    time.sleep(1.061)


#For Project 2, will turn 180 degrees plus or minus 30 degrees
def turn_180_plus_rand():
    a = random.randint(0, 30)
    b = random.randint(0, 1)
    """.004166 seconds per degree"""
    if b == 1:
        time.sleep(0.75+(a*.004166))
    elif b == 0:
        time.sleep(0.75-(a*.004166))
    else:
        print "ERROR"
