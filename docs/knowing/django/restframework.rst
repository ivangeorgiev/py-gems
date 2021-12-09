Django Rest Framework (DRF)
===========================

.. contents:: Table of Contents

Serialize / Deserialize
-----------------------

Remove Fields from Serializer Output
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

There are cases when we need to remove one or more fields from Django Rest Framework serializer's 
output. For example:

- Remove personal information for users without AuthorizationError
- Feature toggles - we want certain information to be available in the 
  output based on a feature toggle (flag).

Override the default ``to_representation`` method to drop the field from
the output:

.. code-block:: python

   class UserSerializer(serializers.ModelSerializer):
       class Meta:
           model = User

       def to_representation(self, instance):
           representation = super().to_representation(instance)
           representation.pop('salary')
           return representation

In this example, the ``salary`` field is removed from the serializer
output.

The behavior could be extracted into a function:

.. code-block:: python

    def drop_fields(representation:dict, fields, error_handler=None):
        """Drop a one or more fields from serializer representation"""
        fields = (fields,) if type(fields) == str else fields
        for field_name in fields:
            try:
                representation.pop(field_name)
            except Exception as error:
                if error_handler:
                    error_handler(error)
                else:
                    raise
        return representation

Using the function our class becomes:

.. code-block:: python

    class UserSerializer(serializers.ModelSerializer):
        class Meta:
            model = User

        def to_representation(self, instance):
            representation = drop_fields(super().to_representation(instance), 'salary')
            return representation

In case field is already missing in the output, ``KeyError`` will be raised. 
This might not be the desired behavior. We might want to ignore missing fields.
For such situations we have provided the ``error_handler`` argument for the 
`drop_fields` function.

.. code-block:: python

    def ignore_errors(errors:list):
        def error_handler(error:Exception):
            """If error is instance of given classes ignore it or raise the error otherwise"""
            if not isinstance(error, errors):
                raise error
        return error_handler

    class UserSerializer(serializers.ModelSerializer):
        class Meta:
            model = User

        def to_representation(self, instance):
            representation = drop_fields(
                super().to_representation(instance),
                'salary', 
                ignore_errors(KeyError),
            )
            return representation

Both functions has been added to the :mod:`pygems.core.shortcuts` module.

