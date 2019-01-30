import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)

GPIO.setmode(GPIO.BOARD)

GPIO.setup(11, GPIO.IN)     #wake_up signal
GPIO.setup(13, GPIO.IN)     #status of parking spot
GPIO.setup(15, GPIO.OUT)    #ack signal

prev_status = 0

while True:
    wake_up = GPIO.input(11)
    status  = GPIO.input(13)

    if wake_up == 0:
        print "sleeping"
        GPIO.output(15, 0)  
        time.sleep(0.2)
    elif wake_up == 1:  #got a wake up signal
        GPIO.output(15, 1)  #Send ack signal
        if ( status != prev_status):
            print "Woke up"
            print "Status: ",status
            print "Prev_Status: ",prev_status
            #send parking request to gateway
        else:
            print "Ask gateway for tasks"
            #ask gateway for tasks
        prev_status = status
        time.sleep(0.2)
