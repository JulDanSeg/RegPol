from flask import Blueprint, render_template, request, redirect, url_for, flash, send_file
from models.Causa import Causa
from models.efectivo import Efectivo
from models.expte import Expte
from utils import db
from utils.db import db
from datetime import datetime
import pandas as pd
from io import BytesIO
from flask_login import login_required

#Uso de blueprint, sirve para no tener que importar app y cargar los metodos y los html aca
causas = Blueprint('causas', __name__)

@causas.route('/causas')
@login_required
def home():
    causas = Causa.query.all()
    return render_template('Causas.html', causas=causas)


@causas.route('/new_causa', methods=['POST'])
def add_causa():
    fechaini=datetime.strptime(request.form['fechaini'], '%Y-%m-%d')
    ptvo=request.form['ptvo']
    nroExpte=request.form['nroExpte']
    detalle=request.form['detalle']
    secretario=request.form['secretario']
    instructor=request.form['instructor']


    

    new_causa = Causa(fechaini, ptvo, nroExpte, detalle, secretario, instructor,)
    
    db.session.add(new_causa)
    db.session.commit()


    flash("Se ha añadido una causa satisfactoriamente!")

    return redirect(url_for('causas.home'))

@causas.route('/causas/update/<id>', methods=['POST', 'GET'])
def update(id):
        print(id)
        causa = Causa.query.get(id)
        if request.method == 'POST':
            
            causa.fechaini = request.form["fechaini"]
            causa.ptvo = request.form["ptvo"]
            causa.nroExpte = request.form["nroExpte"]
            causa.detalle = request.form["detalle"]
            causa.secretario = request.form["secretario"]
            causa.instructor = request.form["instructor"]



            db.session.commit()
            
            flash("Se actualizó una causa satisfactoriamente!")

            return redirect(url_for('causas.home')) 
        
        
        return render_template('updateCausas.html', causa=causa)

@causas.route('/causas/delete/<id>')
def delete(id):
        causa = Causa.query.get(id)
        db.session.delete(causa)
        db.session.commit()

        flash("Se borró una causa satisfactoriamente!")


        return redirect(url_for('causas.home'))

@causas.route('/export/causas')
def export_excel():
    # Consulta de los datos de la base de datos
    causas = Causa.query.all()
    
    # Crear un DataFrame de Pandas
    data = [
        {
            "ID": causa.id,
            "Fecha Inicio": causa.fechaini,
            "Of Preventivo": causa.ptvo,
            "Nro. Expte": causa.nroExpte,
            "Detalle": causa.detalle,
            "Secretario": causa.secretario,
            "Instructor": causa.instructor
        }
        for causa in causas
    ]
    df = pd.DataFrame(data)

    # Guardar el DataFrame en un archivo Excel en memoria
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name="causas")
    output.seek(0)

    # Enviar el archivo al cliente para descargarlo
    return send_file(output, as_attachment=True, download_name="causas.xlsx", mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

@causas.route('/buscar', methods=['GET'])
def buscar():
    query = request.args.get('query')
    tabla = request.args.get('tabla')
    resultados = []

    if query:
        if tabla == 'efectivo':
            resultados = Efectivo.query.filter(
                (Efectivo.fullname.like(f'%{query}%')) |
                (Efectivo.DNI.like(f'%{query}%')) |
                (Efectivo.LP.like(f'%{query}%'))
            ).all()

        elif tabla == 'expediente':
            resultados = Expte.query.filter(
                (Expte.proc.like(f'%{query}%')) |
                (Expte.detalle.like(f'%{query}%')) |
                (Expte.secretario.like(f'%{query}%')) |
                (Expte.instructor.like(f'%{query}%'))
            ).all()

        elif tabla == 'causa':
            resultados = Causa.query.filter(
                (Causa.ptvo.like(f'%{query}%')) |
                (Causa.detalle.like(f'%{query}%')) |
                (Causa.nroExpte.like(f'%{query}%')) |
                (Causa.secretario.like(f'%{query}%')) |
                (Causa.instructor.like(f'%{query}%'))
            ).all()

        elif tabla == 'todos':
            resultados_efectivo = Efectivo.query.filter(
                (Efectivo.fullname.like(f'%{query}%')) |
                (Efectivo.DNI.like(f'%{query}%')) |
                (Efectivo.LP.like(f'%{query}%'))
            ).all()

            resultados_expediente = Expte.query.filter(
                (Expte.proc.like(f'%{query}%')) |
                (Expte.detalle.like(f'%{query}%')) |
                (Expte.secretario.like(f'%{query}%')) |
                (Expte.instructor.like(f'%{query}%'))
            ).all()

            resultados_causa = Causa.query.filter(
                (Causa.ptvo.like(f'%{query}%')) |
                (Causa.detalle.like(f'%{query}%')) |
                (Causa.nroExpte.like(f'%{query}%')) |
                (Causa.secretario.like(f'%{query}%')) |
                (Causa.instructor.like(f'%{query}%'))
            ).all()

            resultados = resultados_efectivo + resultados_expediente + resultados_causa

    return render_template('resultados.html', resultados=resultados)


@causas.route('/about')
def about():
    return render_template('about.html')