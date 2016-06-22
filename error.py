class EOF(Exception):
	def __init__(self,value = None):
		self.value = value

class EMPTY_RC(Exception):
	def __init__(self,value = None):
		self.value = value
