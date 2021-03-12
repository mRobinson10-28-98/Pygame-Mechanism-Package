import RPi.GPIO as GPIO
import time

# Convert Duty to Angles
def set_angle(angle):
    duty = 10 * (angle / 180) + 2
    return duty

GPIO.setmode(GPIO.BOARD)

servoPin = 37
GPIO.setup(servoPin,GPIO.OUT)
pwmPin = GPIO.PWM(servoPin,50)
pwmPin.start(0)
time.sleep(1)

delay = 0.001

while True:
    startTime = time.time()
    pwmPin.ChangeDutyCycle(set_angle(90))
    time.sleep(delay)
    
#     pwmPin.ChangeDutyCycle(set_angle(135))
#     time.sleep(delay)
#     pwmPin.ChangeDutyCycle(set_angle(180))
#     time.sleep(delay)
#     pwmPin.ChangeDutyCycle(set_angle(135))
#     time.sleep(delay)
#     pwmPin.ChangeDutyCycle(set_angle(90))
#     time.sleep(delay)
#     pwmPin.ChangeDutyCycle(set_angle(45))
#     time.sleep(delay)
#     pwmPin.ChangeDutyCycle(set_angle(0))
#     time.sleep(delay)
#     pwmPin.ChangeDutyCycle(set_angle(45))
#     time.sleep(delay)
    
    currentTime = time.time()
    #print(currentTime - startTime)

pwmPin.stop()
GPIO.cleanup()
print("Done")
