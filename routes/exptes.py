from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.expte import Expte
from utils import db
from utils.db import db
from datetime import datetime
#Uso de blueprint, sirve para no tener que importar app y cargar los metodos y los html aca
exptes = Blueprint('exptes', __name__)

@exptes.route('/exptes')
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


@exptes.route('/about')
def about():
    return render_template('about.html')