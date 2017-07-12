#!/usr/bin/env python

from NetworkConnectivity import NetworkConnectivity
from UPSListener import UPS
from UPSListener import UPSListener
from MongoDBRepo import MongoDBRepo
from SMTP import SMTP
from http.server import BaseHTTPRequestHandler, HTTPServer


# HTTPRequestHandler class
class RequestHandler(BaseHTTPRequestHandler):
    sender = 'tuplovdivproject@gmail.com'
    password = '61530412'
    receivers = ['IvanZdravkovBG@gmail.com', 'Trifon.Dardzhonov@gmail.com']

    def __init__(self):
        NetworkConnectivity(self.onPingPass, self.onPingFail).listenOn("8.8.8.8")
        UPSListener(UPS(), self.onPowerOn, self.onPowerOff).TurnOn()
        self.repo = MongoDBRepo()

    def get_routing(self, x):
        return {
            '': self.welcome,
            'getTemperature': self.get_temperature,
            'getUPSStatus': self.get_UPS_Status,
            'isThereInternet': self.ping_is_passing
        }.get(x, '')

    def welcome(self):
        return 'Welcome to the HTTP Services'

    def get_temperature(self):
        return "The current temperature is " + str(self.repo.getTemperature())

    def get_UPS_Status(self):
        return "The UPS is currently: " + 'ON' if self.repo.getUPSStatus() else 'OFF'

    def ping_is_passing(self):
        return "The internet connection is " + 'ON' if self.repo.getInternetStatus() else 'OFF'

    def onPingPass(self, params):
        self.updateInternetStatus(True, params)
        return

    def onPingFail(self, params):
        self.updateInternetStatus(False, params)
        return

    def onPowerOn(self, params):
        self.updateUPSStatus(True, params)
        return

    def onPowerOff(self, params):
        self.updateUPSStatus(False, params)
        return

    def updateUPSStatus(self, isUpsOn, data):
        data.isUpsOn = isUpsOn
        self.repo.updateUPSStatus(data)

        if self.repo.getInternetStatus() is True:
            if isUpsOn is True:
                self.sendEmail('Power ON', 'Power just came back!')
            else:
                self.sendEmail('Power DOWN', 'Power went down!')

        return

    def updateInternetStatus(self, isThereInternet, data):
        data.isThereInternet = isThereInternet
        self.repo.updateInternetStatus(data)

        if isThereInternet is True:
            self.sendEmail('Internet ON', 'The internet just came ON on the server!')

        return

    def sendEmail(self, subject, message):
        SMTP(self.sender, self.password, self.receivers).send_email_message(subject, message)
        return

    def do_GET(self):
        # Send response status code
        self.send_response(200)

        # Send headers
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        # Write content as utf-8 data
        route = self.path[8:]
        func = self.get_routing(route)
        result = func()
        bytes_result = bytes(result, "utf8")
        self.wfile.write(bytes_result)
        return


def run():
    print('starting server...')

    # Server settings
    # Choose port 8080, for port 80, which is normally used for a http server, you need root access
    server_address = ('127.0.0.1', 8080)
    httpd = HTTPServer(server_address, RequestHandler)
    print('running server...')
    httpd.serve_forever()


run()