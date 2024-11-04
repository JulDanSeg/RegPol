from utils.db import db


#Clase Secuestro, sus atributos y los tipos de estos ultimos
class Secuestro (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fechaing = db.Column(db.DateTime)
    detalle = db.Column(db.String(100))
    nroExpte = db.Column(db.Integer)
    fechasal = db.Column(db.DateTime)



#constructor
    def __init__(self, fechaing, detalle, nroExpte, fechasal):
        self.fechaing = fechaing
        self.detalle = detalle
        self.nroExpte = nroExpte
        self.fechasal = fechasal
   