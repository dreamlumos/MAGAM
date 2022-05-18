import numpy as np
import pandas as pd


class Fusion:

	def __init__(self, left_matrix, right_matrix, function):
		self.left_matrix = left_matrix
		self.function = function
		self.right_matrix = right_matrix
		self.calculate_recommendations()

	def calculate_recommendations(self):

		recommendations = self.function(self.left_matrix, self.right_matrix)

		if type(recommendations) == np.ndarray:
				recommendations = pd.DataFrame(recommendations, index=self.left_matrix.index, columns=list(self.right_matrix.columns.values))
			
		self.recommendations = recommendations 

	def get_recommendations(self):
		return self.recommendations
