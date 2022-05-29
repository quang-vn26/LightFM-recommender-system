import numpy as np
import pandas as pd
import re
from datetime import datetime, timedelta

class DataPreparation:
    def __init__(self):
        pass
    def _assign_unique_id(self, data, id_col_name):
        new_dataframe=data.assign(
            int_id_col_name=np.arange(len(data))
            ).reset_index(drop=True)
        return new_dataframe.rename(columns={'int_id_col_name': id_col_name})

    def _dropna(self, data, column, axis):
        return data.dropna(column, axis=axis)

    def _merge_data(self, left_data, left_key, right_data, right_key, how):
        return left_data.merge(
            right_data,
            how=how,
            left_on=left_key,
            right_on=right_key)

    def _group_tags(self, data, group_by, tag_column):
        return data.groupby(
            [group_by])[tag_column].apply(
            ','.join).reset_index()

    def _merge_cv_datasets(
        self,
        professionals,students,
        questions,answers,
        tags,tag_questions,tag_users, questions_score):
        
      
        tag_question = self._merge_data(
            left_data=tag_questions,
            left_key='tag_questions_tag_id',
            right_data=tags,
            right_key='tags_tag_id',
            how='inner')
        tag_question = self._group_tags(
            data=tag_question,
            group_by='tag_questions_question_id',
            tag_column='tags_tag_name')
        
        tag_question = tag_question.rename(
            columns={'tags_tag_name': 'questions_tag_name'})
        
        tags_pro = self._merge_data(
            left_data=tag_users,
            left_key='tag_users_tag_id',
            right_data=tags,
            right_key='tags_tag_id',
            how='inner')
        tags_pro = self._group_tags(
            data=tags_pro,
            group_by='tag_users_user_id',
            tag_column='tags_tag_name')
        tags_pro = tags_pro.rename(
            columns={'tags_tag_name': 'professionals_tag_name'})
        
        questions = self._merge_data(
            left_data=questions,
            left_key='questions_id',
            right_data=tag_question,
            right_key='tag_questions_question_id',
            how='left')
        professionals = self._merge_data(
            left_data=professionals,
            left_key='professionals_id',
            right_data=tags_pro,
            right_key='tag_users_user_id',
            how='left')
        
        questions = self._merge_data(
            left_data=questions,
            left_key='questions_id',
            right_data=questions_score,
            right_key='id',
            how='left')
        
        questions = self._merge_data(
            left_data=questions,
            left_key='questions_author_id',
            right_data=students,
            right_key='students_id',
            how='left')
        
        merge = self._merge_data(
            left_data=answers,
            left_key='answers_question_id',
            right_data=questions,
            right_key='questions_id',
            how='inner')
        
        merge = self._merge_data(
            left_data=merge,
            left_key='answers_author_id',
            right_data=professionals,
            right_key='professionals_id',
            how='inner')
        
        return questions, professionals, merge
  
    def _drop_duplicates_tags(self, data, col_name):
        return (
            data[col_name].str.split(
                ',').apply(set).str.join(','))


    def _merge_pro_pre_ans_tags(self, professionals, merge):
        professionals_prev_ans_tags = (
            merge[['professionals_id', 'questions_tag_name']])
        professionals_prev_ans_tags = professionals_prev_ans_tags.dropna()
        
        professionals_prev_ans_tags = self._group_tags(
            data=professionals_prev_ans_tags,
            group_by='professionals_id',
            tag_column='questions_tag_name')
        
        professionals_prev_ans_tags['questions_tag_name'] = \
        self._drop_duplicates_tags(
            professionals_prev_ans_tags, 'questions_tag_name')
        
        professionals = self._merge_data(
            left_data=professionals,
            left_key='professionals_id',
            right_data=professionals_prev_ans_tags,
            right_key='professionals_id',
            how='left')
        
        professionals['professional_all_tags'] = (
            professionals[['professionals_tag_name',
                           'questions_tag_name']].apply(
                lambda x: ','.join(x.dropna()),
                axis=1))
        return professionals

    def prepare(
        self,
        professionals,students,
        questions,answers,
        tags,tag_questions,tag_users, questions_score):
        
        professionals = self._assign_unique_id(
            professionals, 'professionals_id_num')
        students = self._assign_unique_id(
            students, 'students_id_num')
        questions = self._assign_unique_id(
            questions, 'questions_id_num')
        answers = self._assign_unique_id(
            answers, 'answers_id_num')
        
        tags = tags.dropna()
        tags['tags_tag_name'] = tags['tags_tag_name'].str.replace(
            '#', '')
        
        
        df_questions, df_professionals, df_merge = self._merge_cv_datasets(
            professionals,students,
            questions,answers,
            tags,tag_questions,tag_users,
            questions_score)
        
   
        df_merge['num_ans_per_ques'] = df_merge.groupby(
            ['questions_id'])['answers_id'].transform('count')
        
        df_professionals = self._merge_pro_pre_ans_tags(
            df_professionals, df_merge)
        
        df_questions['score'] = df_questions['score'].fillna(0)
        df_questions['score'] = df_questions['score'].astype(int)
        df_questions['questions_tag_name'] = \
        df_questions['questions_tag_name'].fillna('No Tag')
        
        
        df_questions['questions_tag_name'] = \
        df_questions['questions_tag_name'].str.split(
            ',').apply(set).str.join(',')


        df_professionals['professional_all_tags'] = \
        df_professionals['professional_all_tags'].fillna(
            'No Tag')
        df_professionals['professional_all_tags'] = \
        df_professionals['professional_all_tags'].replace(
            '', 'No Tag')
        
        df_professionals['professionals_location'] = \
        df_professionals['professionals_location'].fillna(
            'No Location')
        
        df_professionals['professionals_industry'] = \
        df_professionals['professionals_industry'].fillna(
            'No Industry')

        df_professionals['professional_all_tags'] = \
        df_professionals['professional_all_tags'].str.split(
            ',').apply(set).str.join(',')

        df_merge['num_ans_per_ques']  = \
        df_merge['num_ans_per_ques'].fillna(0)
        
        return df_questions, df_professionals, df_merge
