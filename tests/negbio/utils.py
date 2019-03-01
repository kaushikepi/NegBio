import bioc


def text_to_document_sentences(id, sentences):
    """
    Convert a list of text to a BioCDocument instance

    Args:
        id (str): BioCDocument id
        sentences (list): a list of sentences

    Returns:
        BioCDocument: a BioCDocument instance
    """
    document = bioc.BioCDocument()
    document.id = id

    offset = 0
    passage = bioc.BioCPassage()
    passage.offset = offset

    for s in sentences:
        sentence = bioc.BioCSentence()
        sentence.offset = offset
        sentence.text = s
        offset += len(s) + 1
        passage.add_sentence(sentence)

    document.add_passage(passage)
    return document


def text_to_document_passages(id, passages):
    """
        Convert a list of text to a BioCDocument instance

        Args:
            id (str): BioCDocument id
            sentences (list): a list of passages

        Returns:
            BioCDocument: a BioCDocument instance
        """
    document = bioc.BioCDocument()
    document.id = id

    offset = 0
    for s in passages:
        passage = bioc.BioCPassage()
        passage.offset = offset
        offset += len(s) + 1
        passage.text = s
        document.add_passage(passage)
    return document
