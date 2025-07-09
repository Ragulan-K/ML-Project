import os 
import sys
import numpy as np
import pandas as pd
from src.exception import CustomException
import dill

def save_object(obj, file_path):
    """
    Save an object to a file using pickle.
    """
  
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'wb') as file:
            dill.dump(obj, file)
       
    except Exception as e:
        raise CustomException(e, sys)
        
       