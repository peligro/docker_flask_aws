from flask_restful import Resource, request
from flask import jsonify, Response
from marshmallow.exceptions import ValidationError
import os
from .dto import EjemploSchema
from datetime import datetime
from werkzeug.utils import secure_filename

import boto3

 
AWS_REGION = 'us-east-2'  # Cambia esto según tu región
S3_BUCKET_NAME = 'cesar-25-12'

s3_client = boto3.client(
    's3',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    region_name=AWS_REGION
)
folder_name="ejemplo"

class EjemploRutaUploadS3(Resource):
    
    def get(self):
        try:
            
            response = s3_client.list_objects_v2(
            Bucket=S3_BUCKET_NAME,
            Prefix=folder_name.rstrip('/') + '/'  # Asegurarse de que termine en '/'
            )
            files = [obj['Key'] for obj in response.get('Contents', [])]
            #print(files)
            return   files , 200

        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    
    def post(self):
        file = request.files['file']

        fecha = datetime.now()
        file = request.files['file'] 
        if file.content_type=="image/jpeg" or file.content_type=="image/png": 
            if file.content_type=="image/jpeg":
                archivo=f"{datetime.timestamp(fecha)}.jpg"
            if file.content_type=="image/png":
                archivo=f"{datetime.timestamp(fecha)}.png"

            try:
                # Subir el archivo a S3
                s3_client.upload_fileobj(
                    file,
                    S3_BUCKET_NAME,
                    f"{folder_name.rstrip('/')}/{archivo}",
                    ExtraArgs={'ContentType': file.content_type}
                )
                return {"estado": "ok", "mensaje": f'Se subió el archivo exitosamente'}, 200

            except Exception as e:
                return {'error': str(e)}, 500
        else:
            return {"estado": "error", "mensaje":"Ocurrió un error inesperado"}, 400 

    """
    def post(self):
        file = request.files['file']
        file = request.files['file']

        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400 

        try:
            # Subir el archivo a S3
            s3_client.upload_fileobj(
                file,
                S3_BUCKET_NAME,
                f"{folder_name.rstrip('/')}/{file.filename}",
                ExtraArgs={'ContentType': file.content_type}
            )
            return {'message': f'File {file.filename} uploaded successfully'}, 200

        except Exception as e:
            return {'error': str(e)}, 500
    """
            

class EjemploRutaUploadS3Imagen(Resource):

    
    def get(self):
        try:
            # Verificar si el archivo existe
            response = s3_client.get_object(Bucket=S3_BUCKET_NAME, Key=request.args.get('imagen'))

           
            return Response(
                response['Body'].read(),
                mimetype=response['ContentType']
            )
        except s3_client.exceptions.ClientError as e:
            if e.response['Error']['Code'] == "404":
                return {'error': f"Recurso no disponible"}, 404
            return {'error': str(e)}, 500
    """

    def get(self):
        try:
            # Verificar si el archivo existe
            response = s3_client.head_object(Bucket=S3_BUCKET_NAME, Key=request.args.get('imagen'))
            

            # Generar la URL estándar (archivo debe ser público)
            public_url = f"https://{S3_BUCKET_NAME}.s3.{AWS_REGION}.amazonaws.com/{request.args.get('imagen')}"
            return {'image_key': public_url }, 200
            
        except s3_client.exceptions.ClientError as e:
            if e.response['Error']['Code'] == "404":
                return {'error': f"Recurso no disponible"}, 404
            return {'error': str(e)}, 500
    """

    def delete(self):
        """
        Borra un archivo específico de una carpeta en S3.
        """
        try:
            # Eliminar el archivo
            s3_client.delete_object(Bucket=S3_BUCKET_NAME, Key=request.args.get('imagen'))
            return {'mensaje': "Se elimina achivo exitosamente"}, 200

        except s3_client.exceptions.NoSuchKey:
            return {'error':"Recurso no disponible"}, 404
        except Exception as e:
            return {'error': str(e)}, 500


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
            return jsonify({"estado":"ok", "mensaje":"Métogo UPLOD", "ruta":ruta ,"file": secure_filename(file.filename), "nombre":archivo, "mime":file.content_type, "id":request.form['id'] })
        else:
            return {"estado": "error", "mensaje":"Ocurrió un error inesperado"}, 400 
    
    """
    def post(self):
        ruta=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        file = request.files['file'] 
        file.save(os.path.join(f"{ruta}/public/ejemplo", file.filename))
        return jsonify({"estado":"ok", "mensaje":"Métogo UPLOD", "ruta":ruta ,"file": secure_filename(file.filename) })
    """   


