from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.efectivo import Efectivo
from utils import db
from utils.db import db
#Uso de blueprint, sirve para no tener que importar app y cargar los metodos y los html aca
efectivos = Blueprint('efectivos', __name__)

@efectivos.route('/')
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


@efectivos.route('/about')
def about():
    return render_template('about.html')
