import networkx as nx
from negbio import ngrex
import pytest


def get_graph():
    G = nx.DiGraph()
    G.add_node('xxx', attr_dict={'lemma': 'xxx'})
    G.add_node('yyy', attr_dict={'lemma': 'yyy'})
    G.add_node('zzz', attr_dict={'lemma': 'zzz'})
    G.add_edge('xxx', 'yyy', attr_dict={'dependency': 'aaa'})
    G.add_edge('yyy', 'zzz', attr_dict={'dependency': 'bbb'})
    G.add_edge('xxx', 'zzz', attr_dict={'dependency': 'ccc'})
    return G


def _helper(G, p, expected):
    pattern = ngrex.compile(p)
    actual = set()
    for m in pattern.finditer(G):
        actual.add(m.group(0))
    assert actual == expected, '{} vs {}'.format(actual, expected)


def test_regex():
    G = get_graph()
    _helper(G, '{} >{dependency:/aaa|bbb/} {}', {'xxx', 'yyy'})


def test_attribute():
    G = get_graph()
    _helper(G, '{} >{dependency:/aaa|bbb/} {}', {'xxx', 'yyy'})
    _helper(G, '{} >{tag:/aaa|bbb/} {}', set())


def test_relation():
    G = get_graph()
    _helper(G, '{lemma:/xxx/} >{dependency:/aaa/} {lemma:/yyy/}', {'xxx'})
    _helper(G, '{lemma:/yyy/} <{dependency:/aaa/} {lemma:/xxx/}', {'yyy'})
    _helper(G, '{} >{} {}', {'xxx', 'yyy'})


def test_relation_next():
    G = get_graph()
    _helper(G,
           '{lemma:/xxx/} >{dependency:/aaa/} ({lemma:/yyy/} >{dependency:/bbb/} {lemma:/zzz/})',
            {'xxx'})


def test_relation_conj():
    G = get_graph()
    _helper(G, '{} >{} {lemma:/yyy/} >{} {lemma:/zzz/}', {'xxx'})
    _helper(G, '{} >{} {lemma:/yyy/} <{} {lemma:/zzz/}', set())


def test_relation_disj():
    G = get_graph()
    _helper(G, '{} >{dependency:/aaa/} {} | >{dependency:/bbb/} {}', {'xxx', 'yyy'})


def test_names():
    G = get_graph()
    pattern = ngrex.compile('{}=t >{dependency:/aaa|bbb/} {}')
    actual = {m.get('t') for m in pattern.finditer(G)}
    assert actual == {'xxx', 'yyy'}

    with pytest.raises(KeyError):
        pattern = ngrex.compile('{}=t >{dependency:/aaa|bbb/} {}')
        m = next(pattern.finditer(G))
        m.get('x')


def test_MatcherObj():
    G = get_graph()
    pattern = ngrex.compile('{lemma:/xxx/} >{dependency:/aaa/} {lemma:/yyy/}')
    matcher = next(pattern.finditer(G))
    assert bool(matcher)
    assert matcher.graph == G
    assert matcher.pattern == pattern
    groups = list(matcher.groups())
    assert len(groups) == 2
    assert groups[0] == 'xxx'
    assert groups[1] == 'yyy'


def test_validate_names():
    with pytest.raises(KeyError):
        ngrex.compile('{}=t >{dependency:/aaa|bbb/} {}=t')
