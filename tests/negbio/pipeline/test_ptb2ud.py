from unittest import mock

from StanfordDependencies import StanfordDependencies

from negbio.pipeline.ptb2ud import NegBioPtb2DepConverter
from tests.negbio.utils import text_to_bioc


class TestNegBioPtb2DepConverter:
    def test_convert_doc(self):
        c = NegBioPtb2DepConverter()
        text = 'hello world!'
        tree = '(S1 (S (NP (NN hello) (NN world) (NN !))))'
        d = text_to_bioc([text], type='d/p/s')
        s = d.passages[0].sentences[0]
        s.infons['parse tree'] = tree
        d = c.convert_doc(d)
        s = d.passages[0].sentences[0]

        assert len(s.annotations) == 3, len(s.annotations)
        assert len(s.relations) == 2
        assert s.annotations[0].text == 'hello'
        assert s.annotations[0].infons['tag'] == 'NN'
        assert s.annotations[0].infons['lemma'] == 'hello'
        assert s.annotations[0].total_span.offset == 0

        assert s.annotations[1].text == 'world'
        assert s.annotations[1].infons['tag'] == 'NN'
        assert s.annotations[1].infons['lemma'] == 'world'
        assert s.annotations[1].total_span.offset == 6

        assert s.annotations[2].text == '!'
        assert s.annotations[2].infons['tag'] == 'NN'
        assert s.annotations[2].infons['lemma'] == '!'
        assert s.annotations[2].total_span.offset == 11

        assert s.relations[0].infons['dependency'] == 'nn'
        assert s.relations[0].nodes[0].refid == 'T0'
        assert s.relations[0].nodes[1].refid == 'T2'

        assert s.relations[1].infons['dependency'] == 'nn'
        assert s.relations[1].nodes[0].refid == 'T1'
        assert s.relations[1].nodes[1].refid == 'T2'


    def test_convert_doc_no_jpype(self):
        c = NegBioPtb2DepConverter()
        c._backend = 'subprocess'
        c._sd = StanfordDependencies.get_instance(backend=c._backend)
        text = 'hello world!'
        tree = '(S1 (S (NP (NN hello) (NN world) (NN !))))'
        d = text_to_bioc([text], type='d/p/s')
        s = d.passages[0].sentences[0]
        s.infons['parse tree'] = tree
        d = c.convert_doc(d)
        s = d.passages[0].sentences[0]
        assert 'lemma' not in s.annotations[1].infons

