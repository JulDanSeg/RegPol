from flask import Blueprint, render_template, request, redirect, url_for, flash, send_file
from models.expte import Expte
from models.Causa import Causa
from models.efectivo import Efectivo
from utils import db
from utils.db import db
from datetime import datetime
import pandas as pd
from io import BytesIO
from flask_login import login_required

#Uso de blueprint, sirve para no tener que importar app y cargar los metodos y los html aca
exptes = Blueprint('exptes', __name__)

@exptes.route('/exptes')
@login_required
def home():
    exptes = Expte.query.all()
    return render_template('expedientes.html', exptes=exptes)


@exptes.route('/new_expte', methods=['POST'])
def add_expte():
    fechaing=datetime.strptime(request.form['fechaing'], '%Y-%m-%d')
    proc=request.form['proc']
    detalle=request.form['detalle']
    secretario=request.form['secretario']
    instructor=request.form['instructor']
    destino=request.form['destino']
    fechasal=request.form['fechasal']
    if fechasal:
        fechasal = datetime.strptime(fechasal, '%Y-%m-%d')
    else:
        fechasal = None
    obs=request.form['obs']
    

    new_expte = Expte(fechaing, proc, detalle, secretario, instructor, destino, fechasal, obs)
    
    db.session.add(new_expte)
    db.session.commit()


    flash("Se ha añadido un expediente satisfactoriamente!")

    return redirect(url_for('exptes.home'))

@exptes.route('/exptes/update/<id>', methods=['POST', 'GET'])
def update(id):
        print(id)
        expte = Expte.query.get(id)
        if request.method == 'POST':
            
            expte.fechaing = request.form["fechaing"]
            expte.proc = request.form["proc"]
            expte.detalle = request.form["detalle"]
            expte.secretario = request.form["secretario"]
            expte.instructor = request.form["instructor"]
            expte.destino = request.form["destino"]
            expte.fechasal = request.form["fechasal"]
            expte.obs = request.form["obs"]

            db.session.commit()
            
            flash("Se actualizó un expediente satisfactoriamente!")

            return redirect(url_for('exptes.home')) 
        
        
        return render_template('updateexpte.html', expte=expte)

@exptes.route('/exptes/delete/<id>')
def delete(id):
        expte = Expte.query.get(id)
        db.session.delete(expte)
        db.session.commit()

        flash("Se borró un expediente satisfactoriamente!")


        return redirect(url_for('exptes.home'))

@exptes.route('/export/exptes')
def export_excel():
    # Consulta de los datos de la base de datos
    exptes = Expte.query.all()
    
    # Crear un DataFrame de Pandas
    data = [
        {
            "ID": expte.id,
            "Fecha Ingreso": expte.fechaing,
            "Procedencia": expte.proc,
            "Detalle": expte.detalle,
            "Secretario": expte.secretario,
            "Instructor": expte.instructor,
            "Destino": expte.destino,
            "Fecha Salida": expte.fechasal,
            "Observaciones": expte.obs,

        }
        for expte in exptes
    ]
    df = pd.DataFrame(data)

    # Guardar el DataFrame en un archivo Excel en memoria
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name="exptes")
    output.seek(0)

    # Enviar el archivo al cliente para descargarlo
    return send_file(output, as_attachment=True, download_name="exptes.xlsx", mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

@exptes.route('/buscar', methods=['GET'])
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


@exptes.route('/about')
def about():
    return render_template('about.html')