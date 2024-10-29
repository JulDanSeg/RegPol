from flask import Flask
from routes.efectivos import efectivos
from routes.exptes import exptes
from routes.Causas import causas
from routes.NrosJ import NrosJ
from routes.NrosVar import NrosV

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
app.register_blueprint(causas)
app.register_blueprint(NrosJ)
app.register_blueprint(NrosV)

