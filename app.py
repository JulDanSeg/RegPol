from flask import Flask
from routes.efectivos import efectivos
from routes.exptes import exptes
from routes.Causas import causas
from routes.NrosJ import NrosJ
from routes.NrosVar import NrosV
from routes.secuestros import secuestros
from routes.users import users
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from models.User import User



#creacion de la app
app = Flask(__name__)


app.secret_key = "secret_key"   
#configuración de mysql
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost/contactsdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False    

login_manager = LoginManager(app)

login_manager.login_view = 'users.login'  # Nombre de la función de vista de la ruta de inicio de sesión

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


#import del blueprint
app.register_blueprint(efectivos)
app.register_blueprint(exptes)
app.register_blueprint(causas)
app.register_blueprint(NrosJ)
app.register_blueprint(NrosV)
app.register_blueprint(secuestros)
app.register_blueprint(users)

