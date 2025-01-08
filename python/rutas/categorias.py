from flask_restful import Resource, request
from flask import jsonify, Response
from marshmallow.exceptions import ValidationError
import os
from .dto import CategoriaSchema
from datetime import datetime
from bson.objectid import ObjectId


def init_db(mongo):
    global categories
    categories = mongo.db.categories

class CategoriaRuta(Resource):
    
    def get(self):
        #datos = list(categories.find())
        datos = list(categories.find().sort('_id', -1))  # Cambia '_id' por otro campo si es necesario

        for dato in datos:
            dato["_id"] = str(dato["_id"])
        return datos, 200

    
    def post(self):
        esquema = CategoriaSchema()
        try:
            data = esquema.load(request.get_json())
            item_id = categories.insert_one({
                "nombre": data['nombre'],
                "slug": data['nombre']
            })
            return {"estado":"ok", "mensaje":f"Se crea el registro exitosamente"}, 201
        except ValidationError as err:
            return {"error": err.messages}, 400
        
        
class CategoriaRutaParametro(Resource):

    def get(self, id):
        try:
            dato = categories.find_one({"_id": ObjectId(id)})
            dato["_id"] = str(dato["_id"])
            return dato, 200
        except:
            return {"error": "Recurso no disponible"}, 404
    
    
    def put(self, id):
        try:
            dato = categories.find_one({"_id": ObjectId(id)})
            dato["_id"] = str(dato["_id"])
            esquema = CategoriaSchema()
            try:
                data = esquema.load(request.get_json())
                result = categories.update_one({"_id": ObjectId(id)}, {"$set": {
                "nombre": data['nombre'],
                "slug": data['nombre']
            }})
            except ValidationError as err:
                return {"error": err.messages}, 400
            return {"estado":"ok", "mensaje":f"Se modifica el registro exitosamente"}, 201
        except:
            return {"error": "Recurso no disponible"}, 404

    
    def delete(self, id):
        try:
            result = categories.delete_one({"_id": ObjectId(id)})
            if result.deleted_count == 0:
                return {"error": "Recurso no disponible"}, 404
            return {"estado":"ok", "mensaje":f"Se elimina el registro exitosamente"}, 201
        except:
            return {"error": "Recurso no disponible"}, 404
    
    


