"""
events.py - lensmaker event handlers.

Author: Hedley Roos (hedley@upfrontsystems.co.za)
Copyright (C) 2007 Rice University. All rights reserved.

This software is subject to the provisions of the GNU Lesser General
Public License Version 2.1 (LGPL).  See LICENSE.txt for details.
"""

from zope.interface import implements
from DateTime import DateTime

from Products.CMFCore.utils import getToolByName
from Products.ATContentTypes.content.folder import ATFolder

from browser.interfaces import IAfterTransitionEvent

class AfterTransitionEvent(object):
    """
    Trivial implementation of the interface
    """
    implements(IAfterTransitionEvent)

    def __init__(self, ob):
        self.object = ob

def onContentSelectionLensModified(context, event):
    """
    Create Tag Namespaces folder if lens is an open lens

    params:
        context - the lens that has been modified
        event - not used but required by API

    return:
        None
    """
    if context.isTemporary():
        return
    id = 'tag-namespaces'
    if id not in context.objectIds():
        obj = ATFolder(id)
        # Create these attributes to work around a Plone indexing bug
        obj.start = DateTime()
        obj.end = DateTime()
        context._setObject(id, obj)
        obj = context._getOb(id)
        obj.setTitle("Tag vocabularies")
        obj.reindexObject()
        obj.notifyWorkflowCreated()

        # Constrain allowed types
        obj.setConstrainTypesMode(1)
        obj.setLocallyAllowedTypes(['TagNamespace'])

        # Set a template as default view
        obj.setLayout('lens_tagnamespaces_default_view')

def onModuleRated(context, event):
    """
    Reindex all SelectedContent that wrap the rated module
    """
    portal = getToolByName(context, 'portal_url').getPortalObject()
    module = context
    rating = module.rating()
    tool = getToolByName(context, 'lens_catalog')
    for brain in tool(id=module.id):
        obj = portal.unrestrictedTraverse(brain.getPath())
        tool.catalog_object(obj, idxs=['getRating'])
