from utils.db import db


#Clase expte, sus atributos y los tipos de estos ultimos
class Expte (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fechaing = db.Column(db.DateTime)
    proc = db.Column(db.String(100))
    detalle = db.Column(db.String(100))
    secretario = db.Column(db.Integer)
    instructor = db.Column(db.Integer)
    destino = db.Column(db.String(100))
    fechasal = db.Column(db.DateTime)
    obs = db.Column(db.String(100))

#constructor
    def __init__(self, fechaing, proc, detalle, secretario, instructor, destino, fechasal, obs):
        self.fechaing = fechaing
        self.proc = proc
        self.detalle = detalle
        self.secretario = secretario
        self.instructor = instructor
        self.destino = destino
        self.fechasal = fechasal
        self.obs = obs        