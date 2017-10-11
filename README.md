# django-dynamic-tests
Collection of tests to Analyze and test Django templates for common errors.

The tests use Regular expressions to extract information from the templates. These are then used to generate the tests dynamically.

I nearly named this repo **django-lint** but this is not a linter/lint-tool. Even though it analyzes your templates statically, It doesn't give you any hint/advice on how to fix your code.

The tests are written to be as general as possible, but if you have specific use cases you can tweak them to suit you. But they should work if they're dropped into any Django project that follows the "Django way" of doing things.

## Installation/Usage
Simply run at the root of your Django project

```bash
git clone git@github.com:danidee10/django-dynamic-tests.git tests
```

This would clone the repo to a new folder called tests. If you haven't done anything Special with the Django's Testfinder running

```python
python manage.py test
```

Should run the tests as part of your test suite(s).

### 1 test_error_fields.py
There is a whole medium article on why this was written https://medium.com/@osaetindaniel/using-dynamic-unit-tests-to-build-sane-django-forms-329d4b3b414d It Allows you to check the forms for missing error fields.

### 2 test_static_assets.py
This test allows you to test links to static files in your templates to see if they're reachable. It uses

**django.contrib.staticfiles import finders** https://docs.djangoproject.com/en/1.11/ref/contrib/staticfiles/

To locate static files on the disk, without making a http request. This Speeds up the tests significantly.


## Configuration
A Sample `config.ini.sample` file is included alongside the tests, This file can be used to control the properties (Form/Static Assets) that are eventually tested.

You should use this file, when you have particular properties that you don't want to test E.g Production Version(s) of JavaScript files that are generated during your build/deploy process.
