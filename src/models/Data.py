class Data:

	def __init__(self):

		self.aspects = dict()
		self.aspect_counter = 0

	def add_aspect(self, aspect, verbose=False):
		aspect_id = self.aspect_counter
		self.aspects[aspect_id] = aspect
		self.aspect_counter += 1
		
		if verbose:
			print("Aspect added")

		return aspect_id

	def get_aspect(self, aspect_id):
		return self.aspects[aspect_id]

	def get_aspects(self):
		return self.aspects

	def delete_aspect(self, aspect_id):
		return self.aspects.pop(aspect_id)

	def export_to_pkl(self):
		# TODO
		pass