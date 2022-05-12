class Fusion:

	def __init__(self, left_matrix, right_matrix, function):
		self.left_matrix = None
		self.function = None
		self.right_matrix = None 
		calculate_recommendations()

	def calculate_recommendations(self):
		self.recommendations = self.function(self.left_matrix, self.right_matrix) 

	def get_recommendations(self):
		return self.recommendations
