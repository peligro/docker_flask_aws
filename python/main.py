from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from rutas import ejemplo, categorias, recetas
from flask_pymongo import PyMongo


app = Flask(__name__)
api = Api(app)
app.secret_key = "123456"
#docker exec -it python_service python main.py
#docker exec -it python_service python main.py --host=0.0.0 -p 8080

#para que nos muestre trazabilidad en la terminal en la ejecución. No llevar esto a producción
@app.before_request
def log_request_info():
    app.logger.info('Headers: %s', request.headers)
    app.logger.info('Body: %s', request.get_data())

# Configuración de la base de datos
app.config["MONGO_URI"] = "mongodb://mongo:27017/mi_db"
mongo = PyMongo(app)

"""
class Ejemplo(Resource):
    
    def get(self):
        return jsonify({"estado":"ok", "mensaje":"Métogo GET"})

    def post(self):
        return jsonify({"estado":"ok", "mensaje":"Método POST"})
    
    def put(self):
        return jsonify({"estado":"ok", "mensaje":"Método PUT"})
    
    def delete(self):
        return jsonify({"estado":"ok", "mensaje":"Método DELETE"})

"""
@app.errorhandler(404)
def page_not_found(error):
    return jsonify({"estado":"error", "mensaje":"Recurso no disponible"}), 404


api.add_resource(ejemplo.EjemploRuta, '/ejemplo')
api.add_resource(ejemplo.EjemploRutaParametro, "/ejemplo/<id>")
api.add_resource(ejemplo.EjemploRutaUpload, '/ejemplo-upload')
api.add_resource(ejemplo.EjemploRutaUploadS3, '/ejemplo-s3')
api.add_resource(ejemplo.EjemploRutaUploadS3Imagen, "/ejemplo-s3-imagen")


categorias.init_db(mongo)
api.add_resource(categorias.CategoriaRuta, '/categorias')
api.add_resource(categorias.CategoriaRutaParametro, "/categorias/<id>")

recetas.init_db(mongo)
api.add_resource(recetas.RecetaRuta, '/recetas')



if __name__=='__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)