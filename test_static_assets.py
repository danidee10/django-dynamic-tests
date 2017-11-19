"""
Generate tests

To check if all application static assets (scripts, css and imagees)
are reachable
"""

import re
from os import walk, path
from configparser import ConfigParser

from django.test import TestCase
from django.contrib.staticfiles import finders

# Load Config file
CONFIG = ConfigParser()

PARENT_DIR = path.dirname(path.abspath(__file__))
CONFIG_FILE = path.join(PARENT_DIR, 'config.ini')
CONFIG.read(CONFIG_FILE)

ASSETS_REGEX = r"<(link|script|img)+.*(href|src)+=[\"']{% static [\"']([^\s\"']+)"

try:
    UNWANTED_ASSETS = CONFIG['Static Assets']['unwanted_assets'].split(',')
except KeyError:
    UNWANTED_ASSETS = []


class AssetsTestCase(TestCase):
    """
    TestCase to check if all static assets in the app are reachable.
    
    The Tests are dynamically generated and added to this class
    """
    pass


def remove_unwanted_assets(asset):
    """Filter out unwanted static files that shouldn't be checked."""

    return asset not in UNWANTED_ASSETS


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

        asset_links = re.findall(ASSETS_REGEX, content)

        # Get the Third group in each match
        asset_links = [asset_link[2] for asset_link in asset_links]

        # Remove static files that shouldn't be checked
        asset_links = list(filter(remove_unwanted_assets, asset_links))

        return {'static_assets': (asset_links,)}


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
                templates.append(path.join(root, file))

    return templates


def setup_tests():
    """Main method."""
    templates = get_templates()

    for template in templates:
        result = parse_templates(template)

        add_tests(template, **result)


setup_tests()
