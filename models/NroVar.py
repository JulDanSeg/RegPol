from utils.db import db


#Clase efectivo, sus atributos y los tipos de estos ultimos
class nroVar (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.DateTime)
    secretario = db.Column(db.Integer)
    destino = db.Column(db.String(100))
    motivo = db.Column(db.String(100))

    

#constructor
    def __init__(self, fecha, secretario, destino, motivo):
        self.fecha = fecha
        self.secretario = secretario
        self.destino = destino
        self.motivo = motivo
