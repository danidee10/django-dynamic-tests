"""
Generate tests

To check if all application static assets are reachable
"""

import re
from os import walk, chdir
from os.path import dirname, abspath, join
from configparser import ConfigParser

from django.test import TestCase
from django.contrib.staticfiles import finders

# Load Config file
config = ConfigParser()

parent_dir = dirname(abspath(__file__))
config_file = join(parent_dir, 'config.ini')
config.read(config_file)

SCRIPTS_REGEX = r"<script.*src=[\"']{% static [\"'](.*)[\"'] %}\".*</script>"
LINKS_REGEX = r"<link.*href=[\"']{% static [\"'](.*)[\"'] %}[\"']"

try:
    UNWANTED_ASSETS = config['Static Assets']['unwanted_assets'].split(',')
except KeyError:
    UNWANTED_ASSETS = []


class AssetsTestCase(TestCase):
    """TestCase to check if all static assets in the app are reachable."""
    pass


def remove_unwanted_assets(field):
    """Filter out unwanted static files that shouldn't be checked."""

    return field not in UNWANTED_ASSETS


def build_test(asset, file_path):
    """
    Build dynamic tests for each script/link.

    file_path is appended to the test name to make it unique,
    without that some tests would be overwritten when we call setattr
    """
    test_name = 'test_{}_{}'.format(asset, file_path)

    def test_func(self):
        path = finders.find(asset)
        self.assertNotEqual(path, None)

    test_func.__name__ = test_name
    test_func.__doc__ = 'Test that {} is reachable.'.format(asset)

    return test_func, test_name


def parse_templates(file_path):
    """
    Use Regular expressions to extract the scripts/links we're interested in.

    Returns a dictionary with the error attribute as the key.
    """
    with open(file_path) as html_file:
        content = html_file.read()

        app_scripts = re.findall(SCRIPTS_REGEX, content)
        app_links = re.findall(LINKS_REGEX, content)

        # Remove static files that shouldn't be checked
        app_scripts = filter(remove_unwanted_assets, app_scripts)
        app_links = filter(remove_unwanted_assets, app_links)

        return {
            'scripts': (app_scripts,),
            'links': (app_links,)
            }


def add_tests(template, **kwargs):
    """Dynamically add tests for each form/field."""

    for _, value in kwargs.items():
        for asset in value[0]:
            test_func, test_name = build_test(asset, template)

            setattr(AssetsTestCase, test_name, test_func)


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
