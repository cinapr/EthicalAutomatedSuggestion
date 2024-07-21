from openai import OpenAI
import pandas as pd
import json
import datetime
import time

#UDF
from Resources.clean_text import clean_text
from Model.ECCOLA import ECCOLA
from Model.LoggerMessage import LoggerMessage

class training_action(LoggerMessage):
        
    #ECCOLA_Questions_csv = 'ECCOLA_Questions.csv'
    #ECCOLA_QuestionsCorrelations_csv = 'ECCOLA_QuestionsCorrelations.csv'
    #trainingDataSetCSV = 'TrainingSet.csv'
    def __init__(self, GPT_API_Key, model_id=None):
        # Initialize ECCOLA with the provided GPT API key
        self.ECCOLA = ECCOLA(GPT_API_Key)
        self.model_id = model_id



    def get_model(self):
        return self.model_id

    
    def run_ECCOLA_training(self, ECCOLA_Questions_csv, ECCOLA_QuestionsCorrelations_csv, trainingDataSetCSV, log_callback=None):   
        ft_success1 = False
        job_id1 = None
        model_id1 = None
        model_id1_complete = False

        # First Dataset
        if ((job_id1 is None) and (model_id1 is None)): # Check if questions have been trained before proceeding
            # Data preparation for three CSV files
            prep_success11, jsonnl_file1 = self.ECCOLA.data_preparation(csv_data=ECCOLA_Questions_csv, 
                                                                        prompt_template="If the INPUT Paragraph can answer the: {Questions}", 
                                                                        response_template="{ECCOLA_Code}", 
                                                                        columns_to_be_cleaned=['ECCOLA_Code','Questions'], 
                                                                        filemethod='w')
            prep_success12, jsonnl_file1 = self.ECCOLA.data_preparation(csv_data=ECCOLA_QuestionsCorrelations_csv, 
                                                                        prompt_template="If the INPUT Paragraph related to: {Questions_Reasoning}", 
                                                                        response_template="{ECCOLA_Code}", 
                                                                        columns_to_be_cleaned=['ECCOLA_Code','Questions_Reasoning'], 
                                                                        filemethod='a')
            prep_success13, jsonnl_file1 = self.ECCOLA.data_preparation(csv_data=trainingDataSetCSV, 
                                                                        prompt_template="INPUT is = {User_Story} {Acceptance_Criteria}. What previously defined classifications of ECCOLA_Code related to the INPUT?", 
                                                                        response_template="{ECCOLA_Code}", 
                                                                        reason_template="Because, the INPUT ({User_Story} {Acceptance_Criteria}) can answer question:{Related_Questions}, which are classified under {ECCOLA_Code}", 
                                                                        columns_to_be_cleaned=['ECCOLA_Code','User_Story','Acceptance_Criteria', 'Related_Questions'], 
                                                                        filemethod='a')

            # Proceed if data preparation was successful
            if prep_success11 and prep_success12 and prep_success13:
                upload_success1, upload_response1, file_id1 = self.ECCOLA.upload_dataset(jsonnl_file1)
                if upload_success1:
                    ft_success1, ft_response1, job_id1 = self.ECCOLA.fine_tune(file_id1)
                    if ft_success1:
                        self.log("Model1 is currently being fine-tuned under job_id : " + job_id1, log_callback)
                        print("Model1 is currently being fine-tuned under job_id : " + job_id1)
                    else:
                        return False, "Failed to fine-tune first dataset:" + ft_response1
                else:
                    return False, "Failed to upload first dataset:" + upload_response1
            else:
                return False, "Failed to prepare first dataset" + jsonnl_file1

        # Waiting for model1 to finish fine-tuning
        model_id1_complete, model_id1 = self.ECCOLA.wait_for_fine_tuning_completion(job_id1, timeout=3600, interval=10, log_callback=log_callback)

        if not model_id1_complete: # Only proceed if the first model finishes fine-tuning
            return False, "Failed to complete first fine-tuning"
        else:
            # Store the fine-tuned model ID
            storemodel_success, storemodel_response = self.ECCOLA.store_model_id(model_id1)
            if storemodel_success:
                self.model_id = model_id1
                message_success = "Fine-tuning completed successfully, model saved in : " + storemodel_response + ", do not forget to save the model properly, as we never shown it again"
                print(message_success)
                self.log(message_success, log_callback)
                return True, message_success
            else:
                return False, "Failed to save model: " + storemodel_response



    def test_accuracy(self, testingDataSetCSV):
        #accuracy check
        accuracy_success, accuracy_response2 = self.ECCOLA.evaluate_model(self.model_id, testingDataSetCSV) #model_id2, 'TestingDataSet.csv')
        if (accuracy_success):
            print("Accuracy of the model : ", accuracy_response2)
        else:
            print("Failed to check accuracy :", accuracy_response2)
        
        return accuracy_success, accuracy_response2