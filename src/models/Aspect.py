import pandas as pd
import numpy as np


class Aspect:

	aspect_types = ["Didactic", "Pedagogic", "Motivational", "Strategic", "Learning style", "Gaming"]

	def __init__(self, aspect_type, users, activities, users_scale, activities_scale):
		"""
		aspect_type : string
		users : matrix
		activities : matrix
		[users/activities]_scale : tuple containing two floats representing the min and max values of the scale used
		"""

		self.aspect_type = aspect_type
		self.users = users
		self.activities = activities
		self.users_scale = users_scale
		self.activities_scale = activities_scale
		self.calc_function = None # function
		self.recommendations = None # np.array

	@classmethod
	def create_from_csv(cls, aspect_type, users_file, activities_file, users_scale, activities_scale):
		"""
		users_file: name of CSV file containing users
		activities_file: name of CSV file containing activities
		"""

		users_df = pd.read_csv(users_file, sep=',', index_col=0)
		users = np.array(users_df)
		users = users.T

		activities_df = pd.read_csv(activities_file, sep=',', index_col=0)
		activities = np.array(activities_df)

		# note: df left here in case necessary later for lookup purposes (using row or column names)
		# maybe create a class which keeps both ndarray and df?

		return cls(aspect_type, users, activities, users_scale, activities_scale)

	@classmethod 
	def create_from_json(cls, users_file, activities_file, aspect_type, users, activities, users_scale, activities_scale):
		print("create_from_json: This method has yet to be implemented.")
		# TODO

	@classmethod 
	def create_from_pkl(cls, users_file, activities_file, aspect_type, users, activities, users_scale, activities_scale):
		print("create_from_pkl: This method has yet to be implemented.")
		# TODO

	def calculate_recommendations(self, function):
		"""
		function: function to be used to calculate the recommendations, must take a users ndarray, and an activities ndarray
		"""

		self.calc_function = function # store name or function? storing in case we want to export the data to review later
		self.recommendations = function(self.users, self.activities)

		# to store or not to store the result as a class attribute? 
		# user will be able to visualise the results of different calculations, but there needs
		# to be one selected result to be used in the fusion...
