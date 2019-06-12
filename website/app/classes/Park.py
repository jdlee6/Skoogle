from math import ceil

class Park(object):
    def __init__(self, data):
        self.name = None
        self.destination = None
        self.rating = None
        self.distance = None
        self.duration = None
        self.photo_url = None
        '''Initialize the object from the data'''
        self.__initialize__(data)

    def __initialize__(self, data):
        '''TODO'''
        temp = list(data)
        self.name = temp[0]
        self.destination = temp[1]
        self.rating = temp[2]
        # multiply the number of kilometers by 0.62137.
        self.distance = str(int(float(temp[3]['value']) * 0.00062137)) + ' Miles'
        self.duration = temp[4]['value']
        self.photo_url = temp[5]

    def __repr__(self):
        return f'Name: {self.name}\nDestination: {self.destination}\nRating: {self.rating}\nDistance: {self.distance}\nETA: {self.duration}'