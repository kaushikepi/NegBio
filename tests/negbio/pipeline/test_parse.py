import sys

import pytest

from negbio.pipeline.parse import NegBioParser
from tests.negbio.utils import text_to_bioc


parser = None
if parser is None:
    parser = NegBioParser()


class TestNegBioParser:
    def test_parse(self):
        tree = '(S1 (S (NP (NN hello) (NN world) (NN !))))'
        t = parser.parse('hello world!')
        assert str(t) == tree

        with pytest.raises(ValueError):
            parser.parse('')

        with pytest.raises(ValueError):
            parser.parse('\n')

        if sys.version_info[0] == 2:
            with pytest.raises(ValueError):
                parser.parse(u'\xe6')
        else:
            t = parser.parse(u'\xe6')
            assert str(t) == u'(S1 (S (NP (NN \xe6))))'

    def test_parse_doc(self):
        text = 'hello world!'
        tree = '(S1 (S (NP (NN hello) (NN world) (NN !))))'
        document = text_to_bioc([text], type='d/p/s')
        d = parser.parse_doc(document)
        assert d.passages[0].sentences[0].infons['parse tree'] == tree

        document = text_to_bioc([''], type='d/p/s')
        d = parser.parse_doc(document)
        assert d.passages[0].sentences[0].infons['parse tree'] is None
