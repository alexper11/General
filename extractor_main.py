from cvlac.ExtractorCvlac import ExtractorCvlac
from cvlac.ExtractorGruplac import ExtractorGruplac
from cvlac.util import get_lxml
from scopus.ExtractorScopus import ExtractorScopus
from scopus.Scientopy import Scientopy
from scopus.readKey import read_key

import pandas as pd
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

#############   Librerias para flask  #########
from flask import Flask, request, make_response, redirect, render_template, session, url_for, flash, jsonify
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms.fields import StringField, SubmitField, RadioField
from wtforms.validators import DataRequired
import unittest
###########   end librerias flask   ###########

#crea una nueva instancia de flask:
app= Flask(__name__)
bootstrap = Bootstrap(app)

app.config['SECRET_KEY']='SECRETO' #test

    
class FieldFormCvlac(FlaskForm):
    enlace_cvlac = StringField('Digite enlace Cvlac:', validators=[DataRequired()])    
    submit_cvlac = SubmitField('Extraer cvlac')
    
class FieldFormGruplac(FlaskForm):
    enlace_gruplac = StringField('Digite enlace Gruplac:', validators=[DataRequired()])
    action_gruplac = RadioField('Elige una opción:', choices = ['Extraer datos del Gruplac', 'Extraer datos del los investigadores del Gruplac'], validators=[DataRequired()])
    submit_gruplac = SubmitField('Extraer gruplac')

#Creamos un decorador:
@app.cli.command()
def test():
    #Todo lo que encuentre unittest en el directorio tests:
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner().run(tests)
    

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html',error=error)

@app.route('/')
def index():
    user_ip = request.remote_addr

    response = make_response(redirect('/home'))
    session['user_ip'] = user_ip

    return response

@app.route('/home', methods=['GET', 'POST']) #ruta en que
def home():
    user_ip = session.get('user_ip')    
    context = {
        'user_ip' : user_ip
    }        
    return render_template('home.html', **context)

@app.route('/extractor', methods=['GET', 'POST'])
def extractor():
    field_form_cvlac = FieldFormCvlac()
    enlace_cvlac = session.get('enlace_cvlac')
        
    field_form_gruplac = FieldFormGruplac()
    enlace_gruplac = session.get('enlace_gruplac')
    action_gruplac = session.get('action_gruplac')
        
    context_extractor = {
        'field_form_cvlac' : field_form_cvlac,
        'enlace_cvlac' : enlace_cvlac,
        'field_form_gruplac' : field_form_gruplac,
        'action_gruplac' : action_gruplac,
        'enlace_gruplac' : enlace_gruplac
    }        
        
    if field_form_cvlac.validate_on_submit():
        enlace_cvlac = field_form_cvlac.enlace_cvlac.data
        session['enlace_cvlac'] = enlace_cvlac
        if 'https://scienti.minciencias.gov.co/cvlac/visualizador/' in enlace_cvlac:
            try:
                Extractor=ExtractorGruplac()
                #urls cvlac:                    
                dom=get_lxml(enlace_cvlac)
                df_prueba=Extractor.get_articulo(dom,enlace_cvlac)  
                
                df_prueba.to_csv('extraccion_cvlac_individual.csv',index=False)
                flash('Extracción del perfil de Cvlac terminado')                
            except:
                flash('Error de conexion')
            #make_response(redirect('/home'))
        else:
            flash('Lo sentimos, link incorrecto')
        
        return redirect(url_for('extractor'))        
    
    if field_form_gruplac.validate_on_submit():#detecta cuando hay post y valida la forma
        enlace_gruplac = field_form_gruplac.enlace_gruplac.data
        action_gruplac = field_form_gruplac.action_gruplac.data
        session['enlace_gruplac'] = enlace_gruplac
        session['action_gruplac'] = action_gruplac
        if 'https://scienti.minciencias.gov.co/gruplac/jsp/' in enlace_gruplac:
            try:       
                Extractor=ExtractorGruplac()        
                
                #Extrae datos de un gruplac:
                if action_gruplac == 'Extraer datos del Gruplac':
                    list_url = enlace_gruplac
                    #render_template('home.html')
                    dom=get_lxml(enlace_gruplac)
                    df_prueba=Extractor.get_perfil_articulos(dom,enlace_gruplac)  
                    df_prueba.to_csv('extraccion_gruplac.csv',index=False)
                                
                    flash('Extracción del perfil de Gruplac terminado')
                    
                #Extrae datos de investigadores de gruplac:
                elif action_gruplac == 'Extraer datos del los investigadores del Gruplac':            
                    list_url=Extractor.get_members_list(enlace_gruplac)
                    for url in list_url:
                        dom=get_lxml(url)                
                        df_prueba=Extractor.get_articulo(dom,url)
                        print("extrayendo") 
                    df_prueba.to_csv('extraccion_cvlacs_gruplac.csv',index=False)
                                
                    flash('Extracción de los Cvlacs del perfil de Gruplac terminado')
                    
                else:
                    #make_response(redirect('/home'))
                    pass  
            except:
                flash('Error de conexion')            
        else:
            flash('Lo sentimos, link incorrecto')
            
        return redirect(url_for('extractor'))
   
    return render_template('extractor.html', **context_extractor)

@app.route('/scopus', methods=['GET', 'POST']) 
def scopus():    
    return render_template('scopus.html')