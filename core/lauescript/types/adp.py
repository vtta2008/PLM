__author__ = 'Arrahed'


class ADPDataError(Exception):
    pass


class ADP(dict):
    def __init__(self, flag='anis'):
        super(ADP, self).__init__()
        self['flag'] = flag

    def __getitem__(self, item):
        try:
            return super(ADP, self).__getitem__(item)
        except KeyError:
            raise ADPDataError
        
    def __setitem__(self, key, value):
        # print key, value
        super(ADP, self).__setitem__(key, value)