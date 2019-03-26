import logging
import os
from pathlib import Path

import bioc
import tqdm
from filelock import FileLock


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
                skip_exists: if the output file exists, do not process the file
        """
        source = kwargs.pop('source')
        verbose = kwargs.pop('verbose', True)
        directory = Path(kwargs.pop('directory'))
        suffix = kwargs.pop('suffix')
        skip_exists = kwargs.pop('skip_exists', False)

        if not directory.exists():
            directory.mkdir(parents=True)

        for pathname in tqdm.tqdm(source, total=len(source), disable=not verbose, unit='col'):
            stem = Path(pathname).stem
            dstname = directory / '{}{}'.format(stem, suffix)

            if skip_exists:
                if dstname.exists():
                    continue

            if os.path.splitext(pathname)[1] != '.xml':
                logging.exception('Filename must end with .xml: %s', pathname)
                continue

            # add file lock
            lckname = dstname.with_suffix('.lck')
            if lckname.exists():
                logging.warning('Skip %s because of the lock file', pathname)
                continue

            with open(lckname, 'w') as _:
                pass

            try:
                with open(pathname, encoding='utf8') as fp:
                    collection = bioc.load(fp)
            except:
                logging.exception('Cannot read %s', pathname)
                os.remove(lckname)
                continue

            new_documents = []
            for document in tqdm.tqdm(collection.documents, unit='doc', disable=not verbose,
                                      leave=False):
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
            finally:
                os.remove(lckname)
