import numpy as np
import pandas as pd

# lightfm imports 
from lightfm.data import Dataset
from lightfm import LightFM
from lightfm import cross_validation
from lightfm.evaluation import precision_at_k
from lightfm.evaluation import auc_score

import re
from datetime import datetime, timedelta

import warnings
warnings.filterwarnings('ignore')
import pickle

import chuan_bi_data
# object = module.GFG() GFG is class
# from module import method
import lightfm_data
import train_model
import recommender
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


############################################
# Doc du lieu va luu vao dataframe
############################################
base_path = '../data/'
df_answer_scores = pd.read_csv(
    base_path + 'answer_scores.csv')

df_answers = pd.read_csv(
    base_path + 'answers.csv',
    parse_dates=['answers_date_added'])

df_comments = pd.read_csv(
    base_path + 'comments.csv')

df_emails = pd.read_csv(
    base_path + 'emails.csv')

df_group_memberships = pd.read_csv(
    base_path + 'group_memberships.csv')

df_groups = pd.read_csv(
    base_path + 'groups.csv')

df_matches = pd.read_csv(
    base_path + 'matches.csv')

df_professionals = pd.read_csv(
    base_path + 'professionals.csv',
    parse_dates=['professionals_date_joined'])

df_question_scores = pd.read_csv(
    base_path + 'question_scores.csv')

df_questions = pd.read_csv(
    base_path + 'questions.csv',
    parse_dates=['questions_date_added'])

df_school_memberships = pd.read_csv(
    base_path + 'school_memberships.csv')

df_students = pd.read_csv(
    base_path + 'students.csv',
    parse_dates=['students_date_joined'])

df_tag_questions = pd.read_csv(
    base_path + 'tag_questions.csv')

df_tag_users = pd.read_csv(
    base_path + 'tag_users.csv')

df_tags = pd.read_csv(
    base_path + 'tags.csv')


# Khoi tao cac class
cv_data_prep = chuan_bi_data.DataPreparation()
light_fm_data_prep = lightfm_data.LightFMDataPrep()
train_lightfm = train_model.TrainLightFM()

# process raw data
def pro_data():
    df_questions_p, df_professionals_p, df_merge_p = \
    cv_data_prep.prepare(
        df_professionals,df_students,
        df_questions,df_answers,
        df_tags,df_tag_questions,df_tag_users,
        df_question_scores)
    if os.path.exists("df_questions_p.csv"):
        os.remove("df_questions_p.csv")
    else:
        display_csv.to_csv("df_questions_p.csv") 

    if os.path.exists("df_professionals_p.csv"):
        os.remove("df_professionals_p.csv")
    else:
        display_csv.to_csv("df_professionals_p.csv") 

    if os.path.exists("df_merge_p.csv"):
        os.remove("df_merge_p.csv")
    else:
        display_csv.to_csv("df_merge_p.csv")   

df_questions_p = pd.read_csv('df_questions_p.csv')
df_professionals_p = pd.read_csv('df_professionals_p.csv')
df_merge_p = pd.read_csv('df_merge_p.csv')

# prepare data for lightfm 
def pre_data():
    interactions, weights, \
    questions_features, professional_features = \
    light_fm_data_prep.fit(
        df_questions_p, df_professionals_p, df_merge_p)

    if os.path.exists("interactions.pkl"):
        os.remove("interactions.pkl")
    else:
        with open('interactions.pkl','wb') as file:
            pickle.dump(interactions,file)

    if os.path.exists("weights.pkl"):
        os.remove("weights.pkl")
    else:
        with open('weights.pkl','wb') as file:
            pickle.dump(weights,file)

    if os.path.exists("questions_features.pkl"):
        os.remove("questions_features.pkl")
    else:
        with open('questions_features.pkl','wb') as file:
            pickle.dump(questions_features,file)

    if os.path.exists("professional_features.pkl"):
        os.remove("professional_features.pkl")
    else:
        with open('professional_features.pkl','wb') as file:
            pickle.dump(professional_features,file)

# pre_data()

questions_features = pickle.load(open("questions_features.pkl","rb"))
professional_features = pickle.load(open("professional_features.pkl","rb"))

# finally build and trian our model
# model = train_lightfm.fit(interactions,
#                           weights,
#                           questions_features,
#                           professional_features)

model = pickle.load(open("rs.h5","rb"))


# define our recommender class
lightfm_recommendations = recommender.LightFMRecommendations(
    model,
    professional_features,questions_features,
    df_questions_p, df_professionals_p, df_merge_p)

# let's what our model predict for user id 3
print("Recommendation for professional: " + str(3))
from IPython.display import display
display_csv = lightfm_recommendations.recommend_by_pro_id_general(3)[:8]
if os.path.exists("display_csv.csv"):
    os.remove("display_csv.csv")
else:
    display_csv.to_csv("display_csv.csv")    

def recommend_by_pro_id_date_rage(professional_id,start_date,end_date,num_prediction):
    rc_by_day = lightfm_recommendations.recommend_by_pro_id_frequency_date_range(professional_id,start_date,end_date,num_prediction)
    
# create file
# create_file_csv(display_csv)
# display(display_csv)