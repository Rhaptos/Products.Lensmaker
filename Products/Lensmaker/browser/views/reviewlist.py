from math import modf
from zope.interface import implements
from Acquisition import aq_inner
from RestrictedPython.Utilities import same_type, test
from Products.Five.browser import BrowserView
from Products.Lensmaker.browser.views.interfaces import IReviewList
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone import PloneMessageFactory as _
from Products.RhaptosModuleStorage.Extensions.DBModule import DBModuleSearch

class record(dict):
    def __setitem__(self, key, value):
        dict.__setitem__(self, key, value)
        setattr(self, key, value)

class ReviewList(BrowserView):
    implements(IReviewList)

    def modules(self):
        """
        Return all the SelectedContent items that can be
        approved by the authenticated member.

        The result is wrapped so that it can be used by the 
        reviewlist.pt template.
        """
        tool = getToolByName(self, 'lens_catalog')
        pms = getToolByName(self, 'portal_membership')
        member = pms.getAuthenticatedMember()

        # Find open Lenses auth member has reviewer role on
        brains = tool(
                portal_type='ContentSelectionLens',
                review_state=['published_open', 'private_open'],
                getReviewers=[member.getId()],
            )
        paths = [b.getPath() for b in brains]

        # Constrain search to the open lens paths
        brains = tool(
                portal_type='SelectedContent',
                getApproved=False,
                path=paths,
                sort_on='getRating',
                sort_order='descending',
            )

        # Wrap the brains, get rid of duplicates
        result = {}
        for b in brains:
            content = b.getObject().getContent()
            if content.portal_type not in ('Module', 'Collection'):
                continue
            r = record()
            r.objectId = content.contentId
            r.version = content.id
            result[(r.objectId, r.version)] = r

        result = result.values()
        result.sort(lambda x,y: cmp(x.objectId, y.objectId))
        return result

    def lenses(self, objectId=None):
        """
        Return the lenses that the context (ie. SelectedContent) belong
        to. If objectId is supplied then that is used to identify the
        SelectedContent.
        
        The SelectedContent must be endorsable for those lenses by
        the authenticated member.
        """
        context = aq_inner(self.context)
        tool = getToolByName(self, 'lens_catalog')
        pms = getToolByName(self, 'portal_membership')
        member = pms.getAuthenticatedMember()

        # Find paths that context.objectId is indexed for. Strip
        # each path to point to a parent.
        if objectId is not None:
            id = objectId
        else:
            id = context.objectId
        brains = tool(
                id=id,
                getApproved=False,
            )
        paths = ['/'.join(b.getPath().split('/')[:-1]) for b in brains]

        # Find open Lenses auth member has reviewer role on. Constrain 
        # path to paths obtained above.
        brains = tool(
                portal_type='ContentSelectionLens',
                review_state=['published_open', 'private_open'],
                getReviewers=[member.getId()],
                path=paths
            )

        return brains

    def approve(self, paths=[], REQUEST=None):
        """
        Approve Selected Content
        """
        context = aq_inner(self.context)
        portal = getToolByName(self, 'portal_url').getPortalObject()
        pms = getToolByName(self, 'portal_membership')
        member = pms.getAuthenticatedMember()
        count = 0
        for path in paths:
            item = portal.restrictedTraverse(path)
            item.edit(approved=True, approvedBy=member.getId())
            count += 1

        if REQUEST is not None:
            pu = getToolByName(self, 'plone_utils')
            pu.addPortalMessage(_('%d Items Approved' % count))
            REQUEST.RESPONSE.redirect(REQUEST.HTTP_REFERER)

    def same_type(self, arg1, *args):
        return same_type(arg1, *args)

    def test(self, *args):
        return test(*args)

    def modf(self, value):
        return modf(value)
