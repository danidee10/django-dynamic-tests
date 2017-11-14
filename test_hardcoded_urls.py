"""
Check if templates contain hardcoded URL's

Django Templates shouldn't have hardcoded URL's in them
the static tag.
"""

from re import findall
from os import walk, path

from django.test import TestCase


HARDCODED_URLS_REGEX = r"<(link|script|img)+.*(href|src)+=[\"']((?!http|{|//)[^\s]+)[\"']"
EXCLUDED_FOLDERS = ['/node_modules', '/coverage']


class HardCodedURLTestCase(TestCase):
    """Test Case for Hardcoded URL's"""
    pass


def filter_templates(templates):
    """Remove templates in EXCLUDED_FOLDERS."""
    result = []

    for template in templates:
        if not any(folder in template for folder in EXCLUDED_FOLDERS):
            result.append(template)

    return result


def get_templates():
    """Walk the project root and return all templates."""
    templates = []

    for root, _, files in walk('.'):
        for file in files:
            if '.html' in file:
                templates.append(path.join(root, file))

    templates = filter_templates(templates)

    return templates


for template in get_templates():
    with open(template) as html_file:
        content = html_file.read()

        hardcoded_urls = findall(HARDCODED_URLS_REGEX, content)
        
        # get the third capturing group for all matches
        matches = [match[2] for match in hardcoded_urls]

        def test_func(self, matches=matches):
            """Test function that's dynamically injected to the test case."""
            self.assertEqual(len(matches), 0, matches)
        
        test_name = 'test_{}_has_no_hardcoded_urls'.format(template)
        test_doc = 'test that {} has no hardcoded urls'.format(template)

        test_func.__name__ = test_name
        test_func.__doc__ = test_doc

        setattr(HardCodedURLTestCase, test_name, test_func)
