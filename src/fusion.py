import numpy as np
import pandas as pd

class FusionFunctions:

	functions = ["mean", "value_multiplication", "min", "max"]

	@staticmethod
	def mean(r1, r2, w1=1, w2=1):
		return np.average([r1, r2], axis=0, weights=[w1, w2])
	
	@staticmethod
	def value_multiplication(r1, r2):

		rows, columns = r1.shape

		recommendations = np.zeros((rows, columns))
		for i in range(rows):
			for j in range(columns):
				recommendations[i, j] = r1[i, j] * r2[i, j]

		return recommendations

	@staticmethod
	def min(r1, r2):
		return np.minimum(r1, r2)

	@staticmethod
	def max(r1, r2):
		return np.maximum(r1, r2)

# check whether the shapes are the same? probably better to put safety mechanisms at a higher level 


# todo: normalisation

# todo: slide 11, selection of activity (best for each student, for the group, etc)