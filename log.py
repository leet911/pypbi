import logging
import inspect

class log:
    def __init__(self, sFilePath, sLevel='WARN'):
        self.sLogPath = sFilePath
        lLevels = ["CRITICAL", "ERROR", "WARN", "WARNING", "INFO", "DEBUG"]
        if sLevel in lLevels:
            self.iLevel = eval("logging." + sLevel)
        else:
            print "Unknown LOG_LEVEL %s specified, defaulting to WARN" %(conf.LOG_LEVEL)
            self.iLevel = logging.WARN
        
    def log(self, iLevel, sMessage):
        oLog = logging.getLogger()
        oLog.setLevel(logging.DEBUG)
        oFormat = logging.Formatter('%(asctime)s -%(levelname)s- %(message)s')

        oFileHandler = logging.FileHandler(self.sLogPath)
        oFileHandler.setLevel(self.iLevel)
        oFileHandler.setFormatter(oFormat)
        oLog.addHandler(oFileHandler)

        #if self.iLevel == logging.DEBUG:
            ## Print to console also if debug enabled
            #oStreamHandler = logging.StreamHandler()
            #oStreamHandler.setLevel(self.iLevel)
            #oStreamHandler.setFormatter(oFormat)
            #oLog.addHandler(oStreamHandler)

        lStack = inspect.stack()
        #print lStack
        try:
            sCallingModule =  lStack[2][1].split("\\")[-1] + "[" + str(lStack[2][2]) + "]"
            sCallingFunction = lStack[2][3]
            sMessage = "<" + sCallingModule + "::" + sCallingFunction + "> " + str(sMessage)
        except:
            pass
        oLog.log(iLevel, sMessage)

        lHandlers = list(oLog.handlers)
        for oHandler in lHandlers:
            oLog.removeHandler(oHandler)
            oHandler.flush()
            oHandler.close()

        return sMessage

    def debug(self, sMessage):
        return self.log(logging.DEBUG, sMessage)

    def info(self, sMessage):
        return self.log(logging.INFO, sMessage)

    def warn(self, sMessage):
        return self.log(logging.WARN, sMessage)

    def error(self, sMessage):
        return self.log(logging.ERROR, sMessage)

    def critical(self, sMessage):
        return self.log(logging.CRITICAL, sMessage)