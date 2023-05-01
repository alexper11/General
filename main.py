from cvlac.ExtractorCvlac import ExtractorCvlac
from cvlac.ExtractorGruplac import ExtractorGruplac
from cvlac.util import get_lxml
from scopus.ExtractorScopus import ExtractorScopus
from scopus.Scientopy import Scientopy
from scopus.readKey import read_key
from scopus.integracion import integrar

import pandas as pd
import numpy as np
import os
import sys

from cvlac.cvlac_models.DBmodel import create_cvlac_db
from cvlac.cvlac_controllers.ActuacionController import ActuacionController
from cvlac.cvlac_controllers.ArticulosController import ArticulosController
from cvlac.cvlac_controllers.BasicoController import BasicoController
from cvlac.cvlac_controllers.EvaluadorController import EvaluadorController
from cvlac.cvlac_controllers.IdentificadoresController import IdentificadoresController
from cvlac.cvlac_controllers.IdiomaController import IdiomaController
from cvlac.cvlac_controllers.InvestigacionController import InvestigacionController
from cvlac.cvlac_controllers.JuradosController import JuradosController
from cvlac.cvlac_controllers.LibrosController import LibrosController
from cvlac.cvlac_controllers.ReconocimientoController import ReconocimientoController
from cvlac.cvlac_controllers.RedesController import RedesController
from cvlac.cvlac_controllers.EstanciasController import EstanciasController
from cvlac.cvlac_controllers.AcademicaController import AcademicaController
from cvlac.cvlac_controllers.ComplementariaController import ComplementariaController
from cvlac.cvlac_controllers.EmpresaTecnologicaController import EmpresaTecnologicaController
from cvlac.cvlac_controllers.InnovacionEmpresarialController import InnovacionEmpresarialController
from cvlac.cvlac_controllers.CaplibrosController import CaplibrosController
from cvlac.cvlac_controllers.PrototipoController import PrototipoController
from cvlac.cvlac_controllers.SoftwareController import SoftwareController
from cvlac.cvlac_controllers.TecnologicosController import TecnologicosController
from cvlac.cvlac_controllers.MetaCvlacDBController import MetaCvlacDBController


from cvlac.gruplac_models.DBmodel import create_gruplac_db
from cvlac.gruplac_controllers.ArticulosGController import ArticulosGController
from cvlac.gruplac_controllers.BasicoGController import BasicoGController
from cvlac.gruplac_controllers.CaplibrosGController import CaplibrosGController
from cvlac.gruplac_controllers.CursoDoctoradoController import CursoDoctoradoController
from cvlac.gruplac_controllers.CursoMaestriaController import CursoMaestriaController
from cvlac.gruplac_controllers.DisenoIndustrialGController import DisenoIndustrialGController
from cvlac.gruplac_controllers.EmpresaTecnologicaGController import EmpresaTecnologicaGController
from cvlac.gruplac_controllers.InnovacionEmpresarialGController import InnovacionEmpresarialGController
from cvlac.gruplac_controllers.InstitucionesController import InstitucionesController
from cvlac.gruplac_controllers.IntegrantesController import IntegrantesController
from cvlac.gruplac_controllers.LibrosGController import LibrosGController
from cvlac.gruplac_controllers.LineasGController import LineasGController
from cvlac.gruplac_controllers.OtroProgramaController import OtroProgramaController
from cvlac.gruplac_controllers.OtrosArticulosController import OtrosArticulosController
from cvlac.gruplac_controllers.OtrosLibrosController import OtrosLibrosController
from cvlac.gruplac_controllers.OtrosTecnologicosController import OtrosTecnologicosController
from cvlac.gruplac_controllers.PlantaPilotoGController import PlantaPilotoGController
from cvlac.gruplac_controllers.ProgramaDoctoradoController import ProgramaDoctoradoController
from cvlac.gruplac_controllers.ProgramaMaestriaController import ProgramaMaestriaController
from cvlac.gruplac_controllers.PrototiposGController import PrototiposGController
from cvlac.gruplac_controllers.SoftwareGController import SoftwareGController
from cvlac.gruplac_controllers.MetaGruplacDBController import MetaGruplacDBController

from scopus.models.DBmodel import create_scopus_db
from scopus.controllers.AutoresController import AutoresController
from scopus.controllers.ProductosController import ProductosController  
from scopus.controllers.MetaDBScoController import MetaDBScoController                  


