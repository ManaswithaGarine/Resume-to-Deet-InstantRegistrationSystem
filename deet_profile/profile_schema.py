"""Marshmallow schema for validating the DEET profile payload."""
from marshmallow import Schema, fields, validate

class ProfileSchema(Schema):
    name       = fields.Str(required=True, validate=validate.Length(min=1, max=120))
    email      = fields.Email(required=True)
    phone      = fields.Str(load_default="")
    skills     = fields.List(fields.Str(), load_default=[])
    education  = fields.List(fields.Dict(), load_default=[])
    experience = fields.List(fields.Dict(), load_default=[])
