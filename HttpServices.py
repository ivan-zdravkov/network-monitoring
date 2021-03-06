#!/usr/bin/env python
import _thread
import configparser
import ast
from NetworkConnectivity import NetworkConnectivity
from UPSListener import UPS
from UPSListener import UPSListener
from FileRepo import FileRepo
from SMTP import SMTP
from http.server import BaseHTTPRequestHandler, HTTPServer

def IpAddresses(config):
    ipAddresses = ast.literal_eval(config.get('Network', 'ipAddresses'))
    return ipAddresses

def receiversEmails(config):
    receivers = ast.literal_eval(config.get('Email', 'receivers'))
    return receivers

class http_server:
    sender = ''
    password = ''
    receivers = []
    repo = None
    networkProvider = NetworkConnectivity(None, None)

    def __init__(self):
        self.repo = FileRepo()

        config = configparser.ConfigParser()
        config.read("config.ini")

        self.sender = config.get('Email', 'sender')
        self.password = config.get('Email', 'password')
        self.receivers = receiversEmails(config)

    def welcome(self):
        return 'Welcome to the HTTP Services'

    def get_temperature(self):
        return "The current temperature is " + str(self.repo.getTemperature())

    def get_UPS_Status(self):
        return "The UPS is currently: " + ('ON' if self.repo.getUPSStatus() else 'OFF')

    def ping_is_passing(self):
        internet_status = self.repo.getInternetStatus()
        return "The internet connection is " + ('ON' if internet_status.isThereInternet else ('OFF. No internet on: ' + internet_status.hosts + ' hosts'))

    def onPingPass(self, params):
        self.updateInternetStatus(params)
        return

    def onPingFail(self, params):
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
        self.repo.updateUPSStatus(data)

        if isUpsOn is True:
            self.sendEmail('Power ON', 'Power just came back!')
        else:
            self.sendEmail('Power DOWN', 'Power went down!')

    def updateInternetStatus(self, data):
        self.repo.updateInternetStatus(data)
        internetStatusForHost = "ON" if str(data['isThereInternet']) else "OFF"
        subject = 'Internet ' + internetStatusForHost
        message = 'The internet just came ' + internetStatusForHost + ' on ' + data['host']
        self.sendEmail(subject, message)

    def sendEmail(self, subject, message):
        if(self.networkProvider.ping('8.8.8.8')):
            SMTP(self.sender, self.password, self.receivers).send_email_message(subject, message)

# HTTPRequestHandler class
class RequestHandler(BaseHTTPRequestHandler):
    http_server_instance = None

    def get_routing(self, x):
        return {
            '': self.http_server_instance.welcome,
            'getTemperature': self.http_server_instance.get_temperature,
            'getUPSStatus': self.http_server_instance.get_UPS_Status,
            'isThereInternet': self.http_server_instance.ping_is_passing
        }.get(x, '')

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
    config = configparser.ConfigParser()
    config.read("config.ini")
    
    address = config.get('Server', 'address')
    port = int(config.get('Server', 'port'))

    print('starting server...')

    # Server settings
    # Choose port 8080, for port 80, which is normally used for a http server, you need root access
    server_address = (address, port)
    httpd = HTTPServer(server_address, RequestHandler)

    server = http_server()

    RequestHandler.http_server_instance = server

    ips = IpAddresses(config)
    _thread.start_new_thread(NetworkConnectivity(server.onPingPass, server.onPingFail).listenOn, (ips,))
    print('Network connectivity running ...')

    _thread.start_new_thread(UPSListener(UPS(), server.onPowerOn, server.onPowerOff).TurnOn, ())
    print('UPS listener running ...')

    print('running server...')
    httpd.serve_forever()


run()