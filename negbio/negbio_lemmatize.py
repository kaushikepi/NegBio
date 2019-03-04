"""
Determines the lemma

Usage:
    negbio_pipeline lemmatize [options] --output=<directory> <file> ...

Options:
    --output=<directory>    Specify the output directory.
    --suffix=<suffix>       Append an additional SUFFIX to file names. [default: .ud.xml]
    --verbose               Print more information about progress.
"""
from negbio.cli_utils import parse_args
from negbio.pipeline.lemmatize import Lemmatizer
from negbio.pipeline.scan import scan_document

if __name__ == '__main__':
    argv = parse_args(__doc__)
    lemmatizer = Lemmatizer()
    scan_document(source=argv['<file>'], directory=argv['--output'], suffix=argv['--suffix'],
                  fn=lemmatizer.lemmatize_doc, non_sequences=[])
