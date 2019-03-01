import bioc


def text_to_bioc(list_of_text, type, **kwargs):
    if type == 'p/s':
        offset = 0
        passage = bioc.BioCPassage()
        passage.offset = offset
        for s in list_of_text:
            sentence = bioc.BioCSentence()
            sentence.offset = offset
            sentence.text = s
            offset += len(s) + 1
            passage.add_sentence(sentence)
        return passage
    elif type == 'd/p/s':
        document = bioc.BioCDocument()
        passage = text_to_bioc('p/s', list_of_text)
        document.add_passage(passage)
        return document
    elif type == 'c/d/p/s':
        c = bioc.BioCCollection()
        d = text_to_bioc(list_of_text, 'd/p/s')
        c.add_document(d)
        return c
    elif type == 'd/p':
        document = bioc.BioCDocument()
        offset = 0
        for s in list_of_text:
            passage = bioc.BioCPassage()
            passage.offset = offset
            offset += len(s) + 1
            passage.text = s
            document.add_passage(passage)
        return document
    elif type == 'c/d/p':
        c = bioc.BioCCollection()
        d = text_to_bioc(list_of_text, 'd/p')
        c.add_document(d)
        return c
    else:
        raise KeyError


def text_to_document_passages(id, passages):
    """
    Convert a list of text to a BioCDocument instance

    Args:
        id (str): BioCDocument id
        sentences (list): a list of passages

    Returns:
        BioCDocument: a BioCDocument instance
    """
    return text_to_bioc(passages, 'd/p')
