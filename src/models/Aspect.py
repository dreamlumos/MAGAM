import pandas as pd
import numpy as np

import os

class Aspect:

	aspect_types = ["Didactic", "Pedagogic", "Motivational", "Strategic", "Learning style", "Gaming"]

	def __init__(self):

		self.aspect_type = None  # str

		# [users/activities]_file: str
		# [users/activities]_array: Dataframe
		# [users/activities]_names: list[str]
		# [users/activities]_scale: tuple containing two floats representing the min and max values of the scale used

		self.users_file = None
		self.users_array = None
		self.users_names = None  # TODO: maybe remove
		self.users_scale = None

		self.activities_file = None
		self.activities_array = None
		self.activities_names = None  # TODO: maybe remove
		self.activities_scale = None

		self.applied_function = None # function
		self.recommendations_dict = dict() # key: function name, value: DataFrame containing recommendations

	# ---- GENERAL ---- #

	def get_aspect_type(self):
		return self.aspect_type

	def set_aspect_type(self, aspect_type):
		self.aspect_type = aspect_type

	def aspect_filled(self):
		if self.users_array is None or self.activities_array is None:
			return False
		return True

	def coherent(self, check_property_names=False):
		# TODO: check property names?

		nb_columns_users = self.users_array.shape[0] # shape[0] because the array hasn't been transposed yet
		nb_rows_users = self.activities_array.shape[0]
		if nb_rows_users == nb_columns_users:
			return True
		else:
			return False

	# ---- USERS ---- #

	def set_users(self, users_file=None, users_array=None):
		"""
		Either enter users_file OR users_array. If both are provided, users_file will be used.
		Raises an IllegalArgumentError if neither is provided, or if the argument value is None.

		:param users_file: CSV file containing the users (TODO: other formats)
		:param users_array: array containing the users

		:type users_file: str
		:type users_array: Dataframe (TODO: other formats?)
		"""

		if users_file != None:
			if os.path.isfile(users_file) and users_file.endswith('.csv'):
				self.users_file = users_file
				self.users_array = pd.read_csv(users_file, sep=',', index_col=0)
			else:
				raise NotImplementedError("Sorry, this type of input file is not implemented yet.")
		elif type(users_array) == pd.DataFrame:
			self.users_array = users_array
		else:
			raise IllegalArgumentError("Please input either a file or an array containing the users. If you did pass an argument, its value is probably 'None' or not a DataFrame. Please rectify that.")

		self.users_names = list(self.users_array.columns.values)
		self.reset_recommendations()

	def get_users_file(self):
		return self.users_file	

	def get_users_array(self):
		return self.users_array

	def get_users_names(self):
		return self.users_names

	def set_users_scale(self, users_scale):
		self.users_scale = users_scale

	def get_users_scale(self):
		return self.users_scale

	# ---- ACTIVITIES ---- #

	def set_activities(self, activities_file=None, activities_array=None):
		"""
		Either enter activities_file OR activities_array. If both are provided, activities_file will be used.
		Raises an IllegalArgumentError if neither is provided, or if the argument value is None.

		:param users_file: CSV file containing the users (TODO: other formats)
		:param users_array: array containing the users

		:type activities_file: str
		:type activities_array: Dataframe (TODO: other formats?)
		"""

		if activities_file != None:
			if os.path.isfile(self.users_file) and self.users_file.endswith('.csv'):
				self.activities_file = activities_file
				self.activities_array = pd.read_csv(activities_file, sep=',', index_col=0)
			else:
				raise NotImplementedError("Sorry, this type of input file is not implemented yet.")
		elif type(activities_array) == pd.DataFrame:
			self.activities_array = activities_array
		else:
			raise IllegalArgumentError("Please input either a file or an array containing the activities. If you did pass an argument, its value is probably 'None' or not a DataFrame. Please rectify that.")

		self.activities_names = list(self.activities_array.columns.values)
		self.reset_recommendations()

	def get_activities_file(self):
		return self.activities_file

	def get_activities_array(self):
		return self.activities_array

	def get_activities_names(self):
		return self.activities_names

	def set_activities_scale(self, activities_scale):
		self.activities_scale = activities_scale

	def get_activities_scale(self):
		return self.activities_scale

	# ---- RECOMMENDATIONS ---- #

	def get_applied_function(self):
		return self.applied_function

	def set_applied_function(self, applied_function):
		self.applied_function = applied_function
		# calculate_recommendations()

	def get_recommendations(self, function=None):
		"""
		Calculates the recommendations.
		Raises IllegalArgumentError if there is an issue with function or self.applied_function.

		:param function: function to be applied to calculate the recommendations. If None, self.applied_function is used. The function should take two ndarrays, and return an ndarray or a DataFrame.

		:rtype: DataFrame
		"""

		if not self.aspect_filled():
			print("Please fill up the ", self.aspect_type, "aspect first.")
			return None

		if not self.coherent():
			raise ValueError("The number of columns in the users array and the number of rows in the activities array are not equal. Please rectify this.")

		if function == None:
			if self.applied_function != None:
				function = self.applied_function
			else: 
				print("Please either set a function to apply with set_applied_function(), or pass a function in the arguments.")
				return None

		if function not in self.recommendations_dict:
			#try:
			users = np.array(self.users_array)
			users = users.T
			activities = np.array(self.activities_array)
			recommendations = function(users, activities)

			if type(recommendations) == np.ndarray:
				recommendations = pd.DataFrame(recommendations, index=self.users_names, columns=self.activities_names)
			self.recommendations_dict[function] = recommendations

			# except Exception as err:
			# 	raise IllegalArgumentError("Failed to calculate the recommendations with this function:", function) from err

		return self.recommendations_dict[function]

	def reset_recommendations(self):
		self.applied_function = None
		self.recommendations_dict = dict()




class IllegalArgumentError(ValueError):
	pass