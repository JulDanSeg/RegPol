from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.Causa import Causa
from utils import db
from utils.db import db
from datetime import datetime
#Uso de blueprint, sirve para no tener que importar app y cargar los metodos y los html aca
causas = Blueprint('causas', __name__)

@causas.route('/causas')
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


@causas.route('/about')
def about():
    return render_template('about.html')