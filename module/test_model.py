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

# rs_loaded = pickle.load(open("rs.h5","rb"))


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
df_questions_p, df_professionals_p, df_merge_p = \
cv_data_prep.prepare(
    df_professionals,df_students,
    df_questions,df_answers,
    df_tags,df_tag_questions,df_tag_users,
    df_question_scores)
# df_questions_p.to_csv("demo.csv")

# prepare data for lightfm 
interactions, weights, \
questions_features, professional_features = \
light_fm_data_prep.fit(
    df_questions_p, df_professionals_p, df_merge_p)


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
# create file
# create_file_csv(display_csv)
# display(display_csv)