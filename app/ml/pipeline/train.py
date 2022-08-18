import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.preprocessing import StandardScaler, PolynomialFeatures
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
from sklearn.feature_selection import SelectKBest, mutual_info_regression

def model_evaluation(y, y_hat):
    return {
        'rmse': mean_squared_error(y, y_hat),
        'r2': r2_score(y, y_hat),
        'rmae': mean_absolute_error(y, y_hat),
    }
    
def model_training(X, y):
    # generate random data-set
    np.random.seed(0)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    pipe = Pipeline([('scale', StandardScaler()),
                    ('selector', SelectKBest(mutual_info_regression)),
                    ('poly', PolynomialFeatures()),
                    ('model', Ridge())])
    k=[3, 4, 5, 6, 7, 10]
    alpha=[1, 0.5, 0.2, 0.1, 0.05, 0.02, 0.01]
    poly = [1, 2, 3, 5, 7]
    grid = GridSearchCV(estimator = pipe,
                        param_grid = dict(selector__k=k,
                                        poly__degree=poly,
                                        model__alpha=alpha),
                        cv = 3,
                    scoring = 'r2')
    model = grid.fit(X_train, y_train)
    y_predicted = grid.predict(X_test)

    return {
        'model': model,
        'metrics': model_evaluation(y_test, y_predicted)
    }