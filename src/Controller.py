from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from models.SystemState import *
from models.Aspect import *
from models.Fusion import *
from views.TabContainer import *
from calculations import *
from fusion import *
import utils


class Controller:

	def __init__(self, system_state):
		self.system_state = system_state
		self.system_data = system_state.get_data()
		self.fusion_tab = None

	def set_fusion_tab(self, fusion_tab):
		self.fusion_tab = fusion_tab
		print("test")

	# --------- ASPECTS --------- #

	def add_empty_aspect(self):
		aspect = Aspect()
		aspect_id = self.system_data.add_aspect(aspect)
		self.update_fusion_tab()
		return aspect_id

	def delete_aspect(self, aspect_id):
		self.system_data.delete_aspect(aspect_id)
		self.update_fusion_tab()

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

		self.update_fusion_tab()

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

		recommendations_array = aspect.get_recommendations()
		recommendations_qtable = utils.df_to_qtable(recommendations_array, recommendations_qtable)
		
		self.update_fusion_tab()

		return users_qtable, activities_qtable, recommendations_qtable

	def get_recommendations(self, aspect_id, function=None):
		aspect = self.system_data.get_aspect(aspect_id)
		return aspect.get_recommendations(function)

	# --------- FUSION --------- #

	def create_fusion(self, id1, id2, function_name, table):
		func = fusion_functions[function_name]

		if id1[0:6] == "Fusion":
			rec1 = self.system_data.get_fusion(int(id1[-1])).get_recommendations()
		else:
			rec1 = self.system_data.get_aspect(int(id1[-1])).get_recommendations()

		if id2[0:6] == "Fusion":
			rec2 = self.system_data.get_fusion(int(id2[-1])).get_recommendations()
		else:
			rec2 = self.system_data.get_aspect(int(id2[-1])).get_recommendations()

		f = Fusion(rec1, rec2, func)
		self.system_data.add_fusion(f)
		rec = f.get_recommendations()
		print(rec)
		table = utils.df_to_qtable(rec, table)

		self.update_fusion_tab()
		return table

	def update_fusion_tab(self):

		combobox_list = []

		aspects_dict = self.system_data.get_aspects()
		for a in aspects_dict.keys():
			aspect_type = aspects_dict.get(a).get_aspect_type()
			if aspect_type is not None:
				print(aspect_type)
				print(a)
				combobox_list.append("Aspect " + aspect_type + " " + str(a))

		fusions_dict = self.system_data.get_fusions()
		print("fusion list: " + str(len(fusions_dict)))
		for f in fusions_dict.keys():
			print(f)
			combobox_list.append("Fusion " + str(f))

		if self.fusion_tab is not None:
			self.fusion_tab.update_combobox_list(combobox_list)
