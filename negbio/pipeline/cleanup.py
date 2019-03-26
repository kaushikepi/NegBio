import warnings


def clean_sentences(document, sort_anns=False):
    """
    Remove sentences in each passage

    Args:
        document(BioCDocument): a document
        sort_anns(bool): sort ann by its location
    """
    warnings.warn("use pipeline2 instead", PendingDeprecationWarning)
    for passage in document.passages:
        del passage.sentences[:]

    if sort_anns:
        key_func = lambda ann: ann.total_span.offset
        id = 0
        for passage in document.passages:
            passage.annotations = sorted(passage.annotations, key=key_func)
            for ann in passage.annotations:
                ann.id = str(id)
                id += 1
    return document
