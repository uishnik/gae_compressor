# encoding: utf-8

from django.template import Lexer
from gae_compressor.helpers import get_templates, CompressorBlock


class DjangoParser(object):
    TOKEN_TEXT = 0
    TOKEN_VAR = 1
    TOKEN_BLOCK = 2
    TOKEN_COMMENT = 3

    @staticmethod
    def tokenize():
        """
        Returns a stream of Django Token() entities
        """
        for template in get_templates():
            with open(template) as fp:
                template_content = fp.read()
            lexer = Lexer(template_content, None)
            for token in lexer.tokenize():
                yield token

    def parse(self):
        """
        Returns a list of CompressorBlock() entities
        """
        copy = False
        block_type = ''
        block_content = ''
        blocks = []
        for token in self.tokenize():
            if token.token_type == self.TOKEN_BLOCK and token.contents.split()[0] == 'compress':
                copy = True
                block_type = token.contents.split()[1]

            if token.token_type == self.TOKEN_BLOCK and token.contents == 'endcompress':
                copy = False

            if copy and token.token_type == self.TOKEN_TEXT:
                block_content += token.contents

            if block_content and not copy:
                block = CompressorBlock(block_type, block_content)
                blocks.append(block)
                block_content = ''

        return blocks