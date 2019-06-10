from math import ceil

class Park(object):
    def __init__(self, data):
        self.name = None
        self.destination = None
        self.rating = None
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
        self.rating = temp[2]
        # multiply the number of kilometers by 0.62137.
        self.distance = str(int(float(temp[3]['value']) * 0.00062137)) + ' Miles'
        self.duration = temp[4]['text']

    def __repr__(self):
        return f'Name: {self.name}\nDestination: {self.destination}\nRating: {self.rating}\nDistance: {self.distance}\nETA: {self.duration}'


# class Pagination(object):

#     def __init__(self, page, per_page, total_count):
#         self.page = page
#         self.per_page = per_page
#         self.total_count = total_count

#     @property
#     def pages(self):
#         return int(ceil(self.total_count / float(self.per_page)))

#     @property
#     def has_prev(self):
#         return self.page > 1

#     @property
#     def has_next(self):
#         return self.page < self.pages

#     def iter_pages(self, left_edge=2, left_current=2,
#                 right_current=5, right_edge=2):
#         last = 0
#         for num in xrange(1, self.pages + 2):
#             if num <= left_edge or \
#                 (num > self.page - left_current - 1 and \
#                 num < self.page + right_current) or \
#                 num > self.pages - right_edge:
#                 if last + 1 != num:
#                     yield None
#                 yield num
#                 last = num