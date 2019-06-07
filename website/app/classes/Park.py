class Park(object):
    def __init__(self, data):
        self.name = None
        self.destination = None
        self.distance = None
        self.duration = None
        # self.photo_url = None
        '''Initialize the object from the data'''
        self.__initialize__(data)

    def __initialize__(self, data):
        '''TODO'''
        temp = list(data)
        self.name = temp[0]
        self.destination = temp[1]
        # multiply the number of kilometers by 0.62137.
        self.distance = str(int(float(temp[2]['value']) * 0.00062137)) + ' Miles'
        self.duration = temp[3]['text']

    def __repr__(self):
        return f'Name: {self.name}\nDestination: {self.destination}\nDistance: {self.distance}\nETA: {self.duration}'