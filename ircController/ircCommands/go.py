#!/usr/bin/env python3
import socket
import logging
import ircController.ircCommands.ircCommand as ircCommandClass

class goCommand(ircCommandClass.ircCommand):

    def __init__(self,hardwareAPI):
        self.logger = logging.getLogger("WallE.ircCommands.echo")
        self.name = "go"
        self.cmdAliases = ["go"]
        self.permssionLevel = -1
        self.usage = ".go"
        self.go = "moves forward '\r\n'" + self.usage
        self.hardwareAPI = hardwareAPI



    def getName(self):
        """Return string with name"""
        return self.name

    def getCmdAliases(self):
        """Return string array with aliases for cmd"""
        return self.cmdAliases

    def getPermissionLevel(self):
        """Return integer for permission level"""
        return self.permssionLevel

    def getUsage(self):
        """Difference between usage and help is that usage is one or two lines, help is a full description.
        Returns a string with command usage"""
        return self.usage

    def getHelp(self):
        """Difference between usage and help is that usage is one or two lines, help is a full description.
        Returns a string explaining the command and its parameters"""
        return self.usage

    def onCommand(self,irc, sender, chan, args):
        """Do Command"""
        isMoving = self.hardwareAPI.go()
        if(isMoving):
            irc.printToIRC("I am moving!",chan)
        elif(not isMoving):
            irc.printToIRC("I have ceased moving",chan)
