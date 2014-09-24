# encoding: utf-8

from jinja2.lexer import Lexer
from jinja2.environment import Environment
from gae_compressor.helpers import get_templates, CompressorBlock


class JinjaParser(object):
    @staticmethod
    def tokenize(content):
        """
        Returns a token stream
        """
        lexer = Lexer(Environment())
        return lexer.tokenize(content, None)

    def parse(self):
        """
        Returns a list of CompressorBlock() entities
        """
        blocks = []
        for template in get_templates():
            with open(template) as fp:
                content = fp.read()
            stream = self.tokenize(content)
            while not stream.eos:
                if stream.current.test('name:compress'):
                    block_type = stream.look().value
                    stream.skip(3)
                    block_content = stream.current.value
                    blocks.append(CompressorBlock(block_type, block_content))
                next(stream)
        return blocks