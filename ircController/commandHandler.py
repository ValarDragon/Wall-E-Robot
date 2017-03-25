
#!/usr/bin/env python3
import socket
import logging
import ssl
import sys
import traceback
import time
import ircController.ircCommands.echo as echoCommandClass
import ircController.ircCommands.go as goCommandClass

class commandHandler:
    """Daemon to control the robot via IRC"""
    def __init__(self, irc):
        self.irc = irc
        self.logger = logging.getLogger("WallE.commandHandler")
        self.commands = []
        self.commands.append(echoCommandClass.echoCommand())

    def executeCommand(self,line):
        cmdName = (line[3][2:]).lower()
        user = (line[0])[1:line[0].index("!")]
        chan = line[2]
        cmdClass = ""
        args = line[4:]
        for command in self.commands:
            if(command.getName() == cmdName):
                cmdClass = command
                break
            for commandAlias in command.getCmdAliases():
                if(commandAlias == cmdName):
                    cmdClass = command
                    break
            if(cmdClass != ""):
                break
        if(cmdClass == ""):
            self.irc.printToIRC("Command %s not found!" % cmdName )
        else:
            cmdClass.onCommand(self.irc, user,chan,args)
