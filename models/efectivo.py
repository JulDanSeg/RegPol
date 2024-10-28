from utils.db import db


#Clase efectivo, sus atributos y los tipos de estos ultimos
class Efectivo (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(100))
    jerarquia = db.Column(db.String(100))
    LP = db.Column(db.Integer)
    DNI = db.Column(db.Integer)
    

#constructor
    def __init__(self, fullname, jerarquia, LP, DNI):
        self.fullname = fullname
        self.jerarquia = jerarquia
        self.LP = LP
        self.DNI = DNI