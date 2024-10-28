from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.NroJ import nroJ
from utils import db
from utils.db import db
from datetime import datetime
#Uso de blueprint, sirve para no tener que importar app y cargar los metodos y los html aca
NrosJ = Blueprint('NrosJ', __name__)

@NrosJ.route('/NrosJ')
def home():
    NrosJ = nroJ.query.all()
    return render_template('NumerosJudiciales.html', NrosJ=NrosJ)


@NrosJ.route('/new_NroJ', methods=['POST'])
def add_NroJ():
    fecha=datetime.strptime(request.form['fecha'], '%Y-%m-%d')
    secretario=request.form['secretario']
    destino=request.form['destino']
    motivo=request.form['motivo']
    

    new_NroJ = nroJ(fecha, secretario, destino, motivo)
    
    db.session.add(new_NroJ)
    db.session.commit()


    flash("Se ha marcó un numero judicial satisfactoriamente!")

    return redirect(url_for('NrosJ.home'))

@NrosJ.route('/NrosJ/update/<id>', methods=['POST', 'GET'])
def update(id):
        print(id)
        NroJ = nroJ.query.get(id)
        if request.method == 'POST':
            
            NroJ.fecha = request.form["fecha"]
            NroJ.secretario = request.form["secretario"]
            NroJ.destino = request.form["destino"]
            NroJ.motivo = request.form["motivo"]

            db.session.commit()
            
            flash("Se actualizó un numero judicial satisfactoriamente!")

            return redirect(url_for('NrosJ.home')) 
        
        
        return render_template('updateNroJ.html', NroJ=NroJ)

@NrosJ.route('/NrosJ/delete/<id>')
def delete(id):
        NroJ = nroJ.query.get(id)
        db.session.delete(NroJ)
        db.session.commit()

        flash("Se borró un Numero judicial satisfactoriamente!")


        return redirect(url_for('NrosJ.home'))


@NrosJ.route('/about')
def about():
    return render_template('about.html')