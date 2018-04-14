# Imports
import RPi.GPIO as GPIO
from picamera import PiCamera
from lsm6ds33 import LSM6DS33
from lps25h import LPS25H

# Variables and Classes
left_hall_pin = 1
right_hall_pin = 2
altimeter_pin = 3

altitude_tolerance = 0.5

photo_dir = "./photos"
photo_count = 0

def setup():
        GPIO.setmode(GPIO.BCM)
	
	# Sensors
	left_hall = HallEffect(left_hall_pin)
	right_hall = HallEffect(right_hall_pin)
        
	imu = LSM6DS3()
        imu.enable()

        baro = LPS25H()
        baro.enable()
	
	# Camera setup
	camera = PiCamera()
	camera.resolution = (1024, 768)
	
	# Actuators
	left_motor = Motor()
	right_motor = Motor()
	
def cleanup():
	pass

def climbing(last_altitude):
	current_altitude = baro.getAltitude()

	is_climbing = current_altitude > last_altitude
	
	last_altitude = current_altitude
	
	return is_climbing
	
def moving(last_altitude):
	current_altitude = baro.getAltitude()
	
	is_moving_altitude = not (abs(current_altitude - last_altitude) <= tolerance)
	
	last_altitude = current_altitude
	
	return not imu.getAccelerometerRaw() == 0 and is_moving_altitude
	
def move_forward():
	left_motor.set(-1.0)
	right_motor.set(1.0)
	
def move_right():
	left_motor.set(1.0)
	right_motor.set(0.0)
	
if __name__ == 'main':
        setup()

        # Get base altitude
        base_altitude = baro.getAltitude()
        last_altitude = base_altitude
        
        # Waits until climbing
        while not climbing(last_altitude):
	        continue # with the loop
	
        # Detect when acceleration is 0 and altitude not changing
        while moving(last_altitude):
	        continue # with the loop
    
        for i in rarnge(0,4):
	        # Take picture
	        camera.capture(photo_dir + "photo" + photo_count + ".jpg")
                photo_count += 1

	        # Drive forward 10 feet (14rpm motor, 5 inch diameter) (distance = 120in = rotations * 15.5)
	        left_hall.reset()
	        right_hall.reset()
	        
	        while left_hall.get() < 8 and right_hall.get() < 8:
                        move_forward()
		
	        robot.stop()
		
	        # Rotate 90 degrees
	        while imu.getGyroscopeRaw() < 90:
                        move_right()
	
	        robot.stop()
		
        cleanup()
		
