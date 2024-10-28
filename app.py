from flask import Flask
from routes.efectivos import efectivos
from routes.exptes import exptes

from flask_sqlalchemy import SQLAlchemy



#creacion de la app
app = Flask(__name__)


app.secret_key = "secret_key"   
#configuración de mysql
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost/contactsdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False    




#import del blueprint
app.register_blueprint(efectivos)
app.register_blueprint(exptes)

