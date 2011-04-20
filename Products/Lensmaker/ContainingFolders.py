"""
Simple AT content types, mostly made to allow us to control their view actions.

Author: J. Cameron Cooper (jccooper@rice.edu)
Copyright (C) 2007 Rice University. All rights reserved.

This software is subject to the provisions of the GNU Lesser General
Public License Version 2.1 (LGPL).  See LICENSE.txt for details.
"""
import AccessControl

from Products.CMFCore.utils import getToolByName
from Products.CMFCore.permissions import View, ModifyPortalContent
from Products.CMFCore.Expression import Expression

from Products.Archetypes.public import Schema
from Products.Archetypes.public import registerType
from Products.Archetypes.public import BaseFolder, BaseFolderSchema
from Products.Archetypes.public import BaseBTreeFolder, BaseBTreeFolderSchema
from Products.Archetypes.public import StringField, SelectionWidget

from xml.dom import minidom

from Products.Lensmaker.domTools import *
from OFS.ObjectManager import ObjectManager
from DateTime import DateTime

from config import LENS_TYPES_OR_NONE, NO_CAT_TOKEN

category = StringField('category',
                          required=0, # '' should be accepted, but won't if this is true, even when in vocab
                          searchable=0,
                          #index=":brains",
                          vocabulary=LENS_TYPES_OR_NONE,
                          enforceVocabulary=1,
                          default = NO_CAT_TOKEN,
                          widget=SelectionWidget(label="Restrict to category",
                                              description="If set to a particular category, display only such lenses.",
                                              i18n_domain="rhaptos"),
                         )

schema = BaseBTreeFolderSchema + Schema((category,))

class LensMajorContainer(BaseBTreeFolder):
    """Simple folder to contain all member-named lens folders.
    This probably wouldn't have been necessary in Plone 2.5, where we could just have used the 'layout'.
    """
    archetype_name = "Lens Major Container"
    use_folder_tabs = 0
    allowed_content_types = ['LensFolder']

    schema = schema
    
    security = AccessControl.ClassSecurityInfo()
    
    actions = (
               {'id': 'view',
                'title': 'View',
                'action': Expression('string:${object_url}/lenses_listing'),
                'permissions': (View,),
                'visible': 0},
               {'id': 'metadata',  # turn off 'properties' tab
	        'visible': 0},
	      )

    # A PUT on the Major folder is intentionally a no-op
    security.declareProtected(ModifyPortalContent, 'PUT')
    def PUT(self, REQUEST):
        return
        
    def getFeedData(self):
        fieldDict = {'author':'Various','title':'All Lenses in the ' + str(self.portal_url.getPortalObject().Title()) + ' System','id':'Lenses','lastUpdated':'','lenses':[]}
        fieldDict['lastUpdated'] = self.ModificationDate()
        #loop through lenses and add to list
        category = self.getCategory()
        
        if category == 'Endorsement':
            fieldDict['title'] = "Endorsed Lenses in the " + str(self.portal_url.getPortalObject().Title()) + " System"
        elif category == 'Affiliation':
            fieldDict['title'] = "Affiliated Lenses in the " + str(self.portal_url.getPortalObject().Title()) + " System"
        elif category == 'List':
            fieldDict['title'] = "Member List Lenses in the " + str(self.portal_url.getPortalObject().Title()) + " System"
        lensList = self.lens_tool.getListsBy(category, incl_organised=True)
        for lens in lensList:
            if lens.review_state != 'private':
                lensDict = {}
                lensDict['author'] = lens.getCreatorName
                lensDict['title'] = lens.Title
                lensDict['category'] = lens.getCategory
                lensDict['id'] = lens.getId
                lensDict['lastModified'] = lens.ModificationDate()
                if lens.hasLogo:
                    lensDict['logoURL'] = str(lens.getURL()) + '/logo_thumb'
                else:
                    lensDict['logoURL'] = ''
                lensDict['lensBy'] = lens.getCreatorName
                lensDict['count'] = lens.getCount
                lensDict['feedURL'] = str(lens.getURL()) + '/atom'
                lensDict['lensURL'] = str(lens.getURL())
                fieldDict['lenses'].append(lensDict)
        return fieldDict
            
            

registerType(LensMajorContainer, 'Lensmaker')

from Acquisition import ImplicitAcquisitionWrapper, aq_base, aq_inner

