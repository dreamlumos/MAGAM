from pyBKT.models import Model
import pandas as pd
import numpy as np


class BKTData():

	def __init__(self, training_data_path, model_seed=42, model_defaults=None):

		self.training_data_path = training_data_path

		if model_defaults == None:
			self.model_defaults = {'user_id': 'user_id', 'skill_name': 'skill_name', 'correct': 'correct'}
		else:
			self.model_defaults = model_defaults

		self.model = Model(seed = model_seed, num_fits = 1, defaults = model_defaults)
		self.train()

	def train(self):
		self.model.fit(self.training_data_path)

	def predict(self, data_path=None):

		if data_path == None:
			data_path = self.training_data_path

		preds_df = self.model.predict(data_path = data_path)
		preds_np = np.array(preds_df)

		user_id_column_name = self.model_defaults["user_id"]
		user_id_column_index = preds_df.columns.get_loc(user_id_column_name)
		concepts_column_name = self.model_defaults["skill_name"]
		concepts_column_index = preds_df.columns.get_loc(concepts_column_name)

		self.user_ids = np.unique(preds_np[:, user_id_column_index]) # list of user_id
		self.concepts = np.unique(preds_np[:, concepts_column_index]) # list of concepts

		all_knowledge_states = []
		for id in self.user_ids:
			preds_id = preds_df[preds_df[user_id_column_name] == id]
			preds_id_np = np.flipud(np.array(preds_id)) # reverse chronological order (last activity done being on top)
			knowledge_states = []
			for c in self.concepts:
				i = 0
				while i < len(preds_id_np) and preds_id_np[i, concepts_column_index] != c: # looking for the last activity done by this student for concept c
					i += 1
				if i >= len(preds_id_np): # student has not done an activity with this concept
					knowledge_states.append(0.5)
				else:
					knowledge_states.append(preds_id_np[i, -1]) # append the most recent state prediction

			all_knowledge_states.append(knowledge_states)

		self.users_predicted_knowledge = np.array(all_knowledge_states).T
	
	def get_users_predicted_knowledge(self):
		if not(hasattr(self, "users_predicted_knowledge")):
			self.predict()
		
		return self.users_predicted_knowledge

	def save_preds_to_csv(self, path="./predictions.csv"):
		if not(hasattr(self, "users_predicted_knowledge")):
			self.predict()
		
		final_df = pd.DataFrame(self.users_predicted_knowledge, index=self.concepts)
		final_df.sort_index(axis=0)
		final_df.sort_index(axis=1)

		return final_df.to_csv(path, header=self.user_ids)
