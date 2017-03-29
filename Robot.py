#!/usr/bin/env python3
import logging
from logging.config import fileConfig
import sys
import ircController.ircDaemon
import HardwareAPI.hardwareAPI
import configparser

def init(argv):
    #load db stuff here
    fileConfig('logConfig.ini')
    logger = logging.getLogger("WallE")
    logger.info('---- Logging Initiated ----')
    main()

def main():
    logger = logging.getLogger("WallE")
    hardwareAPI = HardwareAPI.hardwareAPI.WallEHardware()

    controllerConfig = configparser.ConfigParser()
    controllerConfig.read('controllerConfig.ini')
    if('Controllers' not in controllerConfig):
        print("Bad Controller Config")
        logger.error("Error in Controller Config. No [Controllers] Section Found.")
    if(controllerConfig["Controllers"].getboolean("irc")):
        #Have this in a seperate thread, so we can support multiple controllers?
        irc = ircController.ircDaemon.ircDaemon(hardwareAPI)
        #TODO add way to connect to multiple channels
        irc.setupDaemon()


if __name__ == "__main__":
   init(sys.argv[1:])
