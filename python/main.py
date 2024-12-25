from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from rutas import ejemplo

app = Flask(__name__)
api = Api(app)
app.secret_key = "123456"


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

if __name__=='__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)