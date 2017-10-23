import subprocess
import platform
import time


class NetworkConnectivity:
    previousState = True
    onPingPass = None
    onPingFail = None

    def __init__(self, _onPingPass, _onPingFail):
        self.onPingPass = _onPingPass
        self.onPingFail = _onPingFail

    def listenOn(self, hosts):
        while True:
            time.sleep(5)

			failed_hosts = []
			
			for host in hosts:
				if self.ping(host) is False:
					failed_hosts.append(host)

			response = {
				'timeElapsed': 23,
				'hosts': failed_hosts
			}

			passed = if not failed_hosts
			
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