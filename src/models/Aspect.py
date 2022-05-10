import pandas as pd
import numpy as np


class Aspect:

	aspect_types = ["Didactic", "Pedagogic", "Motivational", "Strategic", "Learning style", "Gaming"]

	def __init__(self, aspect_type, users, user_names, users_scale, activities, activity_names, activities_scale, func):
		"""
		aspect_type : string
		users : ndarray
		activities : ndarray
		[users/activities]_names : list[str] 
		[users/activities]_scale : tuple containing two floats representing the min and max values of the scale used
		"""

		self.aspect_type = aspect_type

		self.users = users
		self.user_names = user_names
		self.users_scale = users_scale

		self.activities = activities
		self.activity_names = activity_names
		self.activities_scale = activities_scale

		self.calc_function = func # function
		self.recommendations_dict = dict() # key: function name, value: ndarray containing recommendations
		self.chosen_recommendations = None;

	@classmethod
	def create_from_csv(cls, aspect_type, users_file, users_scale, activities_file, activities_scale, func):
		"""
		users_file: name of CSV file containing users
		activities_file: name of CSV file containing activities
		"""

		users_df = pd.read_csv(users_file, sep=',', index_col=0)
		users = np.array(users_df)
		users = users.T
		user_names = list(users_df.columns.values)

		activities_df = pd.read_csv(activities_file, sep=',', index_col=0)
		activities = np.array(activities_df)
		activity_names = list(activities_df.columns.values)

		# note: df left here in case necessary later for lookup purposes (using row or column names)
		# maybe create a class which keeps both ndarray and df?

		return cls(aspect_type, users, user_names, users_scale, activities, activity_names, activities_scale, func)

	@classmethod 
	def create_from_json(cls, aspect_type, users_file, users_scale, activities_file, activities_scale):
		print("create_from_json: This method has yet to be implemented.")
		# TODO

	@classmethod 
	def create_from_pkl(cls, aspect_type, users_file, users_scale, activities_file, activities_scale):
		print("create_from_pkl: This method has yet to be implemented.")
		# TODO

	def calculate_recommendations(self, function):
		"""
		function: function to be used to calculate the recommendations, must take a users ndarray, and an activities ndarray
		"""

		if function not in self.recommendations_dict:
			self.recommendations_dict[function] = function(self.users, self.activities)

		self.chosen_recommendations = self.recommendations_dict[function]

		# self.calc_function = function # store name or function? storing in case we want to export the data to review later

		# to store or not to store the result as a class attribute? 
		# user will be able to visualise the results of different calculations, but there needs
		# to be one selected result to be used in the fusion...		