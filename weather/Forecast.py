class Forecast(dict):
    def __init__(self, date, temp, description):
        dict.__init__(self, date=date, temp=temp, description=description)