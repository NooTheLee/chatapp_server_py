from marshmallow import Schema
import inflection

class CamelCaseSchema(Schema):
    def on_bind_field(self, field_name, field_obj):
        field_obj.data_key = inflection.camelize(field_name, False)
