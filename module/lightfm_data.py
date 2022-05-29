import numpy as np
import pandas as pd
import re
from datetime import datetime, timedelta
from lightfm.data import Dataset
from lightfm import LightFM
from lightfm import cross_validation
from lightfm.evaluation import precision_at_k

class LightFMDataPrep:
    def __init__(self):
        pass
    def create_features(self, dataframe, features_name, id_col_name):
        """
        Tao cac future de dua vao lightfm

        Thong so
        ----------
        dataframe: Dataframe
            Pandas Dataframe chua features
        features_name : List
            List of feature columns name avaiable in dataframe
        id_col_name: String
            Column name which contains id of the question or
            answer that the features will map to.
            There are two possible values for this variable.
            1. questions_id_num
            2. professionals_id_num

        Returns
        -------
        Pandas Series
            A pandas series containing process features
            that are ready for feed into lightfm.
            The format of each value
            will be (user_id, ['feature_1', 'feature_2', 'feature_3'])
            Ex. -> (1, ['military', 'army', '5'])
        """

        features = dataframe[features_name].apply(
            lambda x: ','.join(x.map(str)), axis=1)
        features = features.str.split(',')
        features = list(zip(dataframe[id_col_name], features))
        return features



    def generate_feature_list(self, dataframe, features_name):
        """
        Generate features list for mapping 

        Parameters
        ----------
        dataframe: Dataframe
            Pandas Dataframe for Users or Q&A. 
        features_name : List
            List of feature columns name avaiable in dataframe. 

        Returns
        -------
        List of all features for mapping 
        """
        features = dataframe[features_name].apply(
            lambda x: ','.join(x.map(str)), axis=1)
        features = features.str.split(',')
        features = features.apply(pd.Series).stack().reset_index(drop=True)
        return features
    
    def create_data(self, questions, professionals, merge):
        question_feature_list = self.generate_feature_list(
            questions,
            ['questions_tag_name'])

        professional_feature_list = self.generate_feature_list(
            professionals,
            ['professional_all_tags'])
        
        merge['total_weights'] = 1 / (
            merge['num_ans_per_ques'])
        
        # creating features for feeding into lightfm 
        questions['question_features'] = self.create_features(
            questions, ['questions_tag_name'], 
            'questions_id_num')

        professionals['professional_features'] = self.create_features(
            professionals,
            ['professional_all_tags'],
            'professionals_id_num')
        
        return question_feature_list,\
    professional_feature_list,merge,questions,professionals
        
    def fit(self, questions, professionals, merge):
        ########################
        # Dataset building for lightfm
        ########################
        question_feature_list, \
        professional_feature_list,\
        merge,questions,professionals = \
        self.create_data(questions, professionals, merge)
        
        
        # define our dataset variable
        # then we feed unique professionals and questions ids
        # and item and professional feature list
        # this will create lightfm internel mapping
        dataset = Dataset()
        dataset.fit(
            set(professionals['professionals_id_num']), 
            set(questions['questions_id_num']),
            item_features=question_feature_list, 
            user_features=professional_feature_list)


        # now we are building interactions
        # matrix between professionals and quesitons
        # we are passing professional and questions id as a tuple
        # e.g -> pd.Series((pro_id, question_id), (pro_id, questin_id))
        # then we use lightfm build in method for building interactions matrix
        merge['author_question_id_tuple'] = list(zip(
            merge.professionals_id_num,
            merge.questions_id_num,
            merge.total_weights))

        interactions, weights = dataset.build_interactions(
            merge['author_question_id_tuple'])



        # now we are building our questions and
        # professionals features
        # in a way that lightfm understand.
        # we are using lightfm build in method for building
        # questions and professionals features 
        questions_features = dataset.build_item_features(
            questions['question_features'])

        professional_features = dataset.build_user_features(
            professionals['professional_features'])
        
        return interactions,\
    weights,questions_features,professional_features
        
        