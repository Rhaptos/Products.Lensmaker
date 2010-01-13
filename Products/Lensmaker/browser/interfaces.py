from zope.interface import Interface
from zope.app.publisher.interfaces.browser import IBrowserView
from zope.app.event.interfaces import IObjectEvent
from zope.viewlet.interfaces import IViewletManager

class IMiscView(IBrowserView):
    """ 
    Miscellaneous views
    """

    def objectifyTagNamespaceList(self, li, lens_path=None, return_dictionary=False):
        """
        Take a list of the form ['Some_Prefix1::A1', 'Some_Prefix1::B1', 
        'Some_Prefix2:C1'] and return a list of dictionaries of the form
        (
            {'tagnamespace':<TagNamespace1>, 'tags':['A1 Alpha','B1 Beta']}, 
            {'tagnamespace':<TagNamespace2>, 'tags':['C1 Charlie']}
        ).

        If an object lookup via the prefix fails then that item is not 
        included in the result.
        """

    def getPrintableTags(self, tags, lens_path=None):
        """
        Transform a list of tags into a print friendly list.

        Eg. ['grade::2nd', 'grade::3rd', 'plain'] yields
        ['Grade:Second', 'Grade:3rd', 'plain'].
        """

    def getNamespaceTagTerm(self, prefix, tag):
        """
        Return the first word of tag
        """

    def getNamespaceTagLabel(self, tag):
        """
        Return all but the first word from tag
        """

    def getLensContentTypeBreakdown(self, results):
        """
        Return a breakdown of the types in a lens
        """

class IAfterTransitionEvent(IObjectEvent):
    """
    Event which signals that an transition has been performed on
    an object.

    This class will be made redundant as soon as DCWorkflow is upgraded
    to a sufficiently newer version.
    """
