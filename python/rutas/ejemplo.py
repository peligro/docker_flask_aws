from flask_restful import Resource, request
from flask import jsonify
from marshmallow.exceptions import ValidationError
import os
from .dto import EjemploSchema
from datetime import datetime
from werkzeug.utils import secure_filename
 



class EjemploRuta(Resource):
    
    def get(self):
        return jsonify({"estado":"ok", "mensaje":"Métogo GET"})

    def post(self):
        esquema = EjemploSchema()
        try:
            data = esquema.load(request.get_json())
        except ValidationError as err:
            return {"error": err.messages}, 400
        
        return {"estado":"ok", "mensaje":f"Método POST | nombre={data["nombre"]} | correo={data["correo"]} | password={data["password"]}"}, 201

        
    
    """
    def post(self):
        data = request.get_json()
        return jsonify({"estado":"ok", "mensaje":f"Método POST | nombre={data["nombre"]} | correo={data["correo"]} | password={data["password"]}"})
    """
    
    


class EjemploRutaParametro(Resource):

    def get(self, id):
        return jsonify({"estado":"ok", "mensaje":f"Métogo GET | id={id}"})
    
    def put(self, id):
        esquema = EjemploSchema()
        try:
            data = esquema.load(request.get_json())
        except ValidationError as err:
            return {"error": err.messages}, 400
        return jsonify({"estado":"ok", "mensaje":f"Métogo PUT | id={id}"})
    
    def delete(self, id):
        return jsonify({"estado":"ok", "mensaje":f"Métogo DELETE | id={id}"})
    


class EjemploRutaUpload(Resource):
    
    
    def post(self):
        fecha = datetime.now()
        ruta=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        file = request.files['file'] 
        if file.content_type=="image/jpeg" or file.content_type=="image/png": 
            if file.content_type=="image/jpeg":
                archivo=f"{datetime.timestamp(fecha)}.jpg"
            if file.content_type=="image/png":
                archivo=f"{datetime.timestamp(fecha)}.png"
            file.save(os.path.join(f"{ruta}/public/ejemplo", archivo))
            return jsonify({"estado":"ok", "mensaje":"Métogo UPLOD", "ruta":ruta ,"file": secure_filename(file.filename), "nombre":archivo, "mime":file.content_type})
        else:
            return {"estado": "error", "mensaje":"Ocurrió un error inesperado"}, 400 
    
    """
    def post(self):
        ruta=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        file = request.files['file'] 
        file.save(os.path.join(f"{ruta}/public/ejemplo", file.filename))
        return jsonify({"estado":"ok", "mensaje":"Métogo UPLOD", "ruta":ruta ,"file": secure_filename(file.filename) })
    """   