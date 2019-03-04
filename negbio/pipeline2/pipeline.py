import bioc


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
