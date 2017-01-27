import re
import graphene
from graphql.type import definition

class MongoSchema(graphene.ObjectType):
    """
        A class to create a graphene graphl schema based on mongoengine model.
        See https://github.com/graphql-python/graphene/issues/51
    """

    def __init__(self, *args, **kwargs):
        self.__generate_mongo_schema(self.__Model__)
        super().__init__(*args, **kwargs)

    @classmethod
    def __generate_mongo_schema(cls, mongo_model):

        pattern = re.compile('^<mongoengine.fields.(\\w+) object at .*>$')

        # Mongoengine field is the key, and the graphene fields is the values
        mongoengine_fields = {
            'StringField': graphene.String
        }

        model_fields = {
            field_name: object_dsc for field_name, object_dsc in mongo_model._fields.items()
            if not field_name.startswith('_')
        }

        for field_name, object_dsc in model_fields.items():
            # Group 1 is field name
            field = re.match(pattern, str(object_dsc))

            if field:
                field = field.group(1)

                if field in mongoengine_fields.keys():
                    setattr(cls, field_name, mongoengine_fields[field]())
