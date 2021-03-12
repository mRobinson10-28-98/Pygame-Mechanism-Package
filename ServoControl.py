import RPi.GPIO as GPIO
import time
import math as m
import pygame
import csv

# CSV File name to pull angle values from
fileName = '/home/pi/Documents/Motor Control/Normal Walking Gait/03032021.csv'
#fileName = '/home/pi/Documents/Motor Control/Standing Positions/02242021.csv'

# Set GPIO Numbering
GPIO.setmode(GPIO.BOARD)

# Front left 3 servos, front right 3 servos, etc
FL = []
FR = []
RL = []
RR = []
# All 12 servos
servos = []

# Angle offsets based on installment configurations
thighOffset = 180
calfOffset = 180
hipOffset = -90

# Empty lists to be filled with angle values from csv file
hipThetas = []
thighThetas = []
calfThetas = []

# Open csv fil and take all angle values from three rows and append them to appropriate theta lists
with open(fileName, 'r') as csv_file:
    csv_reader = csv.reader(csv_file)
    
    for line in csv_reader:
        thighThetas.append(180 - (int(float(line[0])) - thighOffset))
        calfThetas.append(int(float(line[1])) - calfOffset)
        hipThetas.append(int(float(line[2])) - hipOffset)

print("Thigh: " + str(thighThetas))
print("Calf " + str(calfThetas))
print("Hip: " + str(hipThetas))


#Creating Servo Class
class Servo:
    def __init__(self, pin, thetas, leg):
        #Set Servo Pin to OUTPUT, Freq to 50HZ
        self.pin = pin
        self.thetas = thetas
        self.leg = leg
        GPIO.setup(self.pin,GPIO.OUT)
        self.pwmPin = GPIO.PWM(self.pin,50)
        self.angle = 0
        self.index = 0
        
        #Initilize PWM Pin
        self.pwmPin.start(30)
        
        #Append Servo to Servo Lists
        self.leg.append(self)
        servos.append(self)
        time.sleep(0.2)
    
    # Convert Angle value to Duty and sets the servo angle
    def setAngle(self, angle):
        duty = 10 * (angle / 180) + 2
        self.pwmPin.ChangeDutyCycle(duty)
        
    # Calculates the angle the servo should be set to using linear interpolation between two adjacent angle values in theta list
    # self.index is the index the servo should be referencing from theta list
    # when self.index is not a whole number, it linear interpolates between list element before and after current index value
    # Ex: index = 2.5 -> indexLow = 2, indexHigh = 3, if thetas[2] = 10 and thetas[3] = 20, self.theta = 15
    def calculateAngle(self, speed):
        self.index += speed
        if self.index > len(self.thetas) - 1:
            self.index -= len(self.thetas)
        
        indexLow = m.floor(self.index)
        indexHigh = m.ceil(self.index + 0.0001)
        
        # If index is a whole number, indexHigh still has to be nex number, hence the +0.0001 so it rounds up
        if indexHigh > len(self.thetas) - 1:
            indexHigh -= len(self.thetas)
            
        thetaLow = self.thetas[indexLow]
        thetaHigh = self.thetas[indexHigh]
        
        # Linear interpolation
        self.angle = thetaLow + (((self.index - indexLow) * (thetaHigh - thetaLow)) / (indexHigh - indexLow))


# Take away jitter 
def deJitter(delay):
    time.sleep(delay)
    
    for servo in servos:
        servo.pwmPin.ChangeDutyCycle(0)
        
    time.sleep(delay*2)

#Calculates anlgle values for each servo and adjusts them using setAngle method
def iterateServos(speed):
    for servo in FL:
        servo.calculateAngle(speed)
        servo.setAngle(servo.angle)
    for servo in RL:
        servo.calculateAngle(speed)
        servo.setAngle(servo.angle)
    for servo in FR:
        servo.calculateAngle(speed)
        servo.setAngle(180 - servo.angle)
    for servo in RR:
        servo.calculateAngle(speed)
        servo.setAngle(180 - servo.angle)
        
    deJitter(0.01)

# Should be used after a walking method is used (trot, saunter) in order to set the legs to a proper initial configuration
def initiateServos():
    for servo in servos:
        servo.calculateAngle(0)
        servo.setAngle(servo.angle)
    deJitter(0.2)
    
# Front two legs in sync, offset from rear two legs by half a cycle
def trot():
    findex = 0
    rindex = findex + m.floor(len(hipThetas) / 2)
    for servo in FL:
        servo.index = findex
    for servo in FR:
        servo.index = findex
    for servo in RL:
        servo.index = rindex
    for servo in RR:
        servo.index = rindex
    initiateServos()

# All four legs offset by a quarter of a cycle
def saunter():
    frindex = 0
    flindex = m.floor(len(hipThetas) / 4)
    rrindex = m.floor(len(hipThetas) / 2)
    rlindex = m.floor((3/4) * len(hipThetas))
    for servo in FL:
        servo.index = flindex
    for servo in FR:
        servo.index = frindex
    for servo in RL:
        servo.index = rlindex
    for servo in RR:
        servo.index = rrindex
    initiateServos()

def gallop():
    index1 = 0
    index2 = m.floor(len(hipThetas) / 2)
    for servo in FL:
        servo.index = index1
    for servo in FR:
        servo.index = index2
    for servo in RL:
        servo.index = index2
    for servo in RR:
        servo.index = index1
    initiateServos()

def uniform():
    index = 0
    for servo in servos:
        servo.index = 0
    initiateServos()
 
# Set Up Servo
servoFLH = Servo(18, hipThetas, FL)
servoFLT = Servo(15, thighThetas, FL)
servoFLC = Servo(13, calfThetas, FL)

servoFRH = Servo(3, hipThetas, FR)
servoFRT = Servo(5, thighThetas, FR)
servoFRC = Servo(7, calfThetas, FR)

servoRLH = Servo(10, hipThetas, RL)
servoRLT = Servo(16, thighThetas, RL)
servoRLC = Servo(8, calfThetas, RL)

servoRRH = Servo(19, hipThetas, RR)
servoRRT = Servo(21, thighThetas, RR)
servoRRC = Servo(23, calfThetas, RR)

saunter()
while True:
    startTime = time.time()
    
    iterateServos(0.2)
    
    currentTime = time.time()
    #print(currentTime - startTime)
servoFLH.pwmPin.stop()
servoFLT.pwmPin.stop()
servoFLC.pwmPin.stop()
GPIO.cleanup()




  

