from unittest import TestCase
from inspect import getargspec
from ..build import grid_search
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import pandas as pd
import numpy as np

loan_data = pd.read_csv('data/loan_prediction.csv')
X_bal = loan_data.iloc[:, :-1]
y_bal = loan_data.iloc[:, -1]

X_train, X_test, y_train, y_test = train_test_split(X_bal, y_bal, test_size=0.33, random_state=9)
param_grid = {"max_features": ['sqrt', 4, "log2"],
              "n_estimators": [10, 50, 120],
              "max_depth": [40, 20, 10],
              "max_leaf_nodes": [5, 10, 2]}



class TestGridSearch(TestCase):
    def test_grid_search(self):

        # Input parameters tests
        args = getargspec(grid_search)
        self.assertEqual(len(args[0]), 5, "Expected argument(s) %d, Given %d" % (5, len(args[0])))
        self.assertEqual(args[3], (3,), "Expected default values do not match given default values")

        # Return data types
        rfc = RandomForestClassifier(oob_score=True, random_state=9)
        grid, grid_param, grid_score = grid_search(X_train, y_train, rfc, param_grid, cv=3)

        self.assertIsInstance(grid_param, tuple,
                              "Expected data type for return value is `tuple`, you are returning %s" % (
                                  type(grid_param)))

        self.assertIsInstance(grid_score, np.ndarray,
                              "Expected data type for return value is `numpy.ndarray`, you are returning %s" % (
                                  type(grid_score)))


        # Return value tests
        self.assertEqual(np.shape(grid_param), (81,),
                         "Return value shape does not match expected value")
        self.assertEqual(np.shape(grid_score), (81,),
                         "Return value shape does not match expected value")

        expected_param = [{'max_features': 'sqrt', 'max_leaf_nodes': 5, 'n_estimators': 10, 'max_depth': 40},
                          {'max_features': 'sqrt', 'max_leaf_nodes': 5, 'n_estimators': 50, 'max_depth': 40},
                          {'max_features': 'sqrt', 'max_leaf_nodes': 5, 'n_estimators': 120, 'max_depth': 40},
                          {'max_features': 'sqrt', 'max_leaf_nodes': 10, 'n_estimators': 10, 'max_depth': 40},
                          {'max_features': 'sqrt', 'max_leaf_nodes': 10, 'n_estimators': 50, 'max_depth': 40},
                          {'max_features': 'sqrt', 'max_leaf_nodes': 10, 'n_estimators': 120, 'max_depth': 40},
                          {'max_features': 'sqrt', 'max_leaf_nodes': 2, 'n_estimators': 10, 'max_depth': 40},
                          {'max_features': 'sqrt', 'max_leaf_nodes': 2, 'n_estimators': 50, 'max_depth': 40},
                          {'max_features': 'sqrt', 'max_leaf_nodes': 2, 'n_estimators': 120, 'max_depth': 40},
                          {'max_features': 4, 'max_leaf_nodes': 5, 'n_estimators': 10, 'max_depth': 40},
                          {'max_features': 4, 'max_leaf_nodes': 5, 'n_estimators': 50, 'max_depth': 40},
                          {'max_features': 4, 'max_leaf_nodes': 5, 'n_estimators': 120, 'max_depth': 40},
                          {'max_features': 4, 'max_leaf_nodes': 10, 'n_estimators': 10, 'max_depth': 40},
                          {'max_features': 4, 'max_leaf_nodes': 10, 'n_estimators': 50, 'max_depth': 40},
                          {'max_features': 4, 'max_leaf_nodes': 10, 'n_estimators': 120, 'max_depth': 40},
                          {'max_features': 4, 'max_leaf_nodes': 2, 'n_estimators': 10, 'max_depth': 40},
                          {'max_features': 4, 'max_leaf_nodes': 2, 'n_estimators': 50, 'max_depth': 40},
                          {'max_features': 4, 'max_leaf_nodes': 2, 'n_estimators': 120, 'max_depth': 40},
                          {'max_features': 'log2', 'max_leaf_nodes': 5, 'n_estimators': 10, 'max_depth': 40},
                          {'max_features': 'log2', 'max_leaf_nodes': 5, 'n_estimators': 50, 'max_depth': 40}]

        expected_score = [0.74939173, 0.74209246, 0.756691, 0.75425791, 0.75425791, 0.75912409,
                          0.71289538, 0.71046229, 0.71046229, 0.75912409, 0.76155718, 0.76155718,
                          0.74209246, 0.75912409, 0.756691, 0.76642336, 0.76642336, 0.76642336,
                          0.74939173, 0.74209246]

        for i in range(len(grid_param)):
            if grid_param[i] in expected_param:
                expected_index = expected_param.index(grid_param[i])
                self.assertAlmostEqual(grid_score[i], expected_score[expected_index], 3, "Expected values does not match \
                the given values")
