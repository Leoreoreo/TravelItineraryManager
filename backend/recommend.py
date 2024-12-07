from db_utils import *
import requests
from gensim.models import Word2Vec
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
# import matplotlib.pyplot as plt
from collections import defaultdict
import joblib
import os
from datetime import datetime
# from flask import current_app
# from server import app

base_dir = os.getcwd()
model_path = os.path.join(base_dir, "model")
if not os.path.exists(model_path): os.makedirs(model_path)



################################################################################################################
# GENERATING CLUSTERS BASED ON ALL USER + TRIP DATA --> train kmeans + fit scaler
################################################################################################################

def users_to_df():
	# users = get_all_users() 	# print(users) # 2d array: [[id, name, trait, age], ...]
	users = return_users()
	users_dict = defaultdict(list)
  
	# creating dictionary to conver to df
	for u in users:
		users_dict['uid'].append(u[0])
		users_dict['age'].append(u[3])
		users_dict['trait'].append(u[2])
	
	df = pd.DataFrame(users_dict)

	# REPLACING NULL VALUES WITH MEAN AGE AND MOST COMMON TRAIT
	avg_age = df['age'].fillna(df['age'].mean())
	df['age'] = avg_age
	mode_trait = df['trait'].fillna(df['trait'].mode()[0])
	df['trait'] = mode_trait
  

	df_encoded = encode_df(df)
	scaler, kmeans, df = cluster_df(df, df_encoded)
  	# plot_kmeans(df)
	return scaler, kmeans, df, df_encoded

def cluster_df(df, df_encoded):
	scaler = StandardScaler()
	scaled_data = scaler.fit_transform(df_encoded)

	# Fit the model with a chosen number of clusters (e.g., 3)
	kmeans = KMeans(n_clusters=10, random_state=42)
	kmeans.fit(scaled_data) # scaled_data = age + one hot encoded preferences

	# Add cluster labels to the dataframe
	df['cluster_id'] = kmeans.labels_
	return scaler, kmeans, df

def encode_df(df):
	encoded_preferences = pd.get_dummies(df['trait'])

	# combine the one-hot encoded columns with the original dataframe
	df_encoded = pd.concat([df.drop(columns=['trait', 'uid']), encoded_preferences], axis=1)

	return df_encoded


def plot_kmeans(df):
	plt.scatter(df['age'], df['trait'], c=df['cluster_id'], cmap='viridis')
	plt.xlabel('Age')
	plt.ylabel('trait')
	plt.title('K-Means Clustering of Users Based on Age and Preference')
	plt.colorbar(label='Cluster')
	plt.show()


################################################################################################################
# TRAIN W2V BY GENERATING VECTOR EMBEDDINGS FOR ALL TRIPS
################################################################################################################

def preprocess_trip_data(trips):
	trips_sequences = []
	trip_ids = [t[0] for t in trips]
	
	for tid in trip_ids:
		stops = fetch_stops(tid)
		if stops is None:
			# print(f"{tid} has no stops in their trip")
			continue
		
		sequence = []
		
		for stop in stops:
			try:
				sequence.append(stop['location'])

			except TypeError:
				pass

		trips_sequences.append(sequence)
		
	return trips_sequences


def train_w2v():
	trips = return_trips()					  # gets all trips from all users
	trips_seq = preprocess_trip_data(trips)	 # return a list of stop sequences for every trip
	w2v = init_w2v(trips_seq)				   # trains w2v model for embedding
	
	w2v_path = os.path.join(model_path, "w2v_model.model")
	w2v.save(w2v_path)


def init_w2v(trip_sequences):
	w2v = Word2Vec(
		sentences=trip_sequences,
		vector_size=128,  # Dimensionality of embeddings
		window=3,		 # Context window size
		min_count=1,	  # Minimum frequency of a word to be included
		sg=1,			 # Use skip-gram (sg=1) instead of CBOW (sg=0)
		workers=4		 # Number of threads for training
	)
	w2v.build_vocab(trip_sequences, update=True)
	# w2v.save("w2v.model")

	return w2v

	

def embed_trip(trip_id, model):
	"""
	Embed a list of stops using a Word2Vec model.
	If a stop is not in the vocabulary, fall back to the average embedding.

	Args:
		stops (list): List of stop names (strings).
		model (Word2Vec): Trained Word2Vec model.

	Returns:
		np.ndarray: Embedding of the stop sequence.
	"""
	stop_embeddings = []
	stops = fetch_stops(trip_id)
	durations = 0
	
	if not stops: 
		return np.concatenate([np.zeros(model.vector_size), [0]])
		
	for stop in stops:
		if stop['location'] in model.wv: stop_embeddings.append(model.wv[stop['location']])
		# else: print(f"Stop '{stop}' not in vocabulary, skipping.")
		
		start_time = datetime.strptime(f"{stop['startDate']} {stop['startHour']}:{stop['startMinute']}","%Y-%m-%d %H:%M")
		end_time = datetime.strptime(f"{stop['endDate']} {stop['endHour']}:{stop['endMinute']}","%Y-%m-%d %H:%M")
		
		# print(start_time, end_time, durations)
		# total minutes
		durations += (end_time - start_time).total_seconds() // 60

	avg_durations = durations // len(stops) if stops else 0
	avg_stop_embeddings = np.mean(stop_embeddings, axis=0) if len(stop_embeddings) > 0 else np.zeros(model.vector_size)
	# print(stop_embeddings)

	
	trip_embedding = np.concatenate([
		avg_stop_embeddings,
		[avg_durations],
		# [avg_commute_times]
	])
	
	return trip_embedding
		

# FUNCTION TO USE TO RENEW + ADD ALL TRIP EMBEDDINGS TO THE DB TABLE
def embed_all_trips(model, df=None, use_df=False):
	if use_df:
		user_cluster = df.to_numpy()
		
		for user in user_cluster:
			user_id = user[0]
			cluster_id = user[3]
			trips = fetch_all_trips(user_id)
			if not trips: continue
			
			for trip in trips:
				trip_id = trip['trip_id']
				trip_embedding = embed_trip(trip_id, model)
				# print(user_id, trip_id, cluster_id, trip_embedding)
				# print(user_id, trip_id, cluster_id, sum(trip_embedding))
				add_trip_embedding(user_id, trip_id, cluster_id, trip_embedding.tolist())
			 
	
	else:
		users = return_users()
		user_ids = [u[0] for u in users]

		for user_id in user_ids:
			trips = fetch_all_trips(user_id)
			if not trips: continue
			
			for trip in trips:
				trip_id = trip['trip_id']
				trip_embedding = embed_trip(trip_id, model)
				add_trip_embedding(user_id, trip_id, cluster_id, trip_embedding.tolist())
		

######################################################################################################################
# RECOMMENDATION PART (actual user interaction part) --> use kmeans + scaler to find cluster id + embed + sim search #
######################################################################################################################

# turn user info into format kmeans can understand
def preprocess_user(age, trait, scaler, trait_mapping):
	feature_names = ["age"] + list(trait_mapping.keys())
	trait_encoded = trait_mapping.get(trait, [0, 0, 0, 0, 0, 0, 0, 0, 0, 1])
	train_df = pd.DataFrame([[age] + trait_encoded], columns=feature_names)
	new_array = scaler.transform(train_df)
	return new_array

	# trait_encoded = trait_mapping.get(trait, [0, 0, 0, 0, 0, 0, 0, 0, 0, 1])
	# return np.array([age] + trait_encoded).reshape(1, -1)

# predict cluster given the user info
def predict_cluster(kmeans, scaler, user_age=21, user_trait="Adventurer"):
	trait_mapping = {"Adventurer": [1, 0, 0, 0, 0, 0, 0, 0, 0, 0], "Artist": [0, 1, 0, 0, 0, 0, 0, 0, 0, 0], "Budget": [0, 0, 1, 0, 0, 0, 0, 0, 0, 0], "Family": [0, 0, 0, 1, 0, 0, 0, 0, 0, 0], "Foodie": [0, 0, 0, 0, 1, 0, 0, 0, 0, 0], "Historian": [0, 0, 0, 0, 0, 1, 0, 0, 0, 0], "Luxury": [0, 0, 0, 0, 0, 0, 1, 0, 0, 0], "Nature": [0, 0, 0, 0, 0, 0, 0, 1, 0, 0], "Sightseer": [0, 0, 0, 0, 0, 0, 0, 0, 1, 0], "Solo": [0, 0, 0, 0, 0, 0, 0, 0, 0, 1]}
	
	user_data = preprocess_user(user_age, user_trait, scaler, trait_mapping)
	print(f"USER DATAAAAA {user_data}")
		# convert to format that kmeans can handle
	predicted_cluster = kmeans.predict(user_data)	  
	return int(predicted_cluster[0])
	
# 
def rec_recommend_trip(user_id, trip_id):
	user_info = return_user_info(user_id)
	print("USER INFO!!!!")
	print(user_info)
	user_age = user_info[3] if user_info[3] else 21
	user_trait = user_info[2] if user_info[2] else "Adventurer"
	
	kmeans_path = os.path.join(model_path, "kmeans.pkl")
	scaler_path = os.path.join(model_path, "scaler.pkl")
	w2v_path = os.path.join(model_path, "word2vec.model")
	
	# ensure we have the models trained + serialized to load
	if not os.path.exists(kmeans_path): train_kmeans_scaler()
	if not os.path.exists(w2v_path): train_w2v()

	kmeans = joblib.load(kmeans_path)
	scaler = joblib.load(scaler_path)
	# w2v = joblib.load(w2v_path)
	w2v = Word2Vec.load(w2v_path)
	
	predicted_cluster = predict_cluster(kmeans, scaler, user_age, user_trait)
	trip_embedding = embed_trip(trip_id, w2v).tolist()

	trips = recommend_trip(predicted_cluster, trip_embedding)
	
	return trips if trips else None # [[tid, sim score], [...], [...]]	


"""
def train_w2v():
	trips = return_trips()					  # gets all trips from all users
	trips_seq = preprocess_trip_data(trips)	 # return a list of stop sequences for every trip
	w2v = init_wv(trips_seq)					# trains w2v model for embedding
	
	w2v_path = os.path.join(model_path, "w2v_model.pkl")
	joblib.dump(w2v, w2v_path)
"""
	
	# trip_embedding = embed_trip(10001, w2v)	 # generates trip embedding for a trip
# print(trip_embedding)
# print(len(trip_embedding))

def train_kmeans_scaler():
	scaler, kmeans, df, df_encoded = users_to_df()
	
	kmeans_path = os.path.join(model_path, "kmeans.pkl")
	joblib.dump(kmeans, kmeans_path)
	
	scaler_path = os.path.join(model_path, "scaler.pkl")
	joblib.dump(scaler, scaler_path)
	
def init_models():
	train_w2v()
	train_kmeans_scaler()


# init_models()





'''
# api endpoint
URL = "http://18.216.204.24:8081"
path_users = "all_users"
path_user_trips = "fetch_all_trip"
path_stops = "fetchstops"
path_trips = "all_trips"

def get_all_users():
	r_url = f"{URL}/{path_users}"
	response = requests.get(r_url)
	
	if response.status_code != 200: return f'Users: response error, returned {response.status_code}'
	
	users = response.json()['users']
	# print(users) # 2d array: [[id, name, age, trait], ...]
	return users

def get_all_trips():
	r_url = f"{URL}/{path_trips}"
	response = requests.get(r_url)
	
	if response.status_code != 200: return f'Trips: response error, returned {response.status_code}'
	trips = response.json()['trips']
	return trips
	

def get_trip_from_user(user_id):
	r_url = f"{URL}/{path_user_trips}"
	payload = {"uid": user_id}
	response = requests.get(r_url, payload)

	if response.status_code != 200: return f'User Trips: response error, returned {response.status_code}'

	trips = response.json()['trips'] # [{end_date, start_date, trip_id, trip_name}, ...]
	return trips

def get_stops_from_trip(trip_id):
	r_url = f"{URL}/{path_stops}"
	payload = {"trip_id": trip_id}
	response = requests.get(r_url, payload)
	
	if response.status_code != 200: return f'Stops: response error, returned {response.status_code}'

	stops = response.json()['stops'] # [{description, endDate, endHour, endMinute, startDate, startHour, startMinute, event_id, link, location, title, type}, ...]
	return stops

def preprocess_trip_data(trip_ids):
	for tid in trip_ids:
		stops = get_stops_from_trip(tid)
		
		
	trips_as_sequences = []
	for trip in trip_datasets:
		sequence = [stop["location"] for stop in trip["stops"]]
		trips_as_sequences.append(sequence)
	return trips_as_sequences



def main():
	trips = get_all_trips()
	print(trips[0])
	print(len(trips))
 '''
