#!/usr/bin/env python3
import socket
import logging
import ssl
import sys
import traceback
import time
import ircController.commandHandler as commandHandlerClass

class ircDaemon:
    """Daemon to control the robot via IRC"""
    def __init__(self,hardwareAPI):
        #TODO load these from config
        self.SSL = True
        self.HOST = "irc.hackthissite.org"
        self.PORT = 7000
        self.CHAN = "#bots"
        self.NICK = "Wall-E"
        self.IDENT = "Glados"
        self.REALNAME = "Glados"
        self.RECVBLOCKSIZE = 2048
        self.COMMANDPREFIX = "."

        self.readBuffer = ""
        self.logger = logging.getLogger("WallE.ircDaemon")
        self.hardwareAPI = hardwareAPI

    def setupDaemon(self):
        self.connectToServer()
        self.connectToChan()
        self.commandHandler = commandHandlerClass.commandHandler(self, self.hardwareAPI)
        for i in range(60):
            self.sock.recv(self.RECVBLOCKSIZE)
        while(True):
            try:
                self.getBuffer()
                #time.sleep(.005)
            except:
                if("Keyboard" in str(sys.exc_info()[0])):
                    self.printToIRC(self.NICK + " is shutting down.")
                    self.closeSocket()
                    break
                print("BZZZZZZZZZZZZZZZTTTTT *******    ERROR   *** " + str(traceback.format_exc()))
                self.printToIRC("An internal error occured! See log file!")
                self.logger.exception("Error " + str(traceback.format_exc()))

    def connectToServer(self,host="self.HOST",port="self.PORT",useSSL="self.SSL"):
        """Connect to IRC Server"""
        #Have to do this, because for some reason Python doesn't support self-arguments as overloads.
        if(host=="self.HOST"): host = self.HOST
        if(port=="self.PORT"): port = self.PORT
        if(useSSL=="self.SSL"): useSSL = self.SSL

        unwrappedSocket = socket.socket()
        if(useSSL):
            self.sock = ssl.wrap_socket(unwrappedSocket)
        else:
            self.sock = unwrappedSocket
        self.sock.connect((host,port))
        self.getBuffer()
        self.printBytes(bytes("NICK %s\r\n" % self.NICK, "UTF-8"))
        self.printBytes(bytes("USER %s %s Wolf :%s\r\n" % (self.IDENT, host, self.REALNAME), "UTF-8"))
        self.logger.info("IRC Connection started to HOST: %s , PORT: %s , using SSL: %s " % (str(host),str(port),str(useSSL)))
        self.getBuffer()
        self.getBuffer()

    def connectToChan(self,chan="self.CHAN"):
        if(chan=="self.CHAN"): chan = self.CHAN
        self.printBytes(bytes("JOIN %s\r\n" % chan,"UTF-8"))

    def getBuffer(self):
        """ Gets buffer from IRC, and then executes commands, or replies to pings accordingly. """
        self.logger.debug("GETTING BUFFER")
        #print("getting buff")
        incomingMessage = self.sock.recv(self.RECVBLOCKSIZE)
        #print(incomingMessage)
        self.readBuffer = self.readBuffer + incomingMessage.decode("UTF-8")
        incomingMessage = str.split(self.readBuffer, "\n")
        self.readBuffer=incomingMessage.pop()
        for ircLine in incomingMessage:
            self.logger.debug(ircLine)

            line = str.rstrip(ircLine)
            line = str.split(line) #Split by space by default.

            if(line[0] == "PING"):
                self.printBytes(bytes("PONG %s\r\n" % line[1],"UTF-8"))
                self.logger.debug("PONG " + line[1])

            elif(line[1]=="PRIVMSG"):
                cmd=line[3]
                cmd=cmd[1:]
                if(cmd.startswith(self.COMMANDPREFIX)):
                    self.logger.info(str(line))
                    self.commandHandler.executeCommand(line)

    def printBytes(self, msg):
        """Print bytes directly to server"""
        self.sock.send(msg)

    def printToIRC(self, msg, chan="self.CHAN"):
        """ Print a message to either the channel or a user. To send to a user, simply replace chan with
        chan=USERNAME """
        if(chan=="self.CHAN"): chan = self.CHAN
        self.logger.info("Msg sent on chan %s with content %s" % (chan,msg))
        msg = str(msg).replace('\n','\nPRIVMSG ' + chan + ' :')
        self.printBytes(bytes(("PRIVMSG %s :%s\r\n") % (chan,str(msg)),"UTF-8"))

    def closeSocket(self):
        self.sock.shutdown(socket.SHUT_RDWR)
        self.sock.close()
