from flask import Blueprint, render_template, request, redirect, url_for, flash, send_file
from models.secuestro import Secuestro
from utils import db
from utils.db import db
from datetime import datetime
import pandas as pd
from io import BytesIO
from flask_login import login_required

#Uso de blueprint, sirve para no tener que importar app y cargar los metodos y los html aca
secuestros = Blueprint('secuestros', __name__)

@secuestros.route('/secuestros')
@login_required
def home():
    secuestros = Secuestro.query.all()
    return render_template('Secuestros.html', secuestros=secuestros)


@secuestros.route('/new_secuestro', methods=['POST'])
def add_secuestro():
    fechaing=datetime.strptime(request.form['fechaing'], '%Y-%m-%d')
    detalle=request.form['detalle']
    nroExpte=request.form['nroExpte']
    fechasal=request.form['fechasal']


    

    new_secuestro = Secuestro(fechaing, detalle, nroExpte, fechasal,)
    
    db.session.add(new_secuestro)
    db.session.commit()


    flash("Se ha añadido una secuestro satisfactoriamente!")

    return redirect(url_for('secuestros.home'))

@secuestros.route('/secuestros/update/<id>', methods=['POST', 'GET'])
def update(id):
        print(id)
        secuestro = Secuestro.query.get(id)
        if request.method == 'POST':
            
            secuestro.fechaing = request.form["fechaing"]
            secuestro.detalle = request.form["detalle"]
            secuestro.nroExpte = request.form["nroExpte"]
            secuestro.fechasal = request.form["fechasal"]



            db.session.commit()
            
            flash("Se actualizó una secuestro satisfactoriamente!")

            return redirect(url_for('secuestros.home')) 
        
        
        return render_template('updatesecuestros.html', secuestro=secuestro)

@secuestros.route('/secuestros/delete/<id>')
def delete(id):
        secuestro = Secuestro.query.get(id)
        db.session.delete(secuestro)
        db.session.commit()

        flash("Se borró una secuestro satisfactoriamente!")


        return redirect(url_for('secuestros.home'))

@secuestros.route('/export/secuestros')
def export_excel():
    # Consulta de los datos de la base de datos
    secuestros = Secuestro.query.all()
    
    # Crear un DataFrame de Pandas
    data = [
        {
            "ID": secuestro.id,
            "Fecha Ingreso": secuestro.fechaing,
            "Detalle": secuestro.detalle,
            "Nro. Expte": secuestro.nroExpte,
            "Fecha Salida": secuestro.fechasal,

        }
        for secuestro in secuestros
    ]
    df = pd.DataFrame(data)

    # Guardar el DataFrame en un archivo Excel en memoria
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name="secuestros")
    output.seek(0)

    # Enviar el archivo al cliente para descargarlo
    return send_file(output, as_attachment=True, download_name="secuestros.xlsx", mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")



@secuestros.route('/about')
def about():
    return render_template('about.html')