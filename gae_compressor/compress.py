# encoding: utf-8

import json
import re
import os
from os.path import join, exists
from subprocess import Popen, PIPE
from helpers import get_manifest_path, get_compressed_dirname, get_compressed_dir, get_staticfile_fullpath,\
    hashed_content

import settings
import warnings


class Compressor(object):
    def __init__(self):
        self.compressed_dir = get_compressed_dir()
        for item in ('css', 'js'):
            d = join(self.compressed_dir, item)
            if not exists(d):
                os.makedirs(d)

        self.compressors = {}
        yuicompressor = getattr(settings, 'YUICOMPRESSOR', None)
        if yuicompressor:
            self.check_path(yuicompressor)
            self.compressors['css'] = ['java', '-jar', yuicompressor, '--type', 'css']

        closure_compiler = getattr(settings, 'CLOSURE_COMPILER', None)
        if closure_compiler:
            self.check_path(closure_compiler)
            self.compressors['js'] = ['java', '-jar', closure_compiler]

    @staticmethod
    def check_path(p):
        if not exists(p):
            raise OSError(2, 'No such file or directory: ' + p)

    @staticmethod
    def get_united_content(links):
        """
        Gets links to js or css files and return united js or css content
        """
        content = ''
        for link in links:
            with open(get_staticfile_fullpath(link)) as f:
                data = f.read() + '\n'
            content += data
        return content

    @staticmethod
    def _converter(match):
        url = match.group(1).strip(' \'"')
        fullpath = get_staticfile_fullpath(url)

        if not exists(fullpath):
            return "url('{url}')".format(url=url)

        with open(fullpath) as f:
            return "url('{url}?{hash}')".format(url=url, hash=hashed_content(f.read())[:12])

    def add_hash_to_urls(self, content):
        p = re.compile(r'url\(([^\)]+)\)')
        return p.sub(self._converter, content)

    def compress_content(self, content, content_type):
        """
        Returns compressed content
        """
        proc = Popen(self.compressors[content_type], stdout=PIPE, stderr=PIPE, stdin=PIPE)
        stdout, stderr = proc.communicate(input=content)
        if proc.returncode != 0:
            warnings.warn('Failed to compress. File will be copied untouched.\n' + stderr)
            return content
        return stdout

    @staticmethod
    def save_file(filename, content):
        with open(filename, 'w') as fp:
            fp.write(content)

    @staticmethod
    def get_parser():
        engine = getattr(settings, 'COMPRESSOR_ENGINE', None) or 'Jinja2'
        if engine == 'Django':
            from gae_compressor.parsers.django_parser import DjangoParser
            return DjangoParser()
        elif engine == 'Jinja2':
            from gae_compressor.parsers.jinja_parser import JinjaParser
            return JinjaParser()
        else:
            raise Exception('Invalid COMPRESSOR_ENGINE')

    def compress(self):
        """
        Compress all blocks and create manifest file
        """
        manifest = {}
        parser = self.get_parser()
        for block in parser.parse():
            content = self.get_united_content(block.links)

            if block.type == 'css':
                content = self.add_hash_to_urls(content)

            if self.compressors.get(block.type):
                content = self.compress_content(content, block.type)

            filename = hashed_content(content)[:12] + '.' + block.type
            fullname = join(self.compressed_dir, block.type, filename)
            self.save_file(fullname, content)

            manifest_key = hashed_content(block.content)
            compressed_link = join(settings.STATIC_URL, get_compressed_dirname(), block.type, filename)
            manifest[manifest_key] = compressed_link
            self.save_file(get_manifest_path(), json.dumps(manifest, indent=4))


if __name__ == '__main__':
    if settings.COMPRESS_ENABLED:
        Compressor().compress()
        print 'Compression completed'
    else:
        print 'Compressor is disabled'