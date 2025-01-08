from marshmallow import Schema, fields, validates, validate
from marshmallow.exceptions import ValidationError




class EjemploSchema(Schema):
    nombre = fields.Str(
        required=True,
        validate=validate.Length(min=1, error="El campo nombre es obligatorio")
    )
    correo = fields.Email(
        required=True,
        error_messages={
            "required": "El campo correo es obligatorio.",
            "invalid": "El campo correo debe contener una dirección de correo válida."
        }
    )
    password = fields.Str(
        required=True,
        validate=validate.Length(min=1, error="El campo password es obligatorio")
    )


    @validates('nombre')
    def validate_nombre(self, value):
        if len(value) < 3:
            raise ValidationError('El nombre debe tener al menos 3 caracteres.')



class CategoriaSchema(Schema):
    nombre = fields.Str(
        required=True,
        validate=validate.Length(min=1, error="El campo nombre es obligatorio")
    )

    @validates('nombre')
    def validate_nombre(self, value):
        if len(value) < 3:
            raise ValidationError('El nombre debe tener al menos 3 caracteres.')
