from openai import OpenAI
import pandas as pd
import json
import datetime
import time

#UDF
from Resources.clean_text import clean_text
from Model.ECCOLA import ECCOLA

class suggestion_action:
    def __init__(self, GPT_API_Key, model_id, testingDataSetCSV = None):
        self.ECCOLA = ECCOLA(GPT_API_Key)

        self.trained_model_id = model_id
        self.fine_tune_models = ECCOLA.retrieve_models(self.trained_model_id) 
        
        #ACCURACY TEST
        if (testingDataSetCSV is not None):
            accuracy_success, accuracy_response2 = self.ECCOLA.evaluate_model(self.trained_model_id, testingDataSetCSV) #model_id2, 'TestingDataSet.csv')
            if (accuracy_success):
                print("Accuracy of the model : ", accuracy_response2)
            else:
                print("Failed to check accuracy :", accuracy_response2)
            return accuracy_response2
        else:
            return None
        
    def classify_ECCOLA(self, user_story, max_tokens=150):
        #user_story = 'As a system user, I need guielines to understand the system functionalities. Provide guidelines document'
        _, response = self.ECCOLA.use_model(model_id=self.trained_model_id, user_story=user_story, max_tokens=max_tokens)
        return response
