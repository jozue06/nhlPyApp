class Player(object):
	def __init__(self, p, index):
		setattr(self, "index", index)
		for key in p:
			setattr(self, key, p[key])