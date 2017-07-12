#!/usr/bin/env python


from NetworkConnectivity import NetworkConnectivity
from UPSListener import UPSListener
from SMTP import SMTP
from http.server import BaseHTTPRequestHandler, HTTPServer


# HTTPRequestHandler class
class RequestHandler(BaseHTTPRequestHandler):
    sender = 'tuplovdivproject@gmail.com'
    password = '61530412'
    receivers = ['IvanZdravkovBG@gmail.com', 'Trifon.Dardzhonov@gmail.com']

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
        return "The temp is 30 degrees!"

    def get_UPS_Status(self):
        smtp = SMTP(self.sender, self.password, self.receivers)
        smtp.send_email_message("UPS is on!", "UPS is ON!")
        return "UPS is ON!"

    def ping_is_passing(self):
        connection = NetworkConnectivity(self.onPingPass, self.onPingFail)
        return str(connection.ping('8.8.8.8'))

    def onPingPass(self, param):
        return 'true'

    def onPingFail(self, param):
        return 'false'

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