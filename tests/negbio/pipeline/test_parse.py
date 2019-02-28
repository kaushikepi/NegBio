import pytest

from negbio.pipeline.parse import NegBioParser
from tests.negbio.test_utils import text_to_document_sentences

parser = NegBioParser()


def test_NegBioParser():
    text = 'hello world!'
    tree = '(S1 (S (NP (NN hello) (NN world) (NN !))))'
    t = parser.parse('hello world!')
    assert str(t) == tree

    document = text_to_document_sentences('id', [text])
    d = parser.parse_doc(document)
    assert d.passages[0].sentences[0].infons['parse tree'] == tree

    document = text_to_document_sentences('id', [''])
    d = parser.parse_doc(document)
    assert d.passages[0].sentences[0].infons['parse tree'] is None

    with pytest.raises(ValueError):
        parser.parse('')

    with pytest.raises(ValueError):
        parser.parse('\n')

    t = parser.parse(u'\xe6')
    assert str(t) == u'(S1 (S (NP (NN \xe6))))'
