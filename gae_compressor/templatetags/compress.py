# encoding: utf-8

from django import template
from gae_compressor.helpers import compressed_content


register = template.Library()


class CompressNode(template.Node):
    def __init__(self, nodelist, mode):
        self.nodelist = nodelist
        self.mode = mode

    def render(self, context):
        original_content = self.nodelist.render(context)
        return compressed_content(original_content, self.mode) or original_content


def do_compress(parser, token):
    nodelist = parser.parse(('endcompress',))
    parser.delete_first_token()
    mode = token.contents.split(None, 1)[1]
    return CompressNode(nodelist, mode)

do_compress = register.tag("compress", do_compress)