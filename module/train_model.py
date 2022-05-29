import numpy as np
import pandas as pd
from lightfm import LightFM
from lightfm import cross_validation
class TrainLightFM:
    def __init__(self):
        pass
        
    def train_test_split(self, interactions, weights):
        train_interactions, test_interactions = \
        cross_validation.random_train_test_split(
            interactions, 
            random_state=np.random.RandomState(2019))
        
        train_weights, test_weights = \
        cross_validation.random_train_test_split(
            weights, 
            random_state=np.random.RandomState(2019))
        return train_interactions,\
    test_interactions, train_weights, test_weights
    
    def fit(self, interactions, weights,
            questions_features, professional_features,
            cross_validation=False,no_components=150,
            learning_rate=0.05,
            loss='warp',
            random_state=2019,
            verbose=True,
            num_threads=4, epochs=5):
        ################################
        # Model building part
        ################################

        # define lightfm model by specifying hyper-parametre
        # then fit the model with ineteractions matrix,
        # item and user features
        
        model = LightFM(
            no_components,
            learning_rate,
            loss=loss,
            random_state=random_state)
        model.fit(
            interactions,
            item_features=questions_features,
            user_features=professional_features, sample_weight=weights,
            epochs=epochs, num_threads=num_threads, verbose=verbose)
        
        return model
