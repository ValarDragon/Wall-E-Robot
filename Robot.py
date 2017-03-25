#!/usr/bin/env python3
import logging
from logging.config import fileConfig
import sys
import ircController.ircDaemon
import HardwareAPI.hardwareAPI

def init(argv):
    #load db stuff here
    fileConfig('logConfig.ini')
    logger = logging.getLogger("WallE")
    logger.info('---- Logging Initiated ----')
    main()

def main():
    #load this from config
    useIrcController = True
    hardwareAPI = HardwareAPI.hardwareAPI.WallEHardware()
    if(useIrcController):
        #Have this in a seperate thread, so we can support multiple controllers?
        irc = ircController.ircDaemon.ircDaemon(hardwareAPI)
        #TODO add way to connect to multiple channels
        irc.setupDaemon()


if __name__ == "__main__":
   init(sys.argv[1:])
