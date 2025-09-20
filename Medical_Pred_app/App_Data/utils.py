import pickle
import json
import numpy as np
import App_Data.config as config


class MedicalData():

    def __init__(self,age : int,gender: str,bmi: float,children: int,smoker: str,region: str):

        self.age = age
        self.gender = gender.lower()
        self.bmi = bmi
        self.children = children
        self.smoker = smoker.lower()
        self.region = 'region_' + region.lower()

    def load_model(self):

        try:

            with open(config.MODEL_FILE_PATH,'rb') as f:
                self.model = pickle.load(f)

            with open(config.JSON_FILE_PATH,'r') as f:
                self.json_data = json.load(f)
        
        except FileNotFoundError as e:
            raise FileNotFoundError(f"Model or data file not found: {str(e)}")
        except Exception as e:
            raise Exception(f"Error loading model or data: {str(e)}")
        
    def _validate_inputs(self):
        if self.age < 0 or self.age > 100:
            raise ValueError("Age must be between 0 to 100")
        if self.bmi < 10 or self.bmi > 50:
            raise ValueError("BMI must be between 10 to 50")
        if self.gender not in  ('male','female'):
            raise ValueError("Enter the valid gender")
        if self.children < 0  or self.children>10:
            raise ValueError("Children must be between 0 to 10")
        if self.smoker not in ('yes','no'):
            raise ValueError("Enter the valid smoker data")

    def get_predict(self):

        try:

            self.load_model()
            self._validate_inputs()

            column_names =  self.model.feature_names_in_

            region_index = np.where(column_names == self.region)[0]

            test_array = np.zeros((1,len(column_names)))

            test_array[0][0] = self.age
            test_array[0][1] = self.json_data['gender'][self.gender]
            test_array[0][2] = self.bmi
            test_array[0][3] = self.children
            test_array[0][4]= self.json_data['smoker'][self.smoker]
            test_array[0, region_index] = 1


            prediction = self.model.predict(test_array)

            return prediction
        
        except AttributeError as e:
            raise AttributeError(f"Model is not loaded properly: {str(e)}")
         





