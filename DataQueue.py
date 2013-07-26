from django.core.cache import cache
class DataQueue(object):
    max_size = 60
    cache_key = ""
    data = []

    def __init__(self, cache_key, max_size=None):
        if max_size:
            self.set_max_size(max_size)

        self.set_cache_key(cache_key)
        self.retrieve()

    #these setters probably have a more pythonic way
    def set_max_size(self, max_size):
        self.max_size = int(max_size)

    def set_cache_key(self, cache_key):
        self.cache_key = str(cache_key)

    def trim(self):
        #incredibly simple, no prioritizing.  keeps most recent max_size
        self.data = self.data[-1*self.max_size:]

    def pop(self, number=1):
        return_list = []
        for i in range(0,number):
            try:
                return_list.append(self.data.pop(0))
            except IndexError:
                return return_list
        return return_list
        self.store()

    #self.data is not getting a value here... maybe it's a problem with 2 instances of dataqueue?
    def push(self, new_data):
        if not isinstance(new_data, list):
            new_data = [new_data]

        for cell in new_data:
            self.data.append(cell)
        self.store()


    def store(self):
        self.trim()
        queue_cache_dict = {'max_size': self.max_size, 'data':self.data }
        cache.set(self.cache_key, queue_cache_dict)

    #self.data is not getting a value here... maybe it's a problem with 2 instances of dataqueue?
    def retrieve(self):
        cache_data = cache.get(self.cache_key) 
        if cache_data: #verify cache hit. miss is handled by constructor and variable initialization
            self.max_size = cache_data['max_size']
            self.data = cache_data['data']
