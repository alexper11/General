from cvlac.db_cvlac import Base
from sqlalchemy import Column, Integer, String

class Investigacion(Base):
    
    __tablename__ = 'investigacion'
    id = Column(Integer, primary_key=True)
    idcvlac = Column(String(20), nullable=False)
    nombre = Column(String(1000), nullable=False)
    activa = Column(String(50), nullable=False)
    
    def __init__(self, **kwargs):
        
        for key, value in kwargs.items():
            setattr(self, key, value)
            
    def __repr__(self):
        return f'Investigacion({self.nombre}, {self.idcvlac}, {self.activa})'
    
    def __str__(self):
        return self.idcvlac