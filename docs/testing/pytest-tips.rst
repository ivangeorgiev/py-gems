Pytest Tips
==============

Group test into categories with markers
--------------------------------------------

You can use `pytest markers <https://docs.pytest.org/en/6.2.x/example/markers.html>`_ to group tests into categories, 
e.g. unit, system, integration, etc.

You can mark tests, using ``pytest`` markers:

.. code-block:: python

    import pytest

    # With following we mark all the tests in this module with `all` mark
    pytestmark = [pytest.mark.all]

    @pytest.mark.unit
    def test_unit():
        assert True

    @pytest.mark.system
    def test_system():
        assert True

    @pytest.mark.integration
    def test_integration():
        assert True


Define markers in ``pytest.ini``:

.. code-block:: ini
   :caption: pytest.ini

   [pytest]
   markers =
       unit: mark test(s) as unit
       system: mark test(s) as system
       integration: mark test(s) as integration
       compat: compatibility test(s)
       all: all tests


To execute by default only unit tests, you can add to your ``pytest.ini``:

.. code-block:: ini
   :caption: pytest.ini

   [pytest]
   addopts = 
       -m "unit"

.. code-block:: bash

    $ pytest -vv

    testing/test_markers.py::test_unit PASSED                                       [100%] 

    ========================== 1 passed, 2 deselected in 0.09s =========================== 

To execute only system and integration tests:

.. prompt:: bash

    pytest -m "system or integration" -vv

    testing/test_markers.py::test_system PASSED                                     [ 50%] 
    testing/test_markers.py::test_integration PASSED                                [100%] 

    ========================== 2 passed, 1 deselected in 0.10s =========================== 

To execute tests marked with all:

.. prompt:: bash

    pytest -m "all" -vv

    testing/test_markers.py::test_unit PASSED                                       [ 33%] 
    testing/test_markers.py::test_system PASSED                                     [ 66%] 
    testing/test_markers.py::test_integration PASSED                                [100%] 

    ================================= 3 passed in 0.10s ==================================

You can also execute all tests by pasing empty argument to the markers expression:

.. prompt:: bash

    pytest -m "" -vv

    testing/test_markers.py::test_unit PASSED                                       [ 33%] 
    testing/test_markers.py::test_system PASSED                                     [ 66%] 
    testing/test_markers.py::test_integration PASSED                                [100%]

    ================================= 3 passed in 0.10s ==================================

Generate coverage report with every run
---------------------------------------

.. code-block:: ini
   :caption: Add pytest coverage options to pytest.ini 

   # pytest.ini
   [pytest]
   addopts = 
       --cov
       --cov-report=html
       --cov-report=term

``doctest``
-----------

Execute ``doctest`` tests with ``pytest``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. prompt:: bash

   pytest --doctest-modules

Pass fixtures to ``doctest``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``pytest`` provides a ``doctest_namespace`` fixture which could be used
to inject items into the namespace in which your doctests run.

The ``doctest_namespace`` fixture is a standard `dict` object. You can 
create an ``autouse`` fixture and inject necessary items from this fixture.

For more information, refer to the `doctest_namespace fixture`_ documentation.

For example:

.. code-block:: python

    import pytest

    @pytest.fixture(autouse=True)
        def add_np(doctest_namespace):
            doctest_namespace["username"] = 'John'

.. testsetup:: *

   username = 'John'

.. doctest::

   """
   Let's see what is our username:

   >>> username
   'John'

   """

.. Links
.. _doctest_namespace fixture: https://docs.pytest.org/en/6.2.x/doctest.html#doctest-namespace-fixture


