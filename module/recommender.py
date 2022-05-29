class LightFMRecommendations:
    """
    Make prediction given model and professional ids
    """
    def __init__(self, lightfm_model,
                 professionals_features,
                 questions_features,
                 questions,professionals,merge):
        self.model = lightfm_model
        self.professionals_features = professionals_features
        self.questions_features = questions_features
        self.questions = questions
        self.professionals = professionals
        self.merge = merge
        
    def previous_answered_questions(self, professionals_id):
        previous_q_id_num = (
            self.merge.loc[\
                self.merge['professionals_id_num'] == \
                professionals_id]['questions_id_num'])
        
        previous_answered_questions = self.questions.loc[\
            self.questions['questions_id_num'].isin(
            previous_q_id_num)]
        return previous_answered_questions
        
    
    def _filter_question_by_pro(self, professionals_id):
        """Drop questions that professional already answer"""
        previous_answered_questions = \
        self.previous_answered_questions(professionals_id)
        
        discard_qu_id = \
        previous_answered_questions['questions_id_num'].values.tolist()
        
        questions_for_prediction = \
        self.questions.loc[~self.questions['questions_id_num'].isin(discard_qu_id)]
        
        return questions_for_prediction
    
    def _filter_question_by_date(self, questions, start_date, end_date):
        mask = \
        (questions['questions_date_added'] > start_date) & \
        (questions['questions_date_added'] <= end_date)
        
        return questions.loc[mask]
        
    
    def recommend_by_pro_id_general(self,
                                    professional_id,
                                    num_prediction=8):
        questions_for_prediction = self._filter_question_by_pro(professional_id)
        score = self.model.predict(
            professional_id,
            questions_for_prediction['questions_id_num'].values.tolist(), 
            item_features=self.questions_features,
            user_features=self.professionals_features)
        
        questions_for_prediction['recommendation_score'] = score
        questions_for_prediction = questions_for_prediction.sort_values(
            by='recommendation_score', ascending=False)[:num_prediction]
        return questions_for_prediction
    
    def recommend_by_pro_id_frequency_date_range(self,
                                                 professional_id,
                                                 start_date,
                                                 end_date,
                                                 num_prediction=8):
        questions_for_prediction = \
        self._filter_question_by_pro(professional_id)
        
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
        
        questions_for_prediction = self._filter_question_by_date(
            questions_for_prediction, start_date, end_date)
        
        score = self.model.predict(
            professional_id,
            questions_for_prediction['questions_id_num'].values.tolist(), 
            item_features=self.questions_features,
            user_features=self.professionals_features)
        
        questions_for_prediction['recommendation_score'] = score
        questions_for_prediction = questions_for_prediction.sort_values(
            by='recommendation_score', ascending=False)[:num_prediction]
        return questions_for_prediction
