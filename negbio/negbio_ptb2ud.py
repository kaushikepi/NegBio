"""
Convert from parse tree to universal dependencies

Usage:
    negbio_pipeline ptb2ud [options] --output=<directory> <file> ...

Options:
    --output=<directory>    Specify the output directory.
    --suffix=<suffix>       Append an additional SUFFIX to file names. [default: .ud.xml]
    --verbose               Print more information about progress.
    --workers=<n>           Number of threads [default: 1]
    --files_per_worker=<n>  Number of input files per worker [default: 8]
"""
from negbio.cli_utils import parse_args, calls_asynchronously
from negbio.pipeline.ptb2ud import NegBioPtb2DepConverter
from negbio.pipeline.scan import scan_document


if __name__ == '__main__':
    argv = parse_args(__doc__)
    workers = int(argv['--workers'])
    if workers == 1:
        ptb2dep = NegBioPtb2DepConverter(universal=True)
        scan_document(source=argv['<file>'], directory=argv['--output'], suffix=argv['--suffix'],
                      fn=ptb2dep.convert_doc, non_sequences=[])
    else:
        calls_asynchronously(argv, 'python -m negbio.negbio_ptb2ud ptb2ud')