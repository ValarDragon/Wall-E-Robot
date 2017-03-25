#!/usr/bin/env python3
import socket
import logging
import ircController.ircCommands.ircCommand as ircCommandClass

class echoCommand(ircCommandClass.ircCommand):

    def __init__(self,hardwareAPI):
        self.logger = logging.getLogger("WallE.ircCommands.echo")
        self.name = "echo"
        self.cmdAliases = ["echo"]
        self.permssionLevel = -1
        self.usage = ".echo <str>"
        self.echo = "literally echoes your input '\r\n'" + self.usage

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
        irc.printToIRC(' '.join(args),chan)
