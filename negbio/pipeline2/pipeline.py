import logging
from pathlib import Path

import bioc
import tqdm


class Pipe:
    """
    This class is not instantiated directly. Components inherit from it, and
    it defines the interface that components should follow to function as
    components in an NegBio analysis pipeline.
    """

    def __call__(self, doc: bioc.BioCDocument, *args, **kwargs):
        """
        Apply the pipe to one document. The document is modified in-place, and returned.
        """
        raise NotImplemented


class NegBioPipeline:
    def __init__(self, pipeline):
        self.pipeline = pipeline

    def __call__(self, doc, *args, **kwargs):
        for name, proc in self.pipeline:
            if not hasattr(proc, '__call__'):
                raise ValueError('{} has no __call__ function'.format(name))
            doc = proc(doc)
            if doc is None:
                raise ValueError('{} returns None'.format(name))
        return doc

    def scan(self, **kwargs):
        """
        Scan each document in a list of BioC source files, apply the pipeline, and print to directory.
        The output file names are directory/{stem}{suffix}

        Args:
            kwargs:
                source(list): a list of source pathnames
                directory(str): output directory
                suffix: suffix of output files
                verbose(boolean):
        """
        source = kwargs.pop('source')
        verbose = kwargs.pop('verbose', True)
        directory = Path(kwargs.pop('directory'))
        suffix = kwargs.pop('suffix')

        if not directory.exists():
            directory.mkdir(parents=True)

        for pathname in tqdm.tqdm(source, total=len(source), disable=not verbose):
            stem = Path(pathname).stem
            dstname = directory / '{}{}'.format(stem, suffix)
            try:
                with open(pathname, encoding='utf8') as fp:
                    collection = bioc.load(fp)
            except:
                logging.exception('Cannot read %s', pathname)
                continue

            new_documents = []
            for document in collection.documents:
                try:
                    document = self(document)
                except TypeError as e:
                    raise e
                except:
                    logging.exception('Cannot process %s', document.id)
                new_documents.append(document)
            collection.documents = new_documents

            try:
                with open(dstname, 'w', encoding='utf8') as fp:
                    bioc.dump(collection, fp)
            except:
                logging.exception('Cannot write %s', pathname)
