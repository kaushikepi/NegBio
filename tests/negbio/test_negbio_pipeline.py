import tempfile
from pathlib import Path
from subprocess import call

import bioc
from bioc import biocitertools

from tests.negbio.utils import get_example_dir


def test_negbio_ssplit():
    source = get_example_dir() / '1.xml'
    output = Path(tempfile.mkdtemp())
    suffix = '.ssplit.xml'
    cmd = f'python negbio/negbio_ssplit.py ssplit --output={output} --suffix {suffix} {source}'
    call(cmd.split())
    with open(output / '1.ssplit.xml') as fp:
        actual = bioc.load(fp)
    with open(get_example_dir() / '1.ssplit.xml') as fp:
        expected = bioc.load(fp)

    for actual_sen, expected_sen in zip(biocitertools.sentences(actual),
                                        biocitertools.sentences(expected)):
        assert actual_sen.offset == expected_sen.offset


