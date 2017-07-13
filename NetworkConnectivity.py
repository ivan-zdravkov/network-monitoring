import subprocess
import platform


class NetworkConnectivity:
    previousState = True
    onPingPass = None
    onPingFail = None

    def __init__(self, onPingPass, onPingFail):
        self.onPingPass = onPingPass
        self.onPingFail = onPingFail

    def listenOn(self, host):
        while True:
            passed = self.ping(host)

            response = {
                'timeElapsed': 23,
                'host': host
            }

            if passed != self.previousState:
                if passed is True:
                    self.onPingPass(response)
                else:
                    self.onPingFail(response)

                self.previousState = passed

    def ping(self, host):
        """
        Returns True if host responds to a ping request
        """
        # Ping parameters as function of OS
        ping_str = "-n 1" if platform.system().lower() == "windows" else "-c 1"
        args = "ping " + " " + ping_str + " " + host
        need_sh = False if platform.system().lower() == "windows" else True

        # ping
        return subprocess.call(args, shell=need_sh) == 0

#example
#def onPingPass(param):
#    print("Time elapsed ", param['timeElapsed'], " seconds")
#    print("Host address ", param['host'])

#def onPingFail(param):
#    print("Time elapsed ", param['timeElapsed'], " seconds")
#    print("Host address ", param['host'])
#
#connection = NetworkConnectivity(onPingPass, onPingFail)
#connection.ping("127.0.0.1")
#connection.listenOn("127.0.0.1")