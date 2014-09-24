from jinja2 import nodes
from jinja2.ext import Extension
from gae_compressor.helpers import compressed_content


class CompressExtension(Extension):
    tags = {'compress'}

    def __init__(self, environment):
        super(CompressExtension, self).__init__(environment)

    def parse(self, parser):
        lineno = parser.stream.next().lineno
        args = []
        mode = parser.parse_expression().name
        args.append(nodes.Const(mode))

        body = parser.parse_statements(['name:endcompress'], drop_needle=True)
        return nodes.CallBlock(self.call_method('_compress', args),
                               [], [], body).set_lineno(lineno)

    def _compress(self, mode, caller):
        """Helper callback."""
        original_content = caller()
        return compressed_content(original_content, mode) or original_content