
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from models.SystemState import *
from models.Aspect import *
from models.Fusion import *
from calculations import *
from fusion import *


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

		users_qtable = self.df_to_qtable(users_array)
		activities_qtable = self.df_to_qtable(activities_array)
		recommendations_qtable = self.df_to_qtable(recommendations_array)

		return users_qtable, activities_qtable, recommendations_qtable

	def update_aspect_from_qtables(self, aspect_id, aspect_type, users_qtable, activities_qtable, recommendations_qtable, function_name):

		users_array = self.qtable_to_df(users_qtable)
		activities_array = self.qtable_to_df(activities_qtable)

		aspect = self.system_data.get_aspect(aspect_id)

		aspect.set_aspect_type(aspect_type)
		aspect.set_users(users_array=users_array)
		aspect.set_activities(activities_array=activities_array)
		calc_fn = basic_functions[function_name]
		aspect.set_applied_function(calc_fn)

		# users_array = aspect.get_users_array()
		# activities_array = aspect.get_activities_array()
		recommendations_array = aspect.get_recommendations()
		recommendations_qtable = self.df_to_qtable(recommendations_array, recommendations_qtable)

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
		table = self.df_to_qtable(rec, table)
		return table


	# --------- UTILS --------- #

	# TODO: move them to a separate util file

	def qtable_to_df(self, qtable):  # TODO check size of matrix with "headers"
		col_count = qtable.columnCount()
		row_count = qtable.rowCount()
		for i in range(1, col_count):
			if qtable.item(0, i) is None:
				col_count = i
				break
		for i in range(1, row_count):
			print(type(qtable.item(i, 0)) is None)
			if qtable.item(i, 0) is None:
				row_count = i
				break
		print(col_count)
		print(row_count)
		headers = [str(qtable.item(0, i).text()) for i in range(1, col_count)]
		ind = [str(qtable.item(i, 0).text()) for i in range(1, row_count)]
		print(headers)
		print(ind)
		df_row = []
		for row in range(1, row_count):
			df_col = []
			for col in range(1, col_count):
				table_item = qtable.item(row, col)
				df_col.append(0 if table_item is None else int(table_item.text()))
			df_row.append(df_col)

		df = pd.DataFrame(df_row, index=ind, columns=headers)
		return df

	def nparray_to_qtable(self, table):
		nb_rows, nb_cols = table.shape
		if nb_cols is None:
			nb_cols = 0

		qtable = QTableWidget()

		qtable.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

		qtable.setRowCount(nb_rows)
		qtable.setColumnCount(nb_cols)

		qtable.verticalHeader().setVisible(False)
		qtable.horizontalHeader().setVisible(False)

		for i in range(nb_rows):
			for j in range(nb_cols):
				s = str(table[i, j])
				item = QTableWidgetItem(s)
				item.setTextAlignment(Qt.AlignCenter)
				qtable.setItem(i+1, j+1, item)

		return qtable


	def df_to_qtable(self, dataframe, qtable=None):

		nb_rows = dataframe.shape[0] + 1
		nb_columns = dataframe.shape[1] + 1

		headers = list(dataframe.columns.values)
		index = dataframe.index

		if qtable is None:
			qtable = QTableWidget()

		qtable.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

		qtable.setRowCount(nb_rows)
		qtable.setColumnCount(nb_columns)

		qtable.verticalHeader().setVisible(False)
		qtable.horizontalHeader().setVisible(False)

		for i in range(1, nb_rows):
			item = QTableWidgetItem(index[i - 1])
			item.setTextAlignment(Qt.AlignCenter)
			qtable.setItem(i, 0, item)

		# qtable.resizeColumnsToContents()

		for i in range(1, nb_columns):
			item = QTableWidgetItem(headers[i - 1])
			item.setTextAlignment(Qt.AlignCenter)
			qtable.setItem(0, i, item)
			# qtable.resizeColumnsToContents()

		# qtable.resizeColumnsToContents()

		for i in range(nb_rows-1):
			for j in range(nb_columns-1):
				s = str(dataframe.iloc[i, j])
				item = QTableWidgetItem(s)
				item.setTextAlignment(Qt.AlignCenter)
				qtable.setItem(i+1, j+1, item)

		# Resize the table to fit its content
		# qtable.resizeColumnsToContents()

		return qtable

	def save_as_csv(self, parent, qtable):
		file_name = QFileDialog.getSaveFileName(parent, "Save as .csv", "./", "*.csv")
		if file_name != ('', ''):
			file = open(file_name[0], "a")
			file.write(self.qtable_to_df(qtable).to_csv())
			file.close()
		return file_name[0]

	def load_csv(self, parent):
		file = QFileDialog.getOpenFileName(parent, "Open File", "../data", "CSV (*.csv)")
		file_name = file[0]
		if len(file_name) > 0:
			return file_name
		else:
			return None

	def load_from_csv(self, parent, qtable=None):
		file_name = self.load_csv(parent)
		if file_name != None:
			dataframe = pd.read_csv(file_name, sep=',', index_col=0)
			qtable = self.df_to_qtable(dataframe, qtable)
			return qtable