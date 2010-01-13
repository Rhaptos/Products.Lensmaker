"""
Tool definition.

Author: J. Cameron Cooper (jccooper@rice.edu)
Copyright (C) 2007 Rice University. All rights reserved.

This software is subject to the provisions of the GNU Lesser General
Public License Version 2.1 (LGPL).  See LICENSE.txt for details.
"""
from sets import Set
from types import ListType, StringTypes, TupleType

import AccessControl
from OFS.SimpleItem import SimpleItem
from Globals import InitializeClass
from ZODB.POSException import ConflictError

from Products.CMFCore.utils import UniqueObject, getToolByName
from Products.CMFCore.CMFCorePermissions import View, ManagePortal
from Products.CMFPlone.utils import _createObjectByType
from Products.PageTemplates.PageTemplateFile import PageTemplateFile
from Products.ZCatalog.Lazy import LazyCat

from Products.CMFCore.utils import _getAuthenticatedUser
from Products.CMFCore.CMFCorePermissions import AccessInactivePortalContent


from config import PROJECTNAME, KNOWN_LENS_TYPES, TAGNAMESPACE_DELIMITER

ManagePermission = 'View management screens'  # an old permission that's unimportable

class LensTool(UniqueObject, SimpleItem):
    """Globally available methods for interacting with the lens system."""

    id = 'lens_tool'
    meta_type = 'Lens Tool'
    security = AccessControl.ClassSecurityInfo()

    manage_options=(( {'label':'Overview', 'action':'manage_overview'},
                     )
                    + SimpleItem.manage_options
                    )
    ##   ZMI methods
    security.declareProtected(ManagePortal, 'manage_overview')
    manage_overview = PageTemplateFile('zpt/overview', globals() )
    
    def __init__(self):
        """Setup tool data."""
        self.lenstypes = KNOWN_LENS_TYPES
    
    security.declareProtected(ManagePermission, 'manage_setConfig')
    def manage_setConfig(self, lenstypes, REQUEST=None):
        """Post-creation config; see overview.zpt."""
        if type(lenstypes) in StringTypes:
            lenstypes = lenstypes.split()
        self.lenstypes = lenstypes
        if REQUEST is not None:
            REQUEST.RESPONSE.redirect(self.absolute_url()+'/manage_overview')

    security.declareProtected(ManagePermission, 'getLensTypes')
    def getLensTypes(self):
        """List of content types considered lenses."""
        lenstypes = getattr(self, 'lenstypes', None)
        if lenstypes is None:  # auto-upgrade step
            self.lenstypes = lenstypes = KNOWN_LENS_TYPES
        return lenstypes

    def searchResults(self, REQUEST=None, **kw):
        """Calls lenses_catalog.searchResults with extra arguments that
        limit the results to what the user is allowed to see.
        """
        portal_catalog = getToolByName(self, 'portal_catalog')
        lens_catalog = getToolByName(self, 'lens_catalog')
        user = _getAuthenticatedUser(self)
        kw['allowedRolesAndUsers'] = portal_catalog._listAllowedRolesAndUsers(user)
        
        # portal_catalog checks expiry here, but we don't care

        return lens_catalog.searchResults(REQUEST=REQUEST, **kw)


    security.declarePrivate('_getEntriesFor')
    def _getEntriesFor(self, contentId, version=None, implicit=True, inside=None):
        """Internal method to return all entries pointing to a specified item. If a version is provided,
        only entries with a start version less than and a stop version greater than that version will be
        provided.

        params:
          contentId: key for item. string.
          version: version of item from 'contentId'. string in the form '1.10' or list of ints like [1,10].
              optional; if not provided, no version filtering. List param is a bit faster.
          implicit: get implicitly included content, being content inside an included collection. boolean.
          inside: the collection we are inside, if any, so that entries for that collection can be returned.
              tuple: (contentId, version). version is as above.
        returns:
          (global entries, contextual entries), where each is a (lazy) list of SelectedContent brains
        """
        insideId = inside and inside[0] or None
        insideVersion = inside and inside[1] or None
        if version:
            if type(version) in StringTypes:
                version = [int(x) for x in version.split('.')]  # must provide list, not tuple!
            if type(version) is not ListType:
                version = list(version)
        if inside:
            if type(insideVersion) in StringTypes:
                try:
                    insideVersion = [int(x) for x in insideVersion.split('.')]  # must provide list, not tuple!
                except ValueError:  # not an int, probably an unpublished course
                    if insideVersion == "**new**": insideVersion = [1,1]  # just set dummy version, no course entries will be found
                    else: raise
            if type(insideVersion) is not ListType:
                insideVersion = list(insideVersion)
        
        query = {}
        query['portal_type'] = 'SelectedContent'
        query['id'] = contentId
        if version:
            query['getVersionStart'] = {'query':[version], 'range':'max'}
            query['getVersionStop']  = {'query':[version], 'range':'min'}
            # Note: the version stop here is supposed to be open-ended; we do this by relying on endless entries
            # being a different type to sort to the end instead of the beginning. See VersionField for details.

        directentries = self.searchResults(**query)

        content_catalog = getToolByName(self, 'content').catalog
        collections = [c for c in content_catalog(containedModuleIds=contentId) if c.objectId != insideId]
        latest_version_str = content_catalog(objectId=contentId)[0].version  # TODO: only works for published
                                                                             # leaving here to draw out errors
        if version:
            # Filter out any collections that don't contain this version of the module.
            collectionIds = []
            for c in collections:
                pcp = c.getObject().getContainedObject(contentId)
                if pcp.version == 'latest':
                    pcp_version_str = latest_version_str
                else:
                    pcp_version_str = pcp.version
                pcp_version_tup = [int(x) for x in pcp_version_str.split('.')]
                if pcp_version_tup == version:
                    collectionIds.append(c.objectId)
        else:
            collectionIds = [c.objectId for c in collections]
        containingentries =  self.searchResults({'portal_type':'SelectedContent','id':collectionIds, 'getImplicit':True})
        allentries = directentries + containingentries

        if inside:
            query['id'] = insideId
            query['getVersionStart'] = {'query':[insideVersion], 'range':'max'}
            query['getVersionStop']  = {'query':[insideVersion], 'range':'min'}
            contextual = self.searchResults(**query)
        else:
            contextual = LazyCat([])

        return (allentries, contextual)

    security.declarePublic('getListsIncluding')
    def getListsIncluding(self, contentId, version=None, categories=[], implicit=True, inside=None):
        """Return data about known lens content (per getLensTypes) which include entries for specified item.
        If a version is provided, only entries with a start version less than and a stop version greater
        than that version will be provided.

        params:
          contentId: key for item. string.
          version: version of item from 'contentId'. string.
          categories: "lens" types (endorsement, review, etc) to return. list of strings. Empty/None means all.
          implicit: get implicitly included content, being content inside an included collection. boolean.
          inside: the collection we are inside, if any, so that entries for that collection can be returned.
              tuple: (contentId, version)
          return {category: {listlocation:(listinfo,entryinfo)}}
            where listinfo={name:value} from CSL.listDict(), including lens id, names, category, state, location, et al.
            where entryinfo={name:value} including entry id, Title, tags, comment, fromImplicit
        """
        lens_catalog = getToolByName(self, 'lens_catalog')
        catdict = {}

        entries = self._getEntriesFor(contentId, version, implicit, inside)
        # each list can contain only one entry, so we don't need a set...
        for entry in entries[1] + entries[0]:
            # get parent info, which among other things will tell us about implicitness
            parentpath = entry.getPath().split('/')[:-1]
            parent = self.restrictedTraverse(parentpath)  # TODO : might put this in a CSL metadata slot and get from catalog
            listinfo = parent.listDict()
            listloc = listinfo['location']

            edict = {}
            #we're not us
            if entry.getId != contentId:
                if inside and entry.getId == inside[0]:
                    edict['fromImplicit'] = 'contextual'
                else:
                    edict['fromImplicit'] = 'implicit'
            else:
                edict['fromImplicit'] = False
            edict['id'] = entry.getId
            edict['Title'] = entry.Title
            edict['tags'] = ' '.join(entry.getTags)

            if 'getNamespaceTags' in lens_catalog.indexes():
                # Legacy data with essentially unintialized metadata
                # will not return the desired iterablke type.
                if isinstance(entry.getNamespaceTags, (ListType, TupleType)):
                    edict['namespaceTags'] = entry.getNamespaceTags
                else:
                    edict['namespaceTags'] = []

            edict['comment'] = entry.getPlainComment
            edict['approved'] = getattr(entry, 'getApproved', lambda:False)

            #separate lists by type (or only the specified type, if specified)
            cat = listinfo['category']
            if not catdict.has_key(cat):
                catdict[cat] = {}
            if not catdict[cat].has_key(listloc):
                catdict[cat][listloc]=(listinfo,[])
            catdict[cat][listloc][1].append(edict)

        return catdict

    security.declarePublic('getListsOwned')
    def getListsOwned(self, memberid=None, **kwargs):
        """Return known lens content (per getLensTypes) owned by member 'memberid', as a catalog list.
        
        If memberid is None, default to authenticated user, if any.
        """
        if not memberid:
            mship = getToolByName(self, 'portal_membership')
            m = mship.getAuthenticatedMember()
            if len(m.getRoles()) > 1:  # only one role == Anonymous; should be less fragile than name checks
                memberid = m.getId()
        
        if memberid:
            contentFilter = dict(portal_type=self.getLensTypes(), Creator=memberid)
            if kwargs:
                contentFilter.update(kwargs)
            pwned = self.searchResults(**contentFilter)
            # allowedRolesAndUsers is for viewing, but there's no similar index for editing,
            # which would be more appropriate...
        else:
            pwned = []

        return pwned
    
    security.declarePublic('getRecentlyModifiedListsOwned')
    def getRecentlyModifiedListsOwned(self, memberid=None):
        """Return known lens content owned by member 'memberid' and sorted via modification date,
        as a catalog list.
        
        If memberid is None, default to authenticated user, if any.
        """
        if not memberid:
            mship = getToolByName(self, 'portal_membership')
            m = mship.getAuthenticatedMember()
            if len(m.getRoles()) > 1:  # only one role == Anonymous; should be less fragile than name checks
                memberid = m.getId()
        
        if memberid:
            pwned = self.searchResults(portal_type='ContentSelectionLens', Creator=memberid, sort_on='modified', sort_order='descending')
            # allowedRolesAndUsers is for viewing, but there's no similar index for editing,
            # which would be more appropriate...
        else:
            pwned = []

        return pwned
    
    security.declarePublic('getListsBy')
    def getListsBy(self, category=None, path=None, all=None, memberid=None, inclzero=True):
        """Return public lensish content (per getLensTypes) meeting certain criteria. Light catalog wrapper.
        Returns catalog results list.
        If 'path' is provided, restrict to that path. (Used for showing only those inside a folder.)
        If 'category' is None, all are provided. Otherwise, all in that category.
        If 'all' is true, will not restrict to public.
        If 'inclzero' if true, empty lenses will be included. This is the default, being the old behavior.
        Path should be as acceptable by lens_catalog; like that provided by '/'.join(context.getPhysicalPath())
        """
        # get the lenses
        args = {'portal_type':self.getLensTypes()}
        if category: args['getCategory'] = category
        if path: args['path'] = path
        if not all: args['review_state'] = ('published','published_open','private_open')
        if memberid: args['Creator'] = memberid
        results = self.searchResults(**args)
        if results:
            if not inclzero: results = [x for x in results if x.getCount > 0]

            # find all lenses referenced by a lensorganiser
            rc = getToolByName(self, 'reference_catalog')
            targetUIDs = [b.targetUID for b in rc(relationship='lenses_lensorganizers')] 
            
            # filter out the lenses in lensorganisers
            if targetUIDs:
                results = [x for x in results if x.UID not in targetUIDs]

        return results

    security.declarePublic('getTagsForContent')
    def getTagsForContent(self, contentId, version=None, inside=None, tag_type='tags'):
        """Return the tags on any entries that point to specified item. If version is supplied, only return
        tags on entries that include the version in their range.
        params:
          contentId: key for item. string.
          version: version of item from 'contentId'. string.
        return:
          list of strings

        Theoretical companion would be 'getTagCloudForContent' which would return
        list of {tagname:number/percentage})

        tag_type is one of ('tags', 'namespaceTags')
        """
        insideId = inside and inside[0] or None

        #TODO : switched filter by version
        directentries = self.searchResults(portal_type='SelectedContent', id=contentId)

        content_catalog = getToolByName(self, 'content').catalog
        collectionIds = [c.objectId for c in content_catalog(containedModuleIds=contentId)]
        containingentries =  self.searchResults({'portal_type':'SelectedContent','id':collectionIds, 'getImplicit':True})
        contextualentry =  self.searchResults({'portal_type':'SelectedContent','id':insideId})
        allentries = directentries + containingentries + contextualentry

        #aggregate comments for each entry into set
        #  (for a tag cloud, we could aggregate into a {tagname:number of occurences})
        tagset = Set()
        for brain in allentries:
            if tag_type == 'tags':
                tags = brain.getTags
            elif tag_type == 'namespaceTags':
                # Legacy data with essentially uninitialized metadata
                # will not return the desired iterable type.
                if isinstance(brain.getNamespaceTags, (ListType, TupleType)):
                    tags = brain.getNamespaceTags
                else:
                    tags = []
            else:
                tags = []
            for tag in tags:
                tagset.add(tag)

        if tag_type == 'tags':        
            return tuple(tagset)

        if tag_type == 'namespaceTags':            
            return tuple(tagset)

        return []

    security.declarePublic('getContentForTag')
    def getContentForTag(self, tag):
        """Return content that has this on any entries that point to that content.
        params:
          tag: string
        returns:
          list of entry brains (urls? id/version? objects?)
        """
        contentFilter = dict(portal_type='SelectedContent')
        lens_catalog = getToolByName(self, 'lens_catalog')

        if 'getNamespaceTags' in lens_catalog.indexes():
            if tag.find(TAGNAMESPACE_DELIMITER) != -1:
                contentFilter['getNamespaceTags'] = tag
            else:
                contentFilter['getTags'] = tag
        else:
            contentFilter['getTags'] = tag

        taggedentries = self.searchResults(**contentFilter)
        return taggedentries

    security.declarePublic('entriesToContent')
    def entriesToContent(self, entries):
        """Return list of result objects (catalog brains) for content referred to in list of entries
        passed in with 'entrylist'.
        Used to convert something like the output of 'getContentForTag' into a list of content brains
        for use by a results macro.
        
        params:
          entries: list of entry (SelectedContent) brains
        returns:
          list of content brains
        """
        ids = [elt.getId for elt in entries]
        return self.content.catalog(objectId=ids)
    
    security.declarePrivate('getMajorContainer')
    def getMajorContainer(self):
        """Get the folder that contains all individual folders. Private because one shouldn't
        rely on there being a major container.
        """
        toplevelcontainer="lenses"
        portal = getToolByName(self, 'portal_url').getPortalObject()
        lenses = getattr(portal.aq_explicit, toplevelcontainer, None)
        if lenses is None:  # make one...
            portal.invokeFactory('LensMajorContainer', id=toplevelcontainer, title="Lenses")
            lenses = getattr(portal, toplevelcontainer)
        return lenses
    
    security.declarePublic('getIndividualFolder')
    def getIndividualFolder(self, userid=None, create=True):
        """Return the folder that contains lenses for the current user. None for Anonymous.
        Pass 'userid' for a specific non-current user.
        Pass boolean value for 'create' to create folder if it doens't exist. Default: true.
        """
        mship = getToolByName(self, 'portal_membership')
        if userid is None:
            m = mship.getAuthenticatedMember()
        else:
            m = mship.getMemberById(userid)
        if len(m.getRoles()) > 1:  # only one role == Anonymous; should be less fragile than name checks
            memberid = m.getId()
            lenses = self.getMajorContainer()
            namedfolder = getattr(lenses, memberid, None)
            if namedfolder is None and create: # make one...
                namedfolder = _createObjectByType('LensFolder', lenses, memberid)

                # set ownership
                namedfolder.__ac_local_roles__ = None
                namedfolder.manage_setLocalRoles(memberid, ['Owner'])

            return namedfolder
        return None

    security.declarePublic('getMemberFolder')
    def getMemberFolder(self, context):
        """
        Traverse upwards from context until the member's folder is found
        """
        folder = None
        parent = getattr(context, 'aq_parent', None)
        previous = context
        while parent is not None:
            if getattr(parent, 'portal_type', '') == 'LensMajorContainer':
                folder = previous
                break
            previous = parent
            parent = getattr(parent, 'aq_parent', None)
   
        return folder

    security.declarePublic('getOpenLenses')
    def getOpenLenses(self, full_objects=False, omit_contained_ids=None):
        """
        Return open lenses

        params:
            full_objects: 
                return full objects
            omit_contained_ids:
                do not include a lens in the result if an id in omit_contained_ids
                is contained by the lens
        """

        if omit_contained_ids is not None:
            # Make iterable
            if type(omit_contained_ids) != type([]):
                omit_contained_ids = [omit_contained_ids]
            
            # Remove the paths for the ids to be omitted from result_paths
            result_paths = [b.getPath() for b in self.searchResults(portal_type=self.getLensTypes(), 
                            review_state=['published_open', 'private_open'])]
            remove_paths = ['/'.join(b.getPath().split('/')[:-1]) for b in self.searchResults(path=result_paths, id=omit_contained_ids)]
            new_paths = []
            for pth in result_paths:
                if pth not in remove_paths:
                    new_paths.append(pth)

            # Do the final query
            results = self.searchResults(
                            portal_type=self.getLensTypes(), 
                            path=new_paths,
                            review_state=['published_open', 'private_open'])

        else:
            # Nothing to omit
            results = self.searchResults(portal_type=self.getLensTypes(), review_state=['published_open', 'private_open'])

        if full_objects:
            return [r.getObject() for r in results]
        return results

    security.declarePublic('catalogQueueInfo')
    def catalogQueueInfo(self):
        """Fairly general method for indicating time left for queue catalog to process something just added.
        Put here because the lenses facility uses this, and it's convenient.
        Return tuple of raw size and estimated time in minutes.
        """
        rate = 150.0 # per minute
        qcat = getToolByName(self, 'lens_catalog')
        if getattr(qcat, 'manage_size', None) is not None:
            size = qcat.manage_size()
            return (size, size/rate)
        return None

    security.declarePublic('catalogQueueProcess')
    def catalogQueueProcess(self):
        """Poke otherwise-resticted process method of queue catalog.
        """
        qcat = getToolByName(self, 'lens_catalog')
        process = getattr(qcat, 'process', None)
        if process is not None:
            return process(25)

    security.declarePrivate('notify')
    def notify(self, lenses, object, template, **kwargs):
        """
        Render the mail template provided using the object as context and email it to the adress associated with the lens.
        """
        
        host = self.MailHost
        for lens in lenses:
