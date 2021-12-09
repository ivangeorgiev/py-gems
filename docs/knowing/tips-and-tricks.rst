Tips and Tricks
================

Get nested attribute with dot notation
--------------------------------------

Interesting application for the ``reduce`` function is to access attribute of 
nested objects:

.. literalinclude:: scripts/get_attribute_deep_using_dot_notation_01.py

.. literalinclude:: scripts/get_attribute_deep_using_dot_notation_02.py

Now if we want to access the city of the user, we acually need to access the
``address`` of the user and than the ``city`` of the address. Expressed in dot notation we 
want to access ``address.city`` :

.. code-block:: pycon

    >>> address = Address('Sofia')
    >>> user = User('john', address)
    >>> print(get_attr(user, 'address.city'))
    Sofia

Trying to access missing attribute results in ``AttributeError`` error:

.. code-block:: pycon

    >>> address = Address('Sofia')
    >>> user = User('john', address)
    >>> print(get_attr(user, 'floor'))
    Traceback (most recent call last):
    ...
    AttributeError: 'Address' object has no attribute 'floor'

This function has been included in ``pygems.core.shortcuts`` module.
