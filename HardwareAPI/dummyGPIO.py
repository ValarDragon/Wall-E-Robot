#make a seperate logger for this
states = [False] * 24

BOARD = "BOARD"
OUT = 1

def output(port,value):
    states[port] = value
    #log this

def setup(port,type):
    #log this
    #dummy line
    a = 1

def setmode(type):
    #log this
    #dummy line
    a = 1
