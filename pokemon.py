#########################################
#              pokemon.py               #
#     Non-generic data structures       #
#########################################


class Pokemon:
	def __init__(self, name=None, page=None, number=None):
		self.number = number
		self.name = name
		self.type1 = None
		self.type2 = None
		self.page = page
		self.weight = None
		self.moves = []
		self.description = ""


class Move:
	def __init__(self, name=None, type=None, category=None, condition=None):
		self.name = name
		self.type = type
		self.category = category
		self.condition = condition
