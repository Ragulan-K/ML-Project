import os
import sys
from dataclasses import dataclass

from catboost import CatBoostRegressor
from sklearn.ensemble import(
    RandomForestRegressor, 
    GradientBoostingRegressor,
    AdaBoostRegressor
)

from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from xgboost import XGBRegressor

from src.exception import CustomException
from src.logger import logging
from src.utils import save_object, evaluate_model

@dataclass
class ModelTrainerConfig:
    trained_model_file_path = os.path.join('artifacts', 'model.pkl')
class ModelTrainer:
    def __init__(self):
        self.model_trainer_config = ModelTrainerConfig()

    def initiate_model_trainer(self, train_array, test_array):
        try:
            logging.info("Splitting training and testing input data")
            X_train, y_train, X_test, y_test = (
                train_array[:,:-1], 
                train_array[:,-1], 
                test_array[:,:-1], 
                test_array[:,-1]
            )

            models = {
                'Random Forest': RandomForestRegressor(),
                'Gradient Boosting': GradientBoostingRegressor(),
                'AdaBoost Regressor': AdaBoostRegressor(),
                'Linear Regression': LinearRegression(),
                'K-Neighbors Regressor': KNeighborsRegressor(),
                'Decision Tree': DecisionTreeRegressor(),
                'CatBoostRegressor': CatBoostRegressor(verbose=False),
                'XGB Regressor': XGBRegressor()
            }

            model_report: dict=evaluate_model(X_train=X_train, X_test=X_test,  y_train=y_train,y_test=y_test,models= models)
            best_model_score = max(model_report.values())

            best_model_name = list(model_report.keys())[list(model_report.values()).index(best_model_score)]
            best_model = models[best_model_name]

            if best_model_score < 0.6:
                raise CustomException("No best model found with sufficient accuracy")
            
            logging.info(f"Best model found: {best_model_name} with score: {best_model_score}")
            save_object(
                obj=best_model,
                file_path=self.model_trainer_config.trained_model_file_path
            )
            predictions = best_model.predict(X_test)
            r2_square = r2_score(y_test, predictions)
            return r2_square



        except Exception as e:
            raise CustomException(e, sys)


