class SaveAsCSVButton(QPushButton):

	def __init__(self):

		super().__init__("Save as .csv")

		self.connect(on_click)


	def on_click():
		fileName = QFileDialog.getSaveFileName(self, "Save as .csv", "./", "*.csv")
        if fileName != ('', ''):
            file = open(fileName[0], "a")
            file.write(self.textEdit.toPlainText())
            file.close()
            print(fileName[0])