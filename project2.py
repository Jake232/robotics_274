import task1
import task2
import threading

#Connects to the robot
task1.connect()
print "Connected"


#Defines lock in order to lock and unlock threads
lock = threading.Lock()


#Global variables for threads
clean_pressed = False
wheel_drop = False
left_bumper = False
right_bumper = False
front_bumper = False
left_cliff = False
right_cliff = False


#A thread that runs and constantly checks if the clean button has been pressed
def clean_pressed_function():
    print "Clean Pressed Thread Started"
    global clean_pressed
    while 1:
        lock.acquire()
        pressed = task2.read_buttons()
        lock.release()
        if pressed == 1:
            clean_pressed = True
            print "Pressed"


#A thread that runs and constantly checks if the wheels dropped
def wheel_dropped_function():
    print "Wheel Dropped Thread Started"
    global wheel_drop
    while 1:
        lock.acquire()
        dropped = task2.wheel_dropped()
        lock.release()
        if dropped:
            wheel_drop = True
            print "Dropped"
            task2.warning_song()
            task2.play_song(0)


#A thread that runs and constantly checks if the left bumper has been pressed
def left_bumper_function():
    print "Left Bumper Thread Started"
    global left_bumper
    while 1:
        lock.acquire()
        pressed = task2.left_bumper()
        lock.release()
        if pressed:
            left_bumper = True
            print "Left Bumper Hit"


#A thread that runs and constantly checks if the right bumper has been pressed
def right_bumper_function():
    print "Right Bumper Thread Started"
    global right_bumper
    while 1:
        lock.acquire()
        pressed = task2.right_bumper()
        lock.release()
        if pressed:
            right_bumper = True
            print "Right Bumper Hit"


#A thread that runs and constantly checks if the front bumper has been pressed
def front_bumper_function():
    print "Front Bumper Thread Started"
    global front_bumper
    while 1:
        lock.acquire()
        pressed = task2.front_bumper()
        lock.release()
        if pressed:
            front_bumper = True
            print "Front Bumper Hit"


#A thread that runs and constantly checks if the right cliffs have been activated
def right_cliff_function():
    print "Right Cliff Thread Started"
    global right_cliff
    while 1:
        lock.acquire()
        cliff = task2.right_cliffs()
        lock.release()

#A thread that runs and constantly checks if the left cliffs have been activated
def left_cliff_function():
    print "Left Cliff Thread Started"
    global left_cliff
    while 1:
        lock.acquire()
        cliff = task2.right_cliffs()
        lock.release()
        if cliff:
            left_cliff = True
            print "Cliff on Left"


#main thread
def main_function():
    global clean_pressed, wheel_drop, left_bumper, right_bumper
    global front_bumper, left_cliff, right_cliff
    while 1:
        if clean_pressed:
            task1.wait(0.5)
            clean_pressed = False
            print "Starting"
            while not wheel_drop and not clean_pressed and not left_cliff and not right_cliff:
                if left_bumper:
                    lock.acquire()
                    task2.turn_right()
                    task1.turn_180_plus_rand()
                    lock.release()
                elif right_bumper:
                    lock.acquire()
                    task2.turn_left()
                    task1.turn_180_plus_rand()
                    lock.release()
                elif front_bumper:
                    lock.acquire()
                    task2.turn_random()
                    task1.turn_180_plus_rand()
                    lock.release()
                lock.acquire()
                task2.drive_forward()
                lock.release()
                task1.wait(0.125)
        lock.acquire()
        task2.stop_robot()
        lock.release()
        clean_pressed = False
        wheel_drop = False
        left_bumper = False
        right_bumper = False
        front_bumper = False
        left_cliff = False
        right_cliff = False

#Defines the threads
clean_pressed_thread = threading.Thread(target=clean_pressed_function)
wheel_dropped_thread = threading.Thread(target=wheel_dropped_function)
left_bumper_thread = threading.Thread(target=left_bumper_function)
right_bumper_thread = threading.Thread(target=right_bumper_function)
front_bumper_thread = threading.Thread(target=front_bumper_function)
left_cliffs_thread = threading.Thread(target=left_cliff_function)
right_cliffs_thread = threading.Thread(target=right_cliff_function)
main_thread = threading.Thread(target=main_function)

#Starts the threads
clean_pressed_thread.start()
wheel_dropped_thread.start()
left_bumper_thread.start()
right_bumper_thread.start()
front_bumper_thread.start()
left_cliffs_thread.start()
right_cliffs_thread.start()
main_thread.start()

        if cliff:
            right_cliff = True
            print "Cliff on Right"
