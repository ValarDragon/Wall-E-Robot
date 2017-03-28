#!/usr/bin/env python3
import socket
import logging

class ircCommand:

    def getName(self):
        """Return string with name"""
        raise NotImplementedError("getName() in ircCommand is not implemented")

    def getCmdAliases(self):
        """Return string array with aliases for cmd"""
        raise NotImplementedError("getCmdAliases() in ircCommand is not implemented")

    def getPermissionLevel(self):
        """Return integer for permission level"""
        raise NotImplementedError("getPermissionLevel() in ircCommand is not implemented")

    def getUsage(self):
        """Difference between usage and help is that usage is one or two lines, help is a full description.
        Returns a string with command usage"""
        raise NotImplementedError("getUsage() in ircCommand is not implemented")

    def getHelp(self):
        """Difference between usage and help is that usage is one or two lines, help is a full description.
        Returns a string explaining the command and its parameters"""
        raise NotImplementedError("getHelp() in ircCommand is not implemented")

    def onCommand(irc, sender, chan, args):
        """Do Command"""
        raise NotImplementedError("command not yet defined")
