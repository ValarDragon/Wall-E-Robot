import os
import logging
# Importing RPi.GPIO is done at the end.


class WallEHardware:
    def __init__(self):
        #TODO load these from config
        #Load everything from config
        self.logger = logging.getLogger("WallE.hardware")
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(7,GPIO.OUT)
        self.states = ["dummy"] * 24
        GPIO.output(7,False)
        self.states[7] = False

    def go(self):
        if(self.states[7] == True):
            GPIO.output(7,False)
            self.states[7] = False
        elif(self.states[7] == False):
            GPIO.output(7,True)
            self.states[7] = True
        return self.states[7]

# Hack to get output from terminal cmd
def runProcess(exe,getOutput=False):
    if(getOutput):
        os.system(exe+ ' > /tmp/os.txt')
        returnVal = open('/tmp/os.txt','r').read()
        os.remove('/tmp/os.txt')
        return returnVal
    else:
        os.system(exe)

if(os.name == "posix"):
    if("raspberrypi" in runProcess("uname -a",getOutput=True)):
        import RPi.GPIO as GPIO
    else:
        print("Running on Linux System that is not RaspberryPI, things will probably break quickly.")
else:
    print("Running on Windows System not on a RaspberryPI, things will probably break quickly.")