if __name__ == '__main__':
    
    sys.path.append(".")
    create_cvlac_db()
    create_gruplac_db()
    create_scopus_db()
    print('Bases de datos creadas')
    
    ########################
    #MODULO CVLAC
    ########################
    
    Extractor=ExtractorGruplac()
    #para este caso el parametro de entrada es la url del buscador scienti para el departamento del Cauca
    lista_gruplac=Extractor.get_gruplac_list('https://scienti.minciencias.gov.co/ciencia-war/busquedaGrupoXDepartamentoGrupo.do?codInst=&sglPais=COL&sgDepartamento=CA&maxRows=15&grupos_tr_=true&grupos_p_=1&grupos_mr_=130')
    
    ######################
    #Extraccion de tablas CVLAC
    ######################
    
    print('setting grup attributes...')
    Extractor.set_grup_attrs(lista_gruplac)
    
    print('updating cvlacdb...')
    
    basico=BasicoController()
    basico.insert_df(Extractor.grup_basico.drop_duplicates(ignore_index=True))
    del basico
    
    articulos=ArticulosController()
    articulos.insert_df(Extractor.grup_articulos.drop_duplicates(ignore_index=True))
    del articulos
    
    actuacion = ActuacionController()
    actuacion.insert_df(Extractor.grup_actuacion.drop_duplicates(ignore_index=True))
    del actuacion
    
    evaluador=EvaluadorController()
    evaluador.insert_df(Extractor.grup_evaluador.drop_duplicates(ignore_index=True))
    del evaluador
    
    identificadores=IdentificadoresController()
    aux_identificadores=Extractor.grup_identificadores.drop_duplicates(ignore_index=True)
    aux_identificadores.to_csv('aux_identificadores.csv',index=False)
    identificadores.insert_df(aux_identificadores)
    del identificadores
    
    idioma=IdiomaController()
    idioma.insert_df(Extractor.grup_idioma.drop_duplicates(ignore_index=True))
    del idioma
    
    investigacion=InvestigacionController()
    investigacion.insert_df(Extractor.grup_investiga.drop_duplicates(ignore_index=True))
    del investigacion
    
    jurados=JuradosController()
    jurados.insert_df(Extractor.grup_jurado.drop_duplicates(ignore_index=True))
    del jurados
    
    libros=LibrosController()
    libros.insert_df(Extractor.grup_libros.drop_duplicates(ignore_index=True))
    del libros
    
    reconocimiento=ReconocimientoController()
    reconocimiento.insert_df(Extractor.grup_reconocimiento.drop_duplicates(ignore_index=True))
    del reconocimiento
    
    redes=RedesController()
    redes.insert_df(Extractor.grup_redes.drop_duplicates(ignore_index=True))
    del redes
    
    estancias=EstanciasController()
    estancias.insert_df(Extractor.grup_estancias.drop_duplicates(ignore_index=True))
    del estancias
    
    academica=AcademicaController()
    academica.insert_df(Extractor.grup_academica.drop_duplicates(ignore_index=True))
    del academica
    
    complementaria=ComplementariaController()
    complementaria.insert_df(Extractor.grup_complementaria.drop_duplicates(ignore_index=True))
    del complementaria
    
    caplibros=CaplibrosController()
    caplibros.insert_df(Extractor.grup_caplibros.drop_duplicates(ignore_index=True))
    del caplibros
    
    empresatec=EmpresaTecnologicaController()
    empresatec.insert_df(Extractor.grup_empresa_tecnologica.drop_duplicates(ignore_index=True))
    del empresatec
    
    innovaempresa=InnovacionEmpresarialController()
    innovaempresa.insert_df(Extractor.grup_innovacion_empresarial.drop_duplicates(ignore_index=True))
    del innovaempresa
    
    prototipo=PrototipoController()
    prototipo.insert_df(Extractor.grup_prototipo.drop_duplicates(ignore_index=True))
    del prototipo
    
    software=SoftwareController()
    software.insert_df(Extractor.grup_software.drop_duplicates(ignore_index=True))
    del software
    
    tecnologicos=TecnologicosController()
    tecnologicos.insert_df(Extractor.grup_tecnologicos.drop_duplicates(ignore_index=True))
    del tecnologicos
    
    print('Extracción Cvlac Finalizada')
    
    ######################
    #Extraccion de tablas GRUPLAC
    ######################
    
    print('setting perfil attributes')
    Extractor.set_perfil_attrs(lista_gruplac)
    
    print('updating gruplacdb...')
    
    basicog=BasicoGController()
    aux_basicog=Extractor.perfil_basico
    aux_basicog.to_csv('aux_basicog.csv',index=False)
    basicog.insert_df(aux_basicog)
    del basicog
    
    articulosg=ArticulosGController()
    aux_articulosg=Extractor.perfil_articulos
    aux_articulosg.to_csv('aux_articulosg.csv',index=False)
    articulosg.insert_df(aux_articulosg)
    del articulosg
    
    instituciones=InstitucionesController()
    instituciones.insert_df(Extractor.perfil_instituciones)
    del instituciones
    
    lineasg=LineasGController()
    lineasg.insert_df(Extractor.perfil_lineas)
    del lineasg
    
    integrantes=IntegrantesController()
    aux_integrantes=Extractor.perfil_integrantes
    aux_integrantes.to_csv('aux_integrantes.csv',index=False)
    integrantes.insert_df(aux_integrantes)
    del integrantes
    
    pdoctorado=ProgramaDoctoradoController()
    pdoctorado.insert_df(Extractor.perfil_programa_doctorado)
    del pdoctorado
    
    pmaestria=ProgramaMaestriaController()
    pmaestria.insert_df(Extractor.perfil_programa_maestria)
    del pmaestria
    
    oprograma=OtroProgramaController()
    oprograma.insert_df(Extractor.perfil_otro_programa)
    del oprograma
    
    cdoctorado=CursoDoctoradoController()
    cdoctorado.insert_df(Extractor.perfil_curso_doctorado)
    del cdoctorado
    
    cmaestria=CursoMaestriaController()
    cmaestria.insert_df(Extractor.perfil_curso_maestria)
    del cmaestria
    
    librosg=LibrosGController()
    aux_librosg=Extractor.perfil_libros
    aux_librosg.to_csv('aux_librosg.csv',index=False)
    librosg.insert_df(aux_librosg)
    del librosg
    
    caplibrosg=CaplibrosGController()
    aux_caplibrosg=Extractor.perfil_caplibros
    aux_caplibrosg.to_csv('aux_caplibrosg.csv',index=False)
    caplibrosg.insert_df(aux_caplibrosg)
    del caplibrosg
    
    oarticulos=OtrosArticulosController()
    aux_oarticulos=Extractor.perfil_otros_articulos
    aux_oarticulos.to_csv('aux_oarticulos.csv',index=False)
    oarticulos.insert_df(aux_oarticulos)
    del oarticulos
    
    olibros=OtrosLibrosController()
    aux_olibros=Extractor.perfil_otros_libros
    aux_olibros.to_csv('aux_olibros.csv',index=False)
    olibros.insert_df(aux_olibros)
    del olibros
    
    disenoind=DisenoIndustrialGController()
    disenoind.insert_df(Extractor.perfil_diseno_industrial)
    del disenoind
    
    otecnologicos=OtrosTecnologicosController()
    otecnologicos.insert_df(Extractor.perfil_otros_tecnologicos)
    del otecnologicos
    
    prototiposg=PrototiposGController()
    prototiposg.insert_df(Extractor.perfil_prototipos)
    del prototiposg
    
    softwareg=SoftwareGController()
    softwareg.insert_df(Extractor.perfil_software)
    del softwareg
    
    empresatecg=EmpresaTecnologicaGController()
    empresatecg.insert_df(Extractor.perfil_empresa_tecnologica)
    del empresatecg
    
    innovaempresag=InnovacionEmpresarialGController()
    innovaempresag.insert_df(Extractor.perfil_innovacion_empresarial)
    del innovaempresag
    
    plantapilotog=PlantaPilotoGController()
    plantapilotog.insert_df(Extractor.perfil_planta_piloto)
    del plantapilotog
    
    print('Extracción Gruplac Finalizada')
    
    del Extractor
    
    ########################
    #SCOPUS
    ########################
    API_KEY=""
    INST_TOKEN=""
    API_KEY, INST_TOKEN = read_key()
    
    #Obtener lista de auid Unicauca
    #Obtener autores Unicauca
    
    ExtractorS = ExtractorScopus(API_KEY,INST_TOKEN)
    authors_set=set()
    
    #La siguiente lista de id de afiliciones se obtuvo tras un proceso de selección y filtrado de datos desde la
    #base de datos de scopus para recopilar las afiliciones de los municipios y la capital del Cauca.
    cauca_affiliations=['60051434','113372863','117688708','117795037','126338541','128447346','128268840',
                  '127081273','126489416','128778365','128309743','128482659','117008946','126682182',
                  '128105349','126290034','126174357','112818394','125811395',
                  '127752672','127622090','127564855','127405489','127405461','127381524','115900332',
                  '126777846','126186631','126173286','60108709','101775869','119181814','128840430',
                  '114698614','116513678','117723547','117305237','113883714','114526629','114791601',
                  '123885595','122628633','119043818','115563645','101726347','125032749','121970185',
                  '116735865','101514240','125785463','125750906','124804790','116456976','127190801',
                  '113900343','112191830','60077382','128549532','128171945','128105012','128814956',
                  '128024009','126051165','125818633','125750802','125632933','127586953','126802821',
                  '125632538','125632187','125252062','125251921','124411847','124133827','128828376',
                  '123994672','123836332','122819512','126682198','127781039','123689024','128812265',
                  '122309488','121977650','121967890','121824461','121318460','127656911','128778956',
                  '120708272','120314658','119159252','118786435','118690331','127128201','128620548',
                  '116086835','115060744','114832182','114293784','113845992','126803577','128573517',
                  '109407507','101852916','101836579','101193438','100890026','123046459','128401012',
                  '127577880','125880059','127342961','126722732','117676389','122213398','128178397',
                  '128132135','127180877','127175281','126426661','126369148','126220579','126220389',
                  '116477105','112246667','109475450']   
        
    for affiliation in cauca_affiliations:
        authors_set.update(ExtractorS.get_auid_list(affiliation))

    df_autores=ExtractorS.get_authors_df(authors_set)
    
    try:
        df_autores.to_csv('aux_autores.csv',index=False)
    except:
        print(df_autores)
    
    df_productos=ExtractorS.get_articles_full(cauca_affiliations)
    df_productos = df_productos.astype(str)
    df_productos.to_csv('aux_productos.csv',index=False)
    
    print('Extracción Scopus finalizada')
    
    del ExtractorS

    #########################################
    #Insertar fecha de extracción de los datos en ambos modulos
    #########################################
    
    metadb= MetaCvlacDBController()
    metadb.insert_datetime()
    
    metadb1= MetaGruplacDBController()
    metadb1.insert_datetime()
    
    metadbsco=MetaDBScoController()
    metadbsco.insert_datetime()

    ###############################
    #INTEGRACIÓN DE MODULOS PARA DATOS DE GRUPOS DE INVESTIGACIÓN
    #################################
    
    #Inserción a base de datos de SCOPUS
    aux_articulosg = pd.read_csv('aux_articulosg.csv', dtype = str)
    aux_basicog = pd.read_csv('aux_basicog.csv', dtype = str)
    aux_caplibrosg = pd.read_csv('aux_caplibrosg.csv', dtype = str)
    aux_identificadores = pd.read_csv('aux_identificadores.csv', dtype = str)
    aux_integrantes = pd.read_csv('aux_integrantes.csv', dtype = str)
    aux_librosg = pd.read_csv('aux_librosg.csv', dtype = str) #pendiente de remplazo
    aux_oarticulos = pd.read_csv('aux_oarticulos.csv', dtype = str)
    aux_olibros = pd.read_csv('aux_olibros.csv', dtype = str)
    df_autores = pd.read_csv('aux_autores.csv', dtype = str).drop(['idgruplac','nombre_grupo','idcvlac'], axis=1)
    df_productos = pd.read_csv('aux_productos.csv', dtype = str).drop(['idgruplac','nombre_grupo'], axis=1)

    df_productos, df_autores=integrar(aux_articulosg,aux_basicog,aux_caplibrosg,aux_identificadores,aux_integrantes,aux_librosg,aux_oarticulos,aux_olibros,df_autores,df_productos)
    
    try:
        os.remove('aux_articulosg.csv')
        os.remove('aux_basicog.csv')
        os.remove('aux_caplibrosg.csv')
        os.remove('aux_identificadores.csv')
        os.remove('aux_integrantes.csv')
        os.remove('aux_librosg.csv')
        os.remove('aux_oarticulos.csv')
        os.remove('aux_olibros.csv')
        os.remove('aux_autores.csv')
        os.remove('aux_productos.csv')
        print('aux csv files deletede')
        
    except:
        print('Error deleting csv files')
    
    productos = ProductosController()
    try:
        print('insertando productos')
        productos.insert_df(df_productos)
        #df_productos.to_csv('df_productos_scopus.csv',index=False)
    except:
        print('error en inserción de datos para productos de scopus')
        raise
        #df_productos.to_csv('df_productos_scopus.csv',index=False)
        
    del productos
    
    autores = AutoresController()
    autores.insert_df(df_autores)
    
    print('Integración finalizada')
    
    ###############################
    #SCIENTOPY
    #################################
    """
    API_KEY=""
    INST_TOKEN=""
    API_KEY, INST_TOKEN = read_key()
    scientopy = Scientopy(API_KEY,INST_TOKEN)
    input_df = scientopy.scopus_preprocessed_df('"linked open data"')
    input_df.to_csv('papersPreprocessed.csv',index=False)
    """
