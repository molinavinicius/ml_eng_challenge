from pydantic import BaseModel

class Precipitaciones(BaseModel):
    Coquimbo:  float
    Valparaiso: float
    Metropolitana_de_Santiago: float
    Libertador_Gral__Bernardo_O_Higgins: float
    Maule: float
    Biobio: float
    La_Araucania: float
    Los_Rios: float    


class PIB(BaseModel):
    PIB_Agropecuario_silvicola: int
    PIB_Pesca: int
    PIB_Mineria: int
    PIB_Mineria_del_cobre: int
    PIB_Otras_actividades_mineras: int
    PIB_Industria_Manufacturera: int
    PIB_Alimentos: int
    PIB_Bebidas_y_tabaco: int
    PIB_Textil: int
    PIB_Maderas_y_muebles: int
    PIB_Celulosa: int
    PIB_Refinacion_de_petroleo: int
    PIB_Quimica: int
    PIB_Minerales_no_metalicos_y_metalica_basica: int
    PIB_Productos_metalicos: int
    PIB_Electricidad: int
    PIB_Construccion: int
    PIB_Comercio: int
    PIB_Restaurantes_y_hoteles: int
    PIB_Transporte: int
    PIB_Comunicaciones: int
    PIB_Servicios_financieros: int
    PIB_Servicios_empresariales: int
    PIB_Servicios_de_vivienda: int
    PIB_Servicios_personales: int
    PIB_Administracion_publica: int
    PIB_a_costo_de_factores: int
    PIB: int
    
class Imacec(BaseModel):
    Imacec_empalmado: float
    Imacec_produccion_de_bienes: float
    Imacec_minero: float
    Imacec_industria: float
    Imacec_resto_de_bienes: float
    Imacec_comercio: float
    Imacec_servicios: float
    Imacec_a_costo_de_factores: float
    Imacec_no_minero: float

class Ventas(BaseModel):
    Indice_de_ventas_comercio_real_no_durables_IVCM: float