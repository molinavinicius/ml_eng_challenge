from pyexpat import features
import numpy as np 
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
import locale
from typing import List

#Custom Transformer that extracts columns passed as argument to its constructor 
class FeatureSelector( BaseEstimator, TransformerMixin ):

    def __init__( self, condition=None, feature_names:list=None ):
        self._feature_names = feature_names 
        self._condition = condition
    
    #Return self nothing else to do here    
    def fit( self, X, y = None ):
        return self 
    
    def transform( self, X, y = None):
        features = self._feature_names
        if self._condition is not None:
            features += [col for col in list(X.columns) if self._condition(col)]
        return X[features]
    
class DateTransformer( BaseEstimator, TransformerMixin ):

    def __init__(self, use_dates = ['year', 'month'], drop_duplicates=True, keep_date_column=False, date_column = 'date', locale='es_ES.UTF-8', format='%Y-%m-%d', inplace:bool=True):
        self._use_dates = use_dates
        self._locale = locale
        self._format = format
        self._date_column = date_column
        self._keep_column = keep_date_column
        self._in_place = inplace
        self._drop_duplicates = drop_duplicates
    
    #Return self nothing else to do here
    def fit( self, X, y = None  ):
        return self

    #Helper function to extract year from column 'dates' 
    def get_year( self, datetime ):
        return datetime.year
    
    #Helper function to extract month from column 'dates'
    def get_month( self, datetime ):
        return datetime.month

         

    
    def transform(self, X:pd.DataFrame , y = None ):
        # locale.setlocale(locale.LC_TIME)#, self._locale)
        if not self._in_place:
            X = X.copy()
        
        if self._format == '%Y-%m-%d':
            X[f'{self._date_column}'] = X[f'{self._date_column}'].apply(lambda x: x[0:10])
        X[f'{self._date_column}'] = pd.to_datetime(X[f'{self._date_column}'], format = self._format, errors = 'coerce')
        
        #Depending on constructor argument break dates column into specified units
        #using the helper functions written above 
        for spec in self._use_dates:
            exec( f"X.loc[:,'{spec}'] = X['{self._date_column}'].apply(self.get_{spec}).astype('Int64')")
       

        if self._drop_duplicates:
            X.drop_duplicates(subset = self._date_column, inplace = True)
        X.dropna(axis=0, subset=self._date_column, inplace=True)
        
        if not self._keep_column:
            #Drop unusable column 
            X = X.drop(self._date_column, axis = 1 )
        
        return X

class DropEmptyData (BaseEstimator, TransformerMixin):
    def __init__( self, how:str, axis:int, inplace:bool=True ):
        self._how = how
        self._axis = axis
        self._in_place = inplace
    
    #Return self nothing else to do here    
    def fit( self, X, y = None ):
        return self 
    
    def transform( self, X:pd.DataFrame, y = None):
        if not self._in_place:
            X = X.copy()
        
        X.dropna(how = 'any', axis = 0, inplace=True )
        return X

class NumericalTransformer(BaseEstimator, TransformerMixin):
    #Class Constructor
    def __init__( self, columns:list=None, to_hundreds:bool=False, sep:str = '.',avoid:list=[], inplace:bool=True ):
        self._to_hundreds = to_hundreds
        self._sep = sep
        self._columns = columns
        self._avoid = avoid
        self._in_place = inplace
        
    #Return self, nothing else to do here
    def fit( self, X, y = None ):
        return self 
    
    def convert_string_to_int(self, x:str):
        if isinstance(x, str):
            x = x.replace(self._sep, '')
            try:
                x = int(x)
                return x
            except:
                return np.nan
        elif isinstance(x, int) or isinstance(x, float):
            return x
        else:
            return np.nan
    
    def convert_string_to_hundreds(self, x:str):
        if isinstance(x, str):
            x = x.split('.')
            if len(x) == 1:
                try:
                    return int(x)
                except:
                    return np.nan
            if x[0].startswith('1'): #es 100+
                if len(x[0]) >2:
                    return float(x[0] + '.' + x[1])
                else:
                    x = x[0]+x[1]
                    return float(x[0:3] + '.' + x[3:])
            else:
                if len(x[0])>2:
                    return float(x[0][0:2] + '.' + x[0][-1])
                else:
                    x = x[0] + x[1]
                    return float(x[0:2] + '.' + x[2:])
        else:
            return np.nan
            
    def transform(self, X:pd.DataFrame, y = None):
        
        if not self._in_place:
            X = X.copy()
            
        if self._to_hundreds:
            func = self.convert_string_to_hundreds
        else:
            func = self.convert_string_to_int
        
        columns = self._columns or X.columns
        
        for col in columns:
            if not col in self._avoid:
                X[col] = X[col].apply(lambda x: func(x))
                if not self._to_hundreds:
                    X[col] = X[col].astype('Int64')
            
        #Converting any infinity values in the dataset to Nan
        X = X.replace( [ np.inf, -np.inf ], np.nan )
        
        #returns a numpy array
        return X
