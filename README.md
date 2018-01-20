# django-dynamic-tests
django-dynamic-tests is a collection of tests that check Django templates for common errors and violation of best practices like hardcoding static URL's, missing staticfiles etc.

The tests use Regular expressions to extract information from the templates. These are then used to generate the tests dynamically.

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

### 3 test_hardcoded_urls.py
This generates tests to check if templates (links, scripts and images) have harcoded url's in them e.g 

`<img src="../static/frontend/image.jpg" />`. 

It's always better to use Django template tags to make the codebase more maintanable and make it easier to switch to a CDN for Serving Static files.

`<img src="{% static 'myapp/image.jpg' %}" />`

If you have a lot of relative links that you want to convert to use Django's `static` template tag. You can easily use ![Staticfy](https://github.com/danidee10/Staticfy) to achieve that.


## Configuration
A Sample `config.ini.sample` file is included alongside the tests, This file can be used to control the properties (Form/Static Assets) that are eventually tested.

You should use this file, when you have particular properties that you don't want to test E.g Production Version(s) of JavaScript files that are generated during your build/deploy process.