#           try:
            # we cannot pass 'lens' as it might be private and thus unauthorized to the current user
            lensTitle = lens.Title()
            lensURL = lens.absolute_url()
            included = not lens[object.objectId].getVersionStop()
            lensCreator = lens.Creator()

            if lens.notifyOfChanges:
                mail_text = template( self,
                                      lensTitle=lensTitle,
                                      lensURL=lensURL,
                                      included=included,
                                      lensCreator=lensCreator,
                                      object=object,
                                      **kwargs
                                      )
                try:
                    host.send(mail_text)
                except ConflictError:
                    raise
                except Exception, e:
                    import zLOG
                    zLOG.LOG("Lensmaker", zLOG.ERROR, "Error sending mail: " + str(e))
#           except:
#            raise KeyError, mail_text
    ### FIXME:
    ### We really want the Zope3 Event system for this.
    ### Each of these functions should be defined as adapters
    ### for the specific interface and the event IObjectPublished
    ### Interfaces that we might use to differentiate the different
    ### objects for the different actions they need might be:
    ### IObjectNew, IObjectRevised, IObjectContained,
    ### IObjectParent, IObjectDerived
    ### They would then be registered like:
    ###
    ### from zope import component
    ### @component.adapter(IObjectRevised,IObjectPublished)
    ### def notifyLensRevisedObject(obj,event):
    ###     members = [m.aq_parent.owner for m in catalog(Type='Entry', id=obj.id) if type(m.aq_parent.versions) == type([])]
    ###     obj.lens_tool.notify(members, obj, obj.obj_revised_template)
    ### component.provideHandler(notifyLensRevisedObject)
    ###
    ### But for now, we're just going to define some nice functions
    ### that can be called from elsewhere:

    security.declarePrivate('_lensesFromResults')
    def _lensesFromResults(self, brains):
        """Translate a catalog results list of SelectedContent brains into their parent lenses.
        Returns list of lenses (really the parent of every entry.)
        Provide a 'root' to do an unrestrictedTraverse from if you're doing multiple lookups to save time.
        """
        root = self.unrestrictedTraverse('/')
        return [root.unrestrictedTraverse('/'.join(m.getPath().split('/')[:-1])) for m in brains]

    security.declarePublic('notifyLensObjectRevised')
    def notifyLensRevisedObject(self, object):
        """Notify the lens owner that an object in their lens was revised."""
        # First, objects directly in a lens
        entries = self.lens_catalog(Type='Selected Content', id=object.objectId)
        lenses = [lens for lens in self._lensesFromResults(entries) if lens.portal_type!='SelectedContent']
        if lenses:
            self.notify(lenses, object, self.lens_notify_revised_script)

    security.declarePublic('notifyLensContainedObject')
    def notifyLensContainedObject(self, object):
        """Notify the lens owner that an object inside one of its Collections was revised"""
        # Then, any additional lenses that contain a course with the module in it
        raw_container_objs = self.content.catalog(containedModuleIds=object.objectId)
        # Filter out courses that only use the exact version
        container_objs = [b for b in raw_container_objs
                            if b.getObject().getContainedObject(object.objectId).version == 'latest']
        # FIXME: Turn this off for now - we want two emails until we get a good combined template
        #direct_ids = []
        #direct_ids = [m.getObject().aq_parent.id for m in self.lens_catalog(Type='Selected Content', id=object.objectId)]
        for col in container_objs:
            entries = self.lens_catalog(Type='Selected Content', id=col.objectId)
            lenses = self._lensesFromResults(entries)
            #lenses = [lens for lens in lenses if lens.getId() not in direct_ids]
            if lenses:
                self.notify(lenses, col, self.lens_notify_contained_script, contained_object=object)

    security.declarePublic('notifyLensDerivedObject')
    def notifyLensDerivedObject(self, object):
        """Notify the lens owner that an object was derived from one of its objects"""
        parent_obj = object.getParent()
        entries = self.lens_catalog(Type='Selected Content', id=parent_obj.objectId)
        lenses = self._lensesFromResults(entries)
        if lenses:
            self.notify(lenses, parent_obj, self.lens_notify_derived_script, modified_object=object)

    ### End Event System Hack

InitializeClass(LensTool)
