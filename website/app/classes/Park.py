class Park(object):
    def __init__(self, data):
        self.destination = None
        self.distance = None
        self.duration = None
        self.photo_url = None
        '''Initialize the object from the data'''
        self.__initialize__(data)

    def __initialize__(self, data):
        '''TODO'''
        temp = list(data)
        self.destination = temp[0]
        self.distance = temp[1]['text']
        self.duration = temp[2]['text']

    def __repr__(self):
        return f'Destination: {self.destination}\nDistance: {self.distance}\nETA: {self.duration}'