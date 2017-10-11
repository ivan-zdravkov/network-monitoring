class FileRepo:
    tempFileName = None
    upsFileName = None
    internetFileName = None

    def __init__(self):
        self.tempFileName = 'temperature.txt'
        self.upsFileName = 'ups.txt'
        self.internetFileName = 'internet.txt'

    def getTemperature(self):
        with open(self.tempFileName, 'r') as file:
            last_temp = list(file)[-1]

        return last_temp

    def getUPSStatus(self):
        with open(self.upsFileName, 'r') as file:
            last_ups_status = list(file)[-1]

        return last_ups_status

    def getInternetStatus(self):
        with open(self.internetFileName, 'r') as file:
            internet_status = list(file)[-1]

        return internet_status

    def updateUPSStatus(self, data):
        with open(self.upsFileName, 'w') as file:
            str_data = str(data)
            file.write(str_data + '\n')

    def updateInternetStatus(self, data):
        with open(self.internetFileName, 'w') as file:
            str_data = str(data)
            file.write(str_data + '\n')