# encoding: utf-8

from os.path import join, dirname


PROJECT_ROOT = dirname(__file__)
TEMPLATE_DIRS = (
    join(PROJECT_ROOT, 'tests', 'templates_jinja2'),
)
STATIC_ROOT = join(PROJECT_ROOT, 'tests', 'static')
STATIC_URL = '/static/'

YUICOMPRESSOR = join(PROJECT_ROOT, 'tests', 'compressors', 'yuicompressor-2.4.8.jar')
CLOSURE_COMPILER = join(PROJECT_ROOT, 'tests', 'compressors', 'closure_compiler_20131014.jar')

# COMPRESSED_DIR_NAME = 'compress'
# MANIFEST_FILE_NAME = 'gae_compressor.json'
# COMPRESSOR_ENGINE = 'Django'

COMPRESS_ENABLED = True