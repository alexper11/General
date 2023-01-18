from cvlac.ExtractorCvlac import ExtractorCvlac
from cvlac.ExtractorGruplac import ExtractorGruplac
from cvlac.util import get_lxml
from scopus.ExtractorScopus import ExtractorScopus
from scopus.Scientopy import Scientopy
# from scopus.readKey import read_key

import pandas as pd
import sys
import requests
import json
from requests.exceptions import ConnectionError

# from scopus.models.DBmodel import create_scopus_db
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

#############
import threading
import time
###########   end librerias flask   ###########

#crea una nueva instancia de flask:
app= Flask(__name__)
bootstrap = Bootstrap(app)

app.config['SECRET_KEY']='SUPER SECRETO' #No es la mejor practica


class FieldFormAutor(FlaskForm):
    id_autor = StringField('Digite el Author ID:', validators=[DataRequired()])
    submit_autor = SubmitField('Extraer Autor')
class FieldFormProducto(FlaskForm):
    id_producto = StringField('Digite el EID del producto:', validators=[DataRequired()])
    submit_producto = SubmitField('Extraer Producto')

class CredentialForm(FlaskForm):
    apikey = StringField('Digite el Apikey:', validators=[DataRequired()])
    token = StringField('Digite el Token:', validators=[DataRequired()])
    submit_credential = SubmitField('Registrar')


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

    response = make_response(redirect('/home_scopus'))
    session['user_ip'] = user_ip
    return response

@app.route('/home_scopus', methods=['GET', 'POST']) #ruta en que
def home():
    user_ip = session.get('user_ip')
    credential_form = CredentialForm()
    apikey = session.get('apikey')
    token = session.get('token')

    context = {
        'user_ip' : user_ip,
        'login_form' : credential_form,
        'apikey' : apikey,
        'token' : token
    }

    if credential_form.validate_on_submit():#detecta cuando hay post y valida la forma
        apikey = credential_form.apikey.data
        token = credential_form.token.data
        session['apikey'] = apikey
        session['token'] = token

        flash('Credenciales registradas con éxito')

        return redirect(url_for('extractor'))

    return render_template('home_scopus.html', **context)

@app.route('/extractor_scopus', methods=['GET', 'POST'])
def extractor():
    field_form_autor = FieldFormAutor()
    field_form_producto = FieldFormProducto()
    #credential_form = CredentialForm()
    id_autor = session.get('id_autor')
    id_producto = session.get('id_producto')
    apikey = session.get('apikey')
    token = session.get('token')


    context_extractor = {
        'field_form_autor' : field_form_autor,
        'field_form_producto' : field_form_producto,
        'id_autor' : id_autor,
        'id_producto' : id_producto,
        # 'credential_form': credential_form,
        'apikey' : apikey,
        'token' : token
    }

    if field_form_autor.validate_on_submit():
        id_autor = field_form_autor.id_autor.data
        session['id_autor'] = id_autor
        apikey = session.get('apikey')
        token = session.get('token')
        try:
            sys.path.append(".")
            print('Inicializando prueba...')            
            print('api: ', apikey)
            print ('token: ',token)
            ExtractorS = ExtractorScopus(apikey,token)
            state_api = ExtractorS.get_credential_validator(id_autor)
            if state_api == 'APIKEY_INVALID':
                print('Credenciales invalidas')
                flash('Credenciales inválidas')
            else:
                #Inicio
                print('Credenciales validas')
                
               
                df_autores=ExtractorS.get_authors_df([id_autor])
                flash('Extracción del perfil de Scopus terminado')
                if isinstance(df_autores,str):                    
                    flash(df_autores)
                else:
                    #df_autores.to_csv('df_autores.csv',index=False)
                                        
                    autores = AutoresController()
                    autores.delete_autor_id(id_autor)
                    autores.insert_df(df_autores)                    
                    flash('ghuarda')
            del ExtractorS
        except ConnectionError:            
            print('Error de conexion')
            flash('Error de conexión')
            #make_response(redirect('/home'))
        
        except:
            print('Error de texto, verificar valor ingresado')

        return redirect(url_for('extractor'))
    
    if field_form_producto.validate_on_submit():
        id_producto = field_form_producto.id_producto.data
        session['id_producto'] = id_producto
        apikey = session.get('apikey')
        token = session.get('token')
        try:
            sys.path.append(".")
            print('Inicializando prueba...')            
            print('api: ', apikey)
            print ('token: ',token)
            ExtractorS = ExtractorScopus(apikey,token)
            state_api = ExtractorS.get_credential_validator(id_producto)
            if state_api == 'APIKEY_INVALID':
                print('Credenciales invalidas')
                flash('Credenciales inválidas')
            else:
                #Inicio
                print('Credenciales validas')                
               
                df_productos=ExtractorS.get_article(id_producto)#eid
                flash('Extracción del perfil de Scopus terminado')
                print('df_prodcutos:', df_productos)
                if isinstance(df_productos,str):                    
                    flash(df_productos)
                else:
                    #df_productos.to_csv('df_productos.csv',index=False)
                    
                    productos = ProductosController()
                    productos.delete_eid(id_producto)
                    productos.insert_df(df_productos)                    
                    flash('ghuarda')
            del ExtractorS
                    

        except ConnectionError:            
            print('Error de conexion')
            flash('Error de conexión')
            #make_response(redirect('/home'))
        
        except:
            raise
            print('Error de texto, verificar valor ingresado')

        return redirect(url_for('extractor'))

    return render_template('extractor_scopus.html', **context_extractor)

@app.route('/scopus', methods=['GET', 'POST'])
def scopus():
    return render_template('scopus.html')