from cvlac import db_cvlac
import pandas
from cvlac.cvlac_models.EmpresaTecnologica import EmpresaTecnologica

class EmpresaTecnologicaController:
    count = 0
    def __init__(self):
        self.__class__.count = self.__class__.count + 1
    
    def insert_df(self, df):
        dicList=df.to_dict(orient='records')
        db_cvlac.session.bulk_insert_mappings(EmpresaTecnologica, dicList)
        try:
            db_cvlac.session.commit()
        except:
            db_cvlac.session.rollback()
            print("No se pudo insertar el dataframe en EmpresaTecnologica")
            df.to_csv('EmpresaTecnologicaCvlac.csv')
        finally:
            db_cvlac.session.close()
    
    def delete_idcvlac(self, idcvlac):
        db_cvlac.session.query(EmpresaTecnologica).filter(EmpresaTecnologica.idcvlac==idcvlac).delete(synchronize_session=False)
        try:
            db_cvlac.session.commit()
        except:
            db_cvlac.session.rollback()
            print("No se pudo eliminar el idcvlac: "+idcvlac+" en EmpresaTecnologica")
        finally:
            db_cvlac.session.close()
    