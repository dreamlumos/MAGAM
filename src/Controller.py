from models.SystemState import *
from models.Aspect import *

class Controller:

	def __init__(self, system_state):
		self.system_state = system_state
		self.system_data = system_state.get_data()

	def create_aspect_empty():
		aspect = Aspect()
		self.system_data.add_aspect(aspect)

	def update_aspect(self, aspect_id, aspect_type, users_file, activities_file, function_name):
		# TODO: users/activities_file -> qtables

		aspect = self.data.get_aspect(aspect_id)

		aspect.set_aspect_type(aspect_type)
		aspect.set_users(users_file=users_file)
		aspect.set_activities(activities_file=activities_file)
		calc_fn = calculations.BasicFunctions.functions[function_name]
		aspect.set_applied_function(cal_fn)

		users_array = aspect.get_users_array()
		activities_array = aspect.get_activities_array()
		recommendations_array = aspect.get_recommendations()

		return users_array, activities_array, recommendations_array

	def change_users(self, aspect_id, users_file=None, users_array=None):
		"""
		Either enter users_file OR users_array. If both are provided, users_file will be used.
		Raises an IllegalArgumentError if neither is provided, or if the argument value is None.

		:param users_file: CSV file containing the users (TODO: other formats)
		:param users_array: array containing the users

		:type users_file: str
		:type users_array: Dataframe (TODO: other formats?)
		"""

		aspect = self.data.get_aspect(aspect_id)

		if users_file != None:
			aspect.set_users(users_file=users_file)

		elif users_array != None:
			aspect.set_users(users_file=users_file)

		else:
			raise IllegalArgumentError

	def change_activities(self, aspect_id, activities_file=None, activities_array=None):
		"""
		Either enter activities_file OR activities_array. If both are provided, activities_file will be used.
		Raises an IllegalArgumentError if neither is provided, or if the argument value is None.

		:param activities_file: CSV file containing the activities (TODO: other formats)
		:param activities_array: array containing the activities

		:type activities_file: str
		:type activities_array: Dataframe (TODO: other formats?)
		"""

		aspect = self.data.get_aspect(aspect_id)

		if activities_file != None:
			aspect.set_activities(activities_file=activities_file)

		elif activities_array != None:
			aspect.set_activities(activities_file=activities_file)

		else:
			raise IllegalArgumentError

	def change_function(self, aspect_id, function):
		aspect = self.data.get_aspect(aspect_id)
		aspect.set_applied_function(function)

	def get_recommendations(self, aspect_id, function=None):
		aspect = self.data.get_aspect(aspect_id)
		return aspect.get_recommendations(function)

	def delete_aspect(self, aspect_id):
		self.system_date.delete_aspect(aspect_id)

	def convert_to_csv(qtable):
		# TODO
		return "test.csv"