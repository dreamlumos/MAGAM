class Data:

	def __init__(self):

		self.aspects = dict()
		self.aspect_counter = 0

		self.fusions = dict()  # key: fusion id, value: Fusion object
		self.fusion_counter = 0

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

	def add_fusion(self, fusion, verbose=False):
		fusion_id = self.fusion_counter
		self.fusions[fusion_id] = fusion  # fusion is a table
		self.fusion_counter += 1

		if verbose:
			print("Fusion added")

		return fusion_id

	def get_fusion(self, fusion_id):
		return self.fusions[fusion_id]

	def get_fusions(self):
		return self.fusions

	def delete_fusion(self, fusion_id):
		return self.fusions.pop(fusion_id)

