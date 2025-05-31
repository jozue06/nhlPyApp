class Player(object):
    def __init__(self, p):
        for key in p:
            setattr(self, key, p[key])
