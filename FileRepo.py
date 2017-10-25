import json
import ast

class FileRepo:
    tempFileName = None
    upsFileName = None
    internetFileName = None

    def __init__(self):
        self.tempFileName = 'temperature.txt'
        self.upsFileName = 'ups.txt'
        self.internetFileName = 'internet.txt'

    def getTemperature(self):
        # with open(self.tempFileName, 'r') as file:
        #    if os.stat(file).st_size > 0:
        #       last_temp = list(file)[-1]

        return 30.0

    def getUPSStatus(self):
        with open(self.upsFileName, 'r') as file:
            content = file.readlines()
            content = [x.strip() for x in content]
            last = content[0]
            dataJson = ast.literal_eval(last)

        return dataJson['isUpsOn']

    def getInternetStatus(self):
        with open(self.internetFileName) as file:
            content = file.readlines()
            content = [x.strip() for x in content]
            last = content[0]
            dataJson = ast.literal_eval(last)

        return dataJson

    def updateUPSStatus(self, data):
        with open(self.upsFileName, 'a') as file:
            str_data = str(data)
            file.write(str_data + '\n')

    def updateInternetStatus(self, data):
        with open(self.internetFileName, 'a') as file:
            str_data = str(data)
            file.write(str_data + '\n')