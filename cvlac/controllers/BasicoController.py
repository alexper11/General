from cvlac import db
import pandas
from cvlac.models.Basico import Basico

class BasicoController:
    count = 0
    def __init__(self):
        self.__class__.count = self.__class__.count + 1
    
    def insert_df(self, df):
        dicList=df.to_dict(orient='records')
        for dic in dicList:
            basico = Basico(**dic)
            db.session.add(basico)
        #try:
        db.session.commit()
        #except:
        #    db.session.rollback()
        #    print("No se pudo insertar el dataframe en Basico")
        #finally:
        db.session.close()
    