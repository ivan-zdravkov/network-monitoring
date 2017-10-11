#!/usr/bin/env python

import _thread
from NetworkConnectivity import NetworkConnectivity
from UPSListener import UPS
from UPSListener import UPSListener
from FileRepo import FileRepo
from SMTP import SMTP
from http.server import BaseHTTPRequestHandler, HTTPServer


# HTTPRequestHandler class
class RequestHandler(BaseHTTPRequestHandler):
    sender = 'tuplovdivproject@gmail.com'
    password = '61530412'
    receivers = ['IvanZdravkovBG@gmail.com', 'Trifon.Dardzhonov@gmail.com']
    repo = None
    isThereInternet = True

    def __init__(self, request, client_address, server):
        self.repo = FileRepo()

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
        self.isThereInternet = True
        self.updateInternetStatus(params)

        return

    def onPingFail(self, params):
        self.isThereInternet = False
        self.updateInternetStatus(params)

        return

    def onPowerOn(self, params):
        self.updateUPSStatus(True, params)
        return

    def onPowerOff(self, params):
        self.updateUPSStatus(False, params)
        return

    def updateUPSStatus(self, isUpsOn, data):
        data['isUpsOn'] = isUpsOn
        insertedId = self.repo.updateUPSStatus(data)

        if self.isThereInternet is True:
            if isUpsOn is True:
                self.sendEmail('Power ON', 'Power just came back!')
            else:
                self.sendEmail('Power DOWN', 'Power went down!')

        return

    def updateInternetStatus(self, data):
        data['isThereInternet'] = self.isThereInternet
        insertedId = self.repo.updateInternetStatus(data)

        if self.isThereInternet is True:
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

    requestHandler = RequestHandler(None, None, None)

    ip = '8.8.8.8'
    _thread.start_new_thread(NetworkConnectivity(requestHandler.onPingPass, requestHandler.onPingFail).listenOn, (ip,))
    print('Network connectivity running ...')

    _thread.start_new_thread(UPSListener(UPS(), requestHandler.onPowerOn, requestHandler.onPowerOff).TurnOn, ())
    print('UPS listener running ...')

    print('running server...')
    httpd.serve_forever()


run()