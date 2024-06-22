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

TODO Features
-------------
* Make pipinstallable
* Run CI/CD

Desired features
----------------
* Add support for Django 1.11 to 5
* Add supported model fields
    * Many to Many with `through <https://docs.djangoproject.com/en/4.2/ref/models/fields/#django.db.models.ManyToManyField.through>`_ model
* Add feature: Obfuscate value
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
    pip install -r requirements/requirements_test.txt


How to add a new app and add tests
----------------------------------

1. Create the app

::

    $ cd tests/testproject
    $ python ../../manage.py startapp {APP_NAME}

2. Change the :code:`{APP_NAME}Config.name` inside the :code:`tests/{APP_NAME}/apps.py` file for :code:`tests.testproject.{APP_NAME}.apps.{APP_NAME}`
3. Add the app to the :code:`INSTALLED_APPS` in the :code:`/testproject/testproject/settings.py` file
4. Write the models that you would use to test on the model folder inside your app
5. Create the migrations using :code:`python manage.py makemigrations {APP_NAME}`
6. Run the migrations using :code:`python manage.py migrate`
7. Create the tests inside the :code:`tests/tests_orm_extractor.py` file

Credits
-------

Based on https://github.com/ascaliaio/django-dumpdata-one

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-djangopackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage

