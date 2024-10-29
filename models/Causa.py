from utils.db import db


#Clase causa, sus atributos y los tipos de estos ultimos
class Causa (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fechaini = db.Column(db.DateTime)
    ptvo= db.Column(db.Integer)
    nroExpte = db.Column(db.Integer)
    detalle = db.Column(db.String(100))
    secretario = db.Column(db.Integer)
    instructor = db.Column(db.Integer)



#constructor
    def __init__(self, fechaini, ptvo, nroExpte, detalle, secretario, instructor):
        self.fechaini = fechaini
        self.ptvo = ptvo
        self.nroExpte = nroExpte
        self.detalle = detalle
        self.secretario = secretario
        self.instructor = instructor
   