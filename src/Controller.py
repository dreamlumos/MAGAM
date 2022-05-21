from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from models.SystemState import *
from models.Aspect import *
from models.Fusion import *
from calculations import *
from fusion import *
import utils


class Controller:

	def __init__(self, system_state):
		self.system_state = system_state
		self.system_data = system_state.get_data()

	# --------- ASPECTS --------- #

	def add_empty_aspect(self):
		aspect = Aspect()
		aspect_id = self.system_data.add_aspect(aspect)
		return aspect_id

	def delete_aspect(self, aspect_id):
		self.system_data.delete_aspect(aspect_id)

	def update_aspect_from_files(self, aspect_id, aspect_type, users_file, activities_file, function_name):

		aspect = self.system_data.get_aspect(aspect_id)

		aspect.set_aspect_type(aspect_type)
		aspect.set_users(users_file=users_file)
		aspect.set_activities(activities_file=activities_file)
		calc_fn = basic_functions[function_name]
		aspect.set_applied_function(calc_fn)

		users_array = aspect.get_users_array()
		activities_array = aspect.get_activities_array()
		recommendations_array = aspect.get_recommendations()

		users_qtable = utils.df_to_qtable(users_array)
		activities_qtable = utils.df_to_qtable(activities_array)
		recommendations_qtable = utils.df_to_qtable(recommendations_array)

		return users_qtable, activities_qtable, recommendations_qtable

	def update_aspect_from_qtables(self, aspect_id, aspect_type, users_qtable, activities_qtable, recommendations_qtable, function_name):

		users_array = utils.qtable_to_df(users_qtable)
		activities_array = utils.qtable_to_df(activities_qtable)

		aspect = self.system_data.get_aspect(aspect_id)

		aspect.set_aspect_type(aspect_type)
		aspect.set_users(users_array=users_array)
		aspect.set_activities(activities_array=activities_array)
		calc_fn = basic_functions[function_name]
		aspect.set_applied_function(calc_fn)

		# users_array = aspect.get_users_array()
		# activities_array = aspect.get_activities_array()
		recommendations_array = aspect.get_recommendations()
		recommendations_qtable = utils.df_to_qtable(recommendations_array, recommendations_qtable)

		return users_qtable, activities_qtable, recommendations_qtable

	# def change_users(self, aspect_id, users_file=None, users_array=None):
	# 	"""
	# 	Either enter users_file OR users_array. If both are provided, users_file will be used.
	# 	Raises an IllegalArgumentError if neither is provided, or if the argument value is None.

	# 	:param users_file: CSV file containing the users (TODO: other formats)
	# 	:param users_array: array containing the users

	# 	:type users_file: str
	# 	:type users_array: Dataframe (TODO: other formats?)
	# 	"""

	# 	aspect = self.system_data.get_aspect(aspect_id)

	# 	if users_file is not None:
	# 		aspect.set_users(users_file=users_file)

	# 	elif users_array is not None:
	# 		aspect.set_users(users_file=users_file)

	# 	else:
	# 		raise IllegalArgumentError

	# def change_activities(self, aspect_id, activities_file=None, activities_array=None):
	# 	"""
	# 	Either enter activities_file OR activities_array. If both are provided, activities_file will be used.
	# 	Raises an IllegalArgumentError if neither is provided, or if the argument value is None.

	# 	:param activities_file: CSV file containing the activities (TODO: other formats)
	# 	:param activities_array: array containing the activities

	# 	:type activities_file: str
	# 	:type activities_array: Dataframe (TODO: other formats?)
	# 	"""

	# 	aspect = self.system_data.get_aspect(aspect_id)

	# 	if activities_file != None:
	# 		aspect.set_activities(activities_file=activities_file)

	# 	elif activities_array != None:
	# 		aspect.set_activities(activities_file=activities_file)

	# 	else:
	# 		raise IllegalArgumentError

	# def change_function(self, aspect_id, function):
	# 	aspect = self.system_data.get_aspect(aspect_id)
	# 	aspect.set_applied_function(function)

	def get_recommendations(self, aspect_id, function=None):
		aspect = self.system_data.get_aspect(aspect_id)
		return aspect.get_recommendations(function)


	# --------- FUSION --------- #
	def create_fusion(self, id1, id2, function_name, table):
		func = fusion_functions[function_name]
		if id1[0] == "A":
			rec1 = self.system_data.get_aspect(int(id1[-1])).get_recommendations()
		else:
			rec1 = self.system_data.get_fusion(int(id1[-1])).get_recommendations()

		if id2[0] == "A":
			rec2 = self.system_data.get_aspect(int(id2[-1])).get_recommendations()
		else:
			rec2 = self.system_data.get_fusion(int(id2[-1])).get_recommendations()

		f = Fusion(rec1, rec2, func)
		self.system_data.add_fusion(f)
		rec = f.get_recommendations()
		print(rec)
		table = utils.df_to_qtable(rec, table)
		return table
