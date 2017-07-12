import random
import time


class UPS:
    def read(self):
        time.sleep(3)
        return random.randint(0, 1)


class UPSListener:
    previousState = 0
    startTime = None
    endTime = None

    upsInstance= None
    onPowerUp = None
    onPowerDown = None

    def __init__(self, upsInstance, onPowerUp, onPowerDown):
        self.upsInstance = upsInstance
        self.onPowerUp = onPowerUp
        self.onPowerDown = onPowerDown

    def TurnOn(self):
        self.previousState = 1
        self.startTime = time.time()

        while True:
            state = self.upsInstance.read()

            if state != self.previousState:
                self.TriggerStateEvent(state == 1)
                self.previousState = state

    def TriggerStateEvent(self, isPowerDown):
        self.endTime = time.time()

        response = {
            'timeElapsed': self.inSeconds(self.endTime - self.startTime),
            'routerIp': '127.0.0.1'
        }

        if (isPowerDown is True):
            self.onPowerDown(response)
        else:
            self.onPowerUp(response)

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
#    print("Time elapsed ", param['timeElapsed'], " seconds")
#    print("Router IP ", param['routerIp'])
#
#def onPowerDown(param):
#    print("Time elapsed ", param['timeElapsed'], " seconds")
#    print("Router IP ", param['routerIp'])
#
#UPSSimulator = UPS()
#
#UPSListener = UPSListener(UPSSimulator, onPowerUp, onPowerDown)
#UPSListener.TurnOn()