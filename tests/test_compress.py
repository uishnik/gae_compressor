# encoding: utf-8

import unittest

import os
import sys
import json
import shutil
from gae_compressor.compress import Compressor
from gae_compressor.helpers import get_manifest_path, get_compressed_dir
from django.template import Template, Context
import jinja2
from gae_compressor.jinja2_ext import CompressExtension

import settings


class CompressorTests(unittest.TestCase):
    def setUp(self):
        self.manifest_path = get_manifest_path()
        self.CLOSURE_COMPILER = settings.CLOSURE_COMPILER
        self.YUICOMPRESSOR = settings.YUICOMPRESSOR
        self.TEMPLATE_DIRS = settings.TEMPLATE_DIRS
        self.css_link = '<link rel="stylesheet" href="/static/compress/css/2616b6cbc87d.css" type="text/css" />'

    def tearDown(self):
        os.remove(self.manifest_path)
        shutil.rmtree(get_compressed_dir())
        settings.CLOSURE_COMPILER = self.CLOSURE_COMPILER
        settings.YUICOMPRESSOR = self.YUICOMPRESSOR
        settings.TEMPLATE_DIRS = self.TEMPLATE_DIRS

    def _test_compress(self, correct_manifest):
        Compressor().compress()
        self.manifest_path = get_manifest_path()
        with open(self.manifest_path) as f:
            manifest = json.loads(f.read())
        self.assertDictEqual(manifest, correct_manifest)

    def test_compress(self):
        self._test_compress({
            'c657e0028bb47d7274d16ca9be70382a': '/static/compress/css/2616b6cbc87d.css',
            '5afbdaecf57850fd9a9e78cb7076a4da': '/static/compress/js/72e49fd4b0e3.js'
        })

    def test_compress_without_compilers(self):
        del settings.CLOSURE_COMPILER, settings.YUICOMPRESSOR
        self._test_compress({
            'c657e0028bb47d7274d16ca9be70382a': '/static/compress/css/f5d934a5debd.css',
            '5afbdaecf57850fd9a9e78cb7076a4da': '/static/compress/js/283b93ba5a88.js'
        })

    def test_jinja2_ext_css(self):
        env = jinja2.Environment(extensions=[CompressExtension])
        Compressor().compress()
        template = env.from_string(open(os.path.join(settings.TEMPLATE_DIRS[0], 'index.html')).read())
        self.assertIn(self.css_link, template.render({}))

    def test_compress_css_templatetag(self):
        sys.path.append(settings.PROJECT_ROOT)
        setattr(settings, 'COMPRESSOR_ENGINE', 'Django')
        settings.SECRET_KEY = '123'
        settings.INSTALLED_APPS = ('gae_compressor',)
        settings.TEMPLATE_DIRS = (os.path.join(settings.PROJECT_ROOT, 'tests', 'templates_django'),)
        os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
        Compressor().compress()
        template = open(os.path.join(settings.TEMPLATE_DIRS[0], 'index.html')).read()
        context = Context({})
        template = Template(template)
        self.assertIn(self.css_link, template.render(context))


if __name__ == '__main__':
    unittest.main()