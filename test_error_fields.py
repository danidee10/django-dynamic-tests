"""
Generates tests

to check all forms/fields in a template for corresponding error messages.
"""

import re
from os import walk
from os.path import dirname, abspath, join
from configparser import ConfigParser

from django.test import TestCase


# Load Config file
config = ConfigParser()

parent_dir = dirname(abspath(__file__))
config_file = join(parent_dir, 'config.ini')
config.read(config_file)

# Compile Regexes
FIELD_REGEX = re.compile(
    r"{[{%]\s*.*\b(\w*form(?!set|.non_field_errors)\w*\.\w+)[|\w:\s'\"-]*\s*[%}]}"
    )
ERROR_REGEX = re.compile(r'{{\s*(.*form\w*\.\w+\.errors)\s*}}')
FORMS_REGEX = re.compile(r"{[{%]\s*.*\b(\w*form(?!set)\w*)\.\w+\s*[%}]}")
NON_FIELD_ERROR_REGEX = re.compile(r'{{\s*(.*form\w*\.non_field_errors)\s*}}')

try:
    UNWANTED_FIELDS = config['Form Fields']['unwanted_fields'].split(',')
except KeyError:
    UNWANTED_FIELDS = []


class FormTestCase(TestCase):
    """Test case to check templates for missing error fields."""
    pass


def remove_unwanted_fields(field):
    """Filter out unwanted fields."""

    return field not in UNWANTED_FIELDS


def build_test(form_attr, error_attrs, error_str, file_path):
    """
    Build dynamic tests for each form/field.

    file_path is appended to the test name to make it unique,
    without that some tests would be overwritten when we call setattr
    """
    form_error_attr = '{}.{}'.format(form_attr, error_str)
    test_name = 'test_{}_{}'.format(form_error_attr, file_path)

    def test_func(self):
        self.assertIn(form_error_attr, error_attrs, file_path)

    test_func.__name__ = test_name
    test_func.__doc__ = 'Test that {} has an error message.'.format(form_attr)

    return test_func, test_name


def parse_templates(file_path):
    """
    Use Regular expressions to extract the forms/fields we're interested in.

    Returns a dictionary with the error attribute as the key.
    """
    with open(file_path) as html_file:
        content = html_file.read()

        # normal fields e.g {{ form.password }}
        fields = set(re.findall(FIELD_REGEX, content))
        fields = filter(remove_unwanted_fields, fields)
        error_fields = re.findall(ERROR_REGEX, content)

        # non-field errors for forms
        forms = set(re.findall(FORMS_REGEX, content))
        forms = filter(remove_unwanted_fields, forms)
        non_field_errors = re.findall(NON_FIELD_ERROR_REGEX, content)

        return {
            'errors': [fields, error_fields],
            'non_field_errors': [forms, non_field_errors]
            }


def add_tests(template, **kwargs):
    """Dynamically add tests for each form/field."""

    for key, value in kwargs.items():
        for field in value[0]:
            test_func, test_name = build_test(
                field, value[1], key, template
            )

            setattr(FormTestCase, test_name, test_func)


def get_templates():
    """Walk the project root and return all templates."""
    templates = []

    for root, _, files in walk('.'):
        for file in files:
            if '.html' in file:
                templates.append(join(root, file))

    return templates


def setup_tests():
    """Main method."""
    templates = get_templates()

    for template in templates:
        result = parse_templates(template)

        add_tests(template, **result)


setup_tests()