class LensRedirectContainer(LensMajorContainer):
    """Like a Major Container, but looks for its contents in the real one.
    """
    archetype_name = "Lens Redirect Container"
    allowed_content_types = ()
    
    security = AccessControl.ClassSecurityInfo()
    
    def __bobo_traverse__(self, request, key):
        """If we find child objects in the real lenses folder, return those instead.
        Ideally, I'd like to make them think they were in this folder, but I can't seem to figure out how.
        Instead, push the category value into the request, where the dispatcher script can look.
        """
        stack = request.get('TraversalRequestNameStack')
        lens_tool = getToolByName(self, 'lens_tool')
        canonical = lens_tool.getMajorContainer()

        # first getattr is just a test (which should not be wrapped, acquisition being too broad),
        # second is actual object (which must be wrapped, or else later acquisition fails)
        userfolder = getattr(canonical.aq_base, key, None) and getattr(canonical, key, None)

        if userfolder:
            if type(request) != dict:   # a dict when key is template, and we don't want to get normal lenses_listing
                request.set('getCategory', self.getCategory())
                return userfolder
        return LensMajorContainer.__bobo_traverse__(self, request, key) # uses Five; getattr(self, key, None) doesn't work anymore

    # A PUT on the folder is intentionally a no-op
    security.declareProtected(ModifyPortalContent, 'PUT')
    def PUT(self, REQUEST):
        return

registerType(LensRedirectContainer, 'Lensmaker')


schema = BaseBTreeFolderSchema.copy()

class LensFolder(BaseFolder, ObjectManager):
    """Simple folder to contain a member's lenses.
    """
    archetype_name = "Lens Folder"
    use_folder_tabs = 0
    allowed_content_types = ['ContentSelectionLens', 'FavoritesLens', 'LensOrganizer']

    schema = schema
    
    security = AccessControl.ClassSecurityInfo()
    
    actions = (
               {'id': 'view',
                'title': 'View',
                'action': Expression('string:${object_url}/lens_folder'),
                'permissions': (View,),  # set default view, but don't let anybody see the tab
                'visible': 0},
               {'id': 'edit',  # turn off 'edit' tab
                'visible': 0},
               {'id': 'metadata',  # turn off 'properties' tab
                'visible': 0},
              )
    
    security.declarePublic('getOwnerName')
    def getOwnerName(self):
        """Lookup the owner's fullname and return it."""
        owner = str(self.getOwner())
        return getToolByName(self, 'portal_membership').getMemberById(owner).getProperty('fullname', owner)
    
    # A PUT on the folder is intentionally a no-op
    security.declareProtected(ModifyPortalContent, 'PUT')
    def PUT(self, REQUEST):
        return

    # underlying zope delete must be overriden to throw the proper error
    # security.declareProtected(ModifyPortalContent, 'DELETE')
    security.declareProtected(View, 'DELETE')
    def DELETE(self, REQUEST, RESPONSE):
        REQUEST.response.setStatus('BadRequest')
	REQUEST.response.appendHeader('error', "Lens Folders can not be deleted")

        return 

    security.declareProtected(ModifyPortalContent, 'atomPost')
    def atomPost(self, content):
        """retrieves post information and creates the content """

        text = content
        dom = minidom.parseString(text)

	## make sure id does not already exist
	id = domLensId(dom)

	self.invokeFactory(id=id, type_name="ContentSelectionLens")
	lens = self[id]

        member = self.portal_membership.getAuthenticatedMember()

        fullname = member.getProperty('fullname', None)
        if fullname: 
            lens.setTitle("%s's Lens" % fullname)

	editLensFromDom(lens, dom, False)

        lens.reindexObject(idxs=['count'])
        return
        
    def getFeedData(self):
        fieldDict = {'author':str(self.getOwnerName()),'title':'Lenses By ' + str(self.getOwnerName()),'id':'self.getId()','lastUpdated':str(self.ModificationDate()),'lenses':[]}
        fieldDict['lastUpdated'] = self.ModificationDate()
        #loop through lenses and add to list
        lensList = self.contentValues()
        
        for lens in lensList:
            if lens.review_state() != 'private':
                lensDict = {}
                lensDict['author'] = lens.getOwnerName()
                lensDict['title'] = lens.title
                lensDict['category'] = lens.getCategory()
                lensDict['id'] = lens.getId()
                lensDict['lastModified'] = lens.ModificationDate()
                if lens.hasLogo():
                    lensDict['logoURL'] = str(lens.absolute_url()) + '/logo_thumb'
                else:
                    lensDict['logoURL'] = ''
                lensDict['lensBy'] = lens.getCreatorName()
                lensDict['count'] = lens.getCount()
                lensDict['feedURL'] = str(lens.absolute_url()) + '/atom'
                lensDict['lensURL'] = str(lens.absolute_url())
                fieldDict['lenses'].append(lensDict)
        return fieldDict

registerType(LensFolder, 'Lensmaker')
