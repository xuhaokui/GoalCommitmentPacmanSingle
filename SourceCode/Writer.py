<<<<<<< HEAD

import pandas as pd 
import os 

class WriteDataFrameToCSV():
	def __init__(self,saveResultFile):
		self.saveResultFile=saveResultFile
	def __call__(self,responseDF):
		if not os.path.isfile(self.saveResultFile):
			responseDF.to_csv(self.saveResultFile, header=list(responseDF.columns))
		else:
=======

import pandas as pd 
import os 

class WriteDataFrameToCSV():
	def __init__(self,saveResultFile):
		self.saveResultFile=saveResultFile
	def __call__(self,responseDF):
		if not os.path.isfile(self.saveResultFile):
			responseDF.to_csv(self.saveResultFile, header=list(responseDF.columns))
		else:
>>>>>>> 67e6e0972d5a596e2dd27e6e9dfe81cd4d17d33b
			responseDF.to_csv(self.saveResultFile, mode='a', header=False)