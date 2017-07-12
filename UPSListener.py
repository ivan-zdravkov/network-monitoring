import random
import time


class UPS:
    def read(self):
        return {
            'routerIp': '127.0.0.1',
            'isPowerDown':  (random.randint(0, 1) == 0)
        }


class UPSListener:
    previousState = 0
    startTime = None
    endTime = None

    upsInstance = None
    onPowerUp = None
    onPowerDown = None

    def __init__(self, upsInstance, onPowerUp, onPowerDown):
        self.upsInstance = upsInstance
        self.onPowerUp = onPowerUp
        self.onPowerDown = onPowerDown

    def TurnOn(self):
        self.previousState = False
        self.startTime = time.time()

        while True:
            time.sleep(3)
            UPSResponse = self.upsInstance.read()

            if UPSResponse['isPowerDown'] != self.previousState:
                self.TriggerStateEvent(UPSResponse)
                self.previousState = UPSResponse['isPowerDown']

    def TriggerStateEvent(self, UPSResponse):
        self.endTime = time.time()

        callbackModel = {
            'timeElapsed': self.inSeconds(self.endTime - self.startTime),
            'routerIp': UPSResponse['routerIp']
        }

        if UPSResponse['isPowerDown'] is True:
            self.onPowerDown(callbackModel)
        else:
            self.onPowerUp(callbackModel)

        self.startTime = time.time()

    def inSeconds(self, value):
        valueD = (((value / 365) / 24) / 60)
        Days = int(valueD)

        valueH = (valueD - Days) * 365
        Hours = int(valueH)

        valueM = (valueH - Hours) * 24
        Minutes = int(valueM)

        valueS = (valueM - Minutes) * 60
        Seconds = int(valueS)

        return Seconds

#def onPowerUp(param):
#    print("Up")
#    print("Time elapsed ", param['timeElapsed'], " seconds")
#    print("Router IP ", param['routerIp'])
#
#def onPowerDown(param):
#    print("Down")
#    print("Time elapsed ", param['timeElapsed'], " seconds")
#    print("Router IP ", param['routerIp'])
#
#UPSSimulator = UPS()
#
#UPSListener = UPSListener(UPSSimulator, onPowerUp, onPowerDown)
#UPSListener.TurnOn()