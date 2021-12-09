Plugins through Entry Points
============================

This approach is based on `Advertising Behavior`_ from `setuptools`_. A good example of 
this plug-in behavior can be seen in `pytest plugins`_, where ``pytest`` is a test framework 
that allows other libraries to extend or modify its functionality through the ``pytest11`` 
entry point.

Understanding the API
---------------------

Let's look at an example of listing the console script entry points for all
installed Python packages.

.. literalinclude:: scripts/plugin-entry-points/list_console_scripts.py

Functionality is provided by the ``entry_points()`` function from  `importlib.metadata library`_
introduced in Python 3.8.

The ``entry_points()`` function returns a collection of entry points. Entry points 
are represented by ``EntryPoint`` instances; each ``EntryPoint`` has a ``.name``, ``.group``, 
and ``.value`` attributes and a ``.load()`` method to resolve the value. There are also 
``.module``, ``.attr``, and ``.extras`` attributes for getting the components of the ``.value`` attribute.

For earlier versions of Python, you could use the ``pkg_resources`` package:

.. literalinclude:: scripts/plugin-entry-points/list_console_scripts_pkg_resources.py

Plugin Example
--------------

In this example we will create a script which can be extended via ``pygems.demoplugin`` plugins.

The plugin should register entry points in the ``pygems.demoplugin`` group:

.. code-block:: ini

    # setup.cfg

    [options.entry_points]
    pygems.demoplugin =
        hello-world = pygems.demo.helloworld:hi

Our sample plugin is doing simple print of the "Hi. It is me!" message to the console:

.. code-block:: python

    def hi():
        print("Hi. It is me!")

The application or script that needs to use the plugin filters the entry points by group, loads
the plugins and executes them.

.. literalinclude:: scripts/plugin-entry-points/demoplugin.py


.. _`Advertising Behavior`: https://setuptools.pypa.io/en/latest/userguide/entry_point.html#advertising-behavior
.. _`importlib.metadata library`: https://docs.python.org/3/library/importlib.metadata.html
.. _`pytest plugins`: https://docs.pytest.org/en/latest/writing_plugins.html
.. _`setuptools`: https://setuptools.pypa.io/en/latest/index.html

Conclusion
----------

Package entry points give us a mechanism for implementing plugin architecture
using loosely coupled plugins and consumers.

On the cons side the architecture depends on package entry points advertised by
setuptools. If the feature is dropped from Python, plugins will stop working.


