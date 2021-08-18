from marshmallow import Schema, fields, ValidationError


class TodoSchema(Schema):
    id = fields.Int(dump_only=True)
    user_id = fields.Int(required=True)
    titulo = fields.Str(required=True)
    descripcion = fields.Str(required=True)
