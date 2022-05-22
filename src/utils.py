from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import pandas as pd

def qtable_to_df(qtable):  # TODO check size of matrix with "headers"
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


def nparray_to_qtable(table):
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


def df_to_qtable(dataframe, qtable=None):

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


def save_as_csv(parent, qtable):
	file_name = QFileDialog.getSaveFileName(parent, "Save as .csv", "./", "*.csv")
	if file_name != ('', ''):
		file = open(file_name[0], "a")
		file.write(qtable_to_df(qtable).to_csv())
		file.close()
	return file_name[0]


def load_csv(parent):
	file = QFileDialog.getOpenFileName(parent, "Open File", "../data", "CSV (*.csv)")
	file_name = file[0]
	if len(file_name) > 0:
		return file_name
	else:
		return None


def load_from_csv(parent, qtable=None):
	file_name = load_csv(parent)
	if file_name is not None:
		dataframe = pd.read_csv(file_name, sep=',', index_col=0)
		qtable = df_to_qtable(dataframe, qtable)
		return qtable
