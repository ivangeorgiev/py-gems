Packaging
=========


Get Metadata for Installed Package
----------------------------------

:mod:`os`

Starting Python 3.8 the :py:mod:`importlib.metadata` module could be used:

.. code-block:: python

    >>> from importlib import metadata
    >>> metadata.metadata('pygems')['Version']
    '0.2.0.dev3'

    >>> metadata.version('pygems')
    '0.2.0.dev3'

To see all available metadata elements: 

.. code-block:: python

    >>> metadata.metadata('pygems').keys()
    ['Metadata-Version', 'Name', 'Version', 'Summary', 'Home-page', 'License', 'Platform', 'Requires-Python', 'Description-Content-Type', 'License-File']

For earlier versions, use pkg_resources or ``pip``. Using ``pip`` is not recommended as 
it has no public API.

.. code-block:: python

    >>> from pkg_resources import get_distribution
    >>> pkg = get_distribution('pygems')
    >>> pkg.version
    '0.2.0.dev3'

