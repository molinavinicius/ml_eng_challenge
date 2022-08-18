import pandas as pd

from sklearn.pipeline import  Pipeline 
from .transformers import DropEmptyData, FeatureSelector, DateTransformer, NumericalTransformer

def preprocess_precipitaciones(X):
    precipitaciones = DateTransformer().transform(X)
    return precipitaciones

def preprocess_precio_leche(X):
    X.rename(columns = {'Anio': 'year'}, inplace = True)
    DateTransformer(use_dates=['month'], drop_duplicates=False, date_column='Mes', format='%b').transform(X)
    return X.drop(columns=['Mes'])

def preprocess_banco_central(X):
    imacec_ventas_pipe = Pipeline(
        steps=[
            ('selector',  FeatureSelector(lambda x: 'Imacec' in x, feature_names=['Periodo', 'Indice_de_ventas_comercio_real_no_durables_IVCM'])), 
            ('to_hundreds', NumericalTransformer(to_hundreds=True, avoid=['Periodo'], inplace=False))
        ]
    )

    pib_pipe = Pipeline(
        steps=[
            ('selector', FeatureSelector(lambda x: 'PIB' in x, feature_names=['Periodo'])),
            ('to_int', NumericalTransformer(avoid=['Periodo'], inplace=False))
        ]
    )

    droper = DropEmptyData(how='any', axis=0)

    banco_central = DateTransformer(use_dates=['year', 'month'],keep_date_column=True, date_column='Periodo').transform(X)
    dates = FeatureSelector(feature_names=['Periodo', 'year', 'month']).transform(banco_central)
    
    imacec_ventas = imacec_ventas_pipe.transform(banco_central)
    droper.transform(imacec_ventas)
    
    pib = pib_pipe.transform(banco_central)
    droper.transform(pib)

    banco_central = pd.merge(dates, pib, on = 'Periodo', how = 'inner')
    banco_central = pd.merge(banco_central, imacec_ventas, on = 'Periodo', how = 'inner')
    
    banco_central.drop(columns=['Periodo'], inplace=True)
    
    return banco_central

class Preprocessor():
    
    def __init__(self, dataset_names, dataframes):
        self._dataset_names = dataset_names
        self._dataframes = dataframes
        self._preprocessors = {
            'banco_central': preprocess_banco_central,
            'precipitaciones': preprocess_precipitaciones,
            'precio_leche': preprocess_precio_leche
        }
        
    def clean(self):
        cleaned = []
        
        for name in self._dataset_names:
            if not name in self._preprocessors.keys():
                cleaned.append(self._dataframes[name])
                raise NotImplemented("There is no preprocessor for this database")
            cleaned.append(self._preprocessors[name](self._dataframes[name]))
        
        dff = cleaned[0]
        for df in cleaned[1:]:
            dff = pd.merge(dff, df, on = ['month', 'year'], how = 'inner')
        
        return dff.drop(columns=['Precio_leche']), dff['Precio_leche']
