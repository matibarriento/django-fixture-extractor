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

* Add supported model fields
    * Many to Many
    * Many to Many with `through <https://docs.djangoproject.com/en/4.2/ref/models/fields/#django.db.models.ManyToManyField.through>`_ model
* Make more tests
* Add feature: Ofuscate value
* Add feature: Generate schema from model
* Fix tox and pyenv to work together

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

Credits
-------

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-djangopackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage
