try:
    import RPi.GPIO as GPIO
except RuntimeError:
    print("Error importing RPi.GPIO!  This is probably because you need superuser privileges.  You can achieve this by using 'sudo' to run your script")

import time as time

GPIO.setmode(GPIO.BCM)

channel = 4

GPIO.setup(channel, GPIO.IN, pull_up_down=GPIO.PUD_UP)

print(GPIO.input(channel)) 
print(GPIO.LOW)
while GPIO.input(channel) == GPIO.LOW:
    time.sleep(0.01)  # wait 10 ms to give CPU chance to do other things
    print(".")

if GPIO.input(channel):
    print('Input was HIGH')
else:
    print('Input was LOW')

print("Done");

