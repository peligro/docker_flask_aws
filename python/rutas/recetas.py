from flask_restful import Resource, request
from marshmallow.exceptions import ValidationError
from .dto import RecetaSchema
from bson.objectid import ObjectId


def init_db(mongo):
    global mongoDb
    mongoDb = mongo 

class RecetaRuta(Resource):
    
    def get(self):
        #datos = list(categories.find())
        #datos2 = list(mongoDb.db.recipes.find().sort('_id', -1))  # Cambia '_id' por otro campo si es necesario
        """
        pipeline = [
            {
                "$lookup": {
                    "from": "categories",  # Nombre de la colección de usuarios
                    "localField": "category_id",
                    "foreignField": "_id",
                    "as": "category"
                }
            },
            {
                "$unwind": {
                    "path": "$category",
                    "preserveNullAndEmptyArrays": True
                }
            },
            {
                "$project": {
                    "_id": 1,
                    "nombre": 1,
                    "slug": 1,
                    "category_id": {"$toString": "$category_id"},
                    "category":  "$category.nombre"
                }
            },
            {
                "$sort": {
                    "_id": -1  # -1 para orden descendente, 1 para ascendente
                }
            }
            ]
        """
        pipeline = [
            {
                "$lookup": {
                    "from": "categories",  # Nombre de la colección de usuarios
                    "localField": "category_id",
                    "foreignField": "_id",
                    "as": "category"
                }
            },
            {
                "$unwind": {
                    "path": "$category",
                    "preserveNullAndEmptyArrays": True
                }
            },
            {
                "$project": {
                    "_id": 1,
                    "nombre": 1,
                    "slug": 1,
                    "category_id": {"$toString": "$category_id"},
                    "category":  "$category.nombre"
                }
            } 
            ]
        pipeline.append({
            "$sort": {
                "_id": -1
            }
        })
        # Agregar el filtro si se proporciona el parámetro
        """
        pipeline.append({
            "$match": {
                "user_name": user_name  # Filtrar por nombre exacto
            }
        })
        """
        #agregar filtro con like
        """
        pipeline.append({
            "$match": {
                "user_name": {"$regex": user_name, "$options": "i"}  # Búsqueda parcial, insensible a mayúsculas
            }
        })
        """
        datos = list(mongoDb.db.recipes.aggregate(pipeline))
        for dato in datos:
            dato["_id"] = str(dato["_id"])
            dato["category_id"] = str(dato["category_id"])
        return {"data":datos}, 200

    
    def post(self):
        esquema = RecetaSchema()
        try:
            data = esquema.load(request.get_json())
            mongoDb.db.recipes.insert_one({
                "nombre": data['nombre'],
                "slug": data['nombre'],
                "category_id":ObjectId(data['category_id'])
            })
            return {"estado":"ok", "mensaje":f"Se crea el registro exitosamente"}, 201
        except ValidationError as err:
            return {"error": err.messages}, 400