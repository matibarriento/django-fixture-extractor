=============================
Django Fixtures Extractor
=============================

.. image:: https://badge.fury.io/py/django-fixtures-extractor.svg
    :target: https://badge.fury.io/py/django-fixtures-extractor

.. image:: https://travis-ci.org/matibarriento/django-fixtures-extractor.svg?branch=master
    :target: https://travis-ci.org/matibarriento/django-fixtures-extractor

.. image:: https://codecov.io/gh/matibarriento/django-fixtures-extractor/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/matibarriento/django-fixtures-extractor

Extract specific data to a django fixture

Documentation
-------------

The full documentation is at https://django-fixtures-extractor.readthedocs.io.

Quickstart
----------

Install Django Fixtures Extractor::

    pip install django-fixtures-extractor

Add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'fixtures_extractor',
        ...
    )

Features
--------

* Autocreate schema
* Make tests
* Ofuscate value
* Add supported model fields
* Fix tox and pyenv

Running Tests
-------------

Does the code actually work?

::

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ python runtests.py


Development commands
---------------------

::

    pip install -r requirements/requirements_dev.txt
    invoke -l


Credits
-------

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-djangopackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage
