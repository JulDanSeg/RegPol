from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.NroVar import nroVar
from utils import db
from utils.db import db
from datetime import datetime
#Uso de blueprint, sirve para no tener que importar app y cargar los metodos y los html aca
NrosV = Blueprint('NrosV', __name__)

@NrosV.route('/NrosV')
def home():
    NrosV = nroVar.query.all()
    return render_template('NumerosVarios.html', NrosV=NrosV)


@NrosV.route('/new_NroV', methods=['POST'])
def add_NroV():
    fecha=datetime.strptime(request.form['fecha'], '%Y-%m-%d')
    secretario=request.form['secretario']
    destino=request.form['destino']
    motivo=request.form['motivo']
    

    new_NroV = nroVar(fecha, secretario, destino, motivo)
    
    db.session.add(new_NroV)
    db.session.commit()


    flash("Se ha marcó un numero vario satisfactoriamente!")

    return redirect(url_for('NrosV.home'))

@NrosV.route('/NrosV/update/<id>', methods=['POST', 'GET'])
def update(id):
        print(id)
        NroV = nroVar.query.get(id)
        if request.method == 'POST':
            
            NroV.fecha = request.form["fecha"]
            NroV.secretario = request.form["secretario"]
            NroV.destino = request.form["destino"]
            NroV.motivo = request.form["motivo"]

            db.session.commit()
            
            flash("Se actualizó un numero vario satisfactoriamente!")

            return redirect(url_for('NrosV.home')) 
        
        
        return render_template('updateNroVario.html', NroV=NroV)

@NrosV.route('/NrosV/delete/<id>')
def delete(id):
        NroV = nroVar.query.get(id)
        db.session.delete(NroV)
        db.session.commit()

        flash("Se borró un Numero vario satisfactoriamente!")


        return redirect(url_for('NrosV.home'))


@NrosV.route('/about')
def about():
    return render_template('about.html')