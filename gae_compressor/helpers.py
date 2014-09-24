# encoding: utf-8

import os
import re
import json
import fnmatch
import hashlib
import warnings

import settings


def get_manifest_filename():
    return getattr(settings, 'MANIFEST_FILE_NAME', None) or 'gae_compressor.json'


def get_manifest_path():
    return os.path.join(settings.PROJECT_ROOT, get_manifest_filename())


def get_compressed_dirname():
    """
    Returns the name of the directory where you store the compressed files
    """
    return getattr(settings, 'COMPRESSED_DIR_NAME', None) or 'compress'


def get_compressed_dir():
    return os.path.join(settings.STATIC_ROOT, get_compressed_dirname())


def hashed_content(original_content):
    """
    Returns hashed content
    """
    return hashlib.md5(original_content).hexdigest()


def get_staticfile_fullpath(link):
    """
    Make full path from 'link' attribute
    """
    return os.path.join(settings.STATIC_ROOT, link.replace(settings.STATIC_URL, ''))


def compressed_content(original_content, mode):
    """
    Returns a link to a compressed file if compression is enabled
    """
    if settings.COMPRESS_ENABLED:
        if not os.path.exists(get_manifest_path()):
            warnings.warn("gae_compressor is enabled, but manifest file not found. Run compress.py or set COMPRESS_ENABLED to False")
            return original_content

        with open(get_manifest_path()) as fp:
            manifest = json.loads(fp.read())

        link = manifest[hashed_content(original_content)]

        if mode == 'css':
            return '<link rel="stylesheet" href="{0}" type="text/css" />'.format(link)

        if mode == 'js':
            return '<script type="text/javascript" src="{0}"></script>'.format(link)


def get_templates():
    """
    Returns a list of all templates in project
    """
    for d in settings.TEMPLATE_DIRS:
        for root, dirnames, filenames in os.walk(d):
            for filename in fnmatch.filter(filenames, '*.html'):
                yield os.path.join(root, filename)


class CompressorBlock(object):
    def __init__(self, block_type, block_content):
        self.type = block_type
        self.content = block_content

    @property
    def links(self):
        """
        Returns a list of links to js and css files in block
        """
        attr = 'href' if self.type == 'css' else 'src'
        return [item for item in re.findall('{0}=[\'"]?([^\'" >]+)'.format(attr), self.content)]