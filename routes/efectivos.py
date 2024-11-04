from flask import Blueprint, render_template, request, redirect, url_for, flash, send_file
from models.efectivo import Efectivo
from models.Causa import Causa
from models.expte import Expte
from utils import db
from utils.db import db
import pandas as pd
from io import BytesIO
from flask_login import login_required


#Uso de blueprint, sirve para no tener que importar app y cargar los metodos y los html aca
efectivos = Blueprint('efectivos', __name__)

@efectivos.route('/dashboard')


@efectivos.route('/')
@login_required
def home():
    efectivos = Efectivo.query.all()
    return render_template('index.html', efectivos=efectivos)



@efectivos.route('/new_efectivo', methods=['POST'])
def add_efectivo():
    fullname=request.form['fullname']
    jerarquia=request.form['jerarquia']
    LP=request.form['LP']
    DNI=request.form['DNI']

    new_efectivo = Efectivo(fullname, jerarquia, LP, DNI)
    
    db.session.add(new_efectivo)
    db.session.commit()


    flash("Se ha añadido personal satisfactoriamente!")

    return redirect(url_for('efectivos.home'))

@efectivos.route('/update_efectivo/<id>', methods=['POST', 'GET'])
def update(id):
        print(id)
        efectivo = Efectivo.query.get(id)
        if request.method == 'POST':
            
            efectivo.fullname = request.form["fullname"]
            efectivo.jerarquia = request.form["jerarquia"]
            efectivo.LP = request.form["LP"]
            efectivo.DNI = request.form["DNI"]

            db.session.commit()
            
            flash("Se actualizó el personal satisfactoriamente!")

            return redirect(url_for('efectivos.home')) 
        
        
        return render_template('update.html', efectivo=efectivo)

@efectivos.route('/delete/<id>')
def delete(id):
        efectivo = Efectivo.query.get(id)
        db.session.delete(efectivo)
        db.session.commit()

        flash("Se borró personal satisfactoriamente!")


        return redirect(url_for('efectivos.home'))

@efectivos.route('/export/efectivos')
def export_excel():
    # Consulta de los datos de la base de datos
    efectivos = Efectivo.query.all()
    
    # Crear un DataFrame de Pandas
    data = [
        {
            "ID": efectivo.id,
            "Nombre Completo": efectivo.fullname,
            "Jerarquía": efectivo.jerarquia,
            "LP": efectivo.LP,
            "DNI": efectivo.DNI
        }
        for efectivo in efectivos
    ]
    df = pd.DataFrame(data)

    # Guardar el DataFrame en un archivo Excel en memoria
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name="Efectivos")
    output.seek(0)

    # Enviar el archivo al cliente para descargarlo
    return send_file(output, as_attachment=True, download_name="efectivos.xlsx", mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")


@efectivos.route('/buscar', methods=['GET'])
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


@efectivos.route('/about')
def about():
    return render_template('about.html')
