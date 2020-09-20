import pandas as pd
import re
import pickle
import os
import joblib as jb
from scipy.sparse import hstack, csr_matrix
from scipy import sparse
import numpy as np
import json
from settings import MODELOS_DIR

# mdl_rf = pickle.load( open( "random_forest_20200911", "rb" ) )
# mdl_lgbm = pickle.load( open( "lgbm_20200911", "rb" ) )
# title_vec = pickle.load( open( "title_vectorizer_20200911", "rb" ) )


mdl_rf = jb.load(os.path.join(MODELOS_DIR, "random_forest_20200911.pkl.z"))
mdl_lgbm = jb.load(os.path.join(MODELOS_DIR,"lgbm_20200911.pkl.z"))
title_vec = jb.load(os.path.join(MODELOS_DIR, "title_vectorizer_20200911.pkl.z"))

def clean_date(data):
    return pd.to_datetime(data['upload_date'], format="%Y-%m-%d")

def clean_views(data):
    raw_views_str = data['view_count']
    if raw_views_str is None:
        return 0

    return int(raw_views_str)


def compute_features(data):

    publish_date = clean_date(data)
    if publish_date is None:
        return None


    views = clean_views(data)
    title = data['title']

    features = dict()

    features['tempo_desde_pub'] = (pd.Timestamp.today() - publish_date) / np.timedelta64(1, 'D')
    features['views'] = views
    features['views_por_dia'] = features['views'] / features['tempo_desde_pub']
    del features['tempo_desde_pub']

    vectorized_title = title_vec.transform([title])

    num_features = sparse.csr_matrix(np.array([features['views'], features['views_por_dia']]))
    feature_array = sparse.hstack([num_features, vectorized_title])

    return feature_array


def compute_prediction(data):
    feature_array = compute_features(data)

    if feature_array is None:
        return 0

    p_rf = mdl_rf.predict_proba(feature_array)[0][1]
    p_lgbm = mdl_lgbm.predict_proba(feature_array)[0][1]

    p = 0.2*p_rf + 0.8*p_lgbm
    #log_data(data, feature_array, p)

    return p

def log_data(data, feature_array, p):

    #print(data)
    video_id = data.get('og:video:url', '')
    data['prediction'] = p
    data['feature_array'] = feature_array.todense().tolist()
    #print(video_id, json.dumps(data))







