"""
Principal container schema and definition.

Author: J. Cameron Cooper (jccooper@rice.edu)
Copyright (C) 2007 Rice University. All rights reserved.

This software is subject to the provisions of the GNU Lesser General
Public License Version 2.1 (LGPL).  See LICENSE.txt for details.
"""
from math import floor
from types import ListType, StringTypes, TupleType

import AccessControl

from Products.CMFCore.CMFCorePermissions import View, ModifyPortalContent
from Products.CMFCore.Expression import Expression
from Products.CMFCore.utils import getToolByName

from xml.dom import minidom
from Products.Archetypes.public import Schema
from Products.Archetypes.public import registerType
from Products.Archetypes.public import OrderedBaseFolder, OrderedBaseFolderSchema
from Products.Archetypes.public import StringField, StringWidget
from Products.Archetypes.public import TextField, TextAreaWidget
from Products.Archetypes.public import BooleanField, BooleanWidget
from Products.Archetypes.public import IdWidget, SelectionWidget
from Products.Archetypes.public import ImageField, ImageWidget, LinesWidget
from Products.Archetypes.public import ComputedField, LinesField
from Products.Lensmaker.domTools import domEntryId, findEntryById, editEntryFromDom, editLensFromDom
from OFS.ObjectManager import ObjectManager
from DateTime import DateTime

from Products.RhaptosCollection.Widget import URLWidget, LanguageWidget
from Products.RhaptosCollection.config import LICENSES, LANGUAGES, LANGS_NOSUB, LANGS_COMBINED
from Products.RhaptosCollection.types import Collection

from Products.MasterSelectWidget.MasterSelectWidget import MasterSelectWidget

# allowedRolesAndUsers
from AccessControl.PermissionRole import rolesForPermissionOn
from Products.CMFCore.utils import _mergedLocalRoles

from LensPermissions import AddQualityLens
from LensPermissions import BrandContent

from config import LENS_TYPES, TAGNAMESPACE_DELIMITER
from widgets import ColorWidget

LEVELS = 5

# fields... (we might put these in separate schema file somewhere.)
# recognized schemata are 'basic', 'settings', 'display'. We might have an 'advanced' or use 'default' for that.

shortnamedesc = """Change how the lens will be identified in its URL. Short names of all-lowercase recommended.
If left blank, the system will provide a value.
"""
shortname = StringField('id',        # overrides default
                schemata='advanced',
                required=0,
                mode="rw",
                accessor="getId",
                mutator="setId",
                default=None,
                widget=IdWidget(label="Lens ID",
                                label_msgid="label_name",
                                description=shortnamedesc,
                                description_msgid="help_name",
                                i18n_domain="plone",
                                ignore_visible_ids=True)
                )

displaynamedesc = """An abbreviated name of this lens or your organization. This will be displayed on
content pages and may be used to generate part of the URL for the lens."""
displayname = StringField('displayName',
                          schemata='basic',
                          required=1,
                          searchable=1,
                          index="lens_catalog/:brains",
                          widget=StringWidget(label="Display Name",
                                              description=displaynamedesc,
                                              i18n_domain="rhaptos"),
                         )

titledesc = "Enter the full title of your lens."
title = StringField('title',         # overrides default
                accessor='Title',                             # compat with default/DC
                schemata='basic',
                required=1,
                searchable=1,
                widget=StringWidget(label="Title",
                                    description=titledesc,
                                    i18n_domain="rhaptos",
                                    size='75')
                )

descdesc = "Enter a description of this lens and/or your organization. Accepts simple HTML, including links and paragraphs."
desc = TextField('description',         # overrides default
              schemata='basic',
              required = 0,
              accessor="Description",                             # compat with default/DC
              validators=('simple_safe_html',),
              default_content_type='text/html',
              default_output_type='text/html',
              ## our validator is so strict, that we don't need to run the
              ## safe_html transform, which inserts extra <p> tags around the data, which is a bit mysterious.
              #default_output_type='text/x-html-safe',
              allowable_content_types=('text/html'),
              widget=TextAreaWidget(label="Description",
                                    description=descdesc,)
              )

logodesc = """To add or change the logo: click the \"Browse\" button and select an image.
Maximum dimensions are 150 pixels wide by 150 pixels tall. Your image will be resized if it is too large."""
logo = ImageField('logo',
                schemata='branding',
                searchable=0,
                #swallowResizeExceptions=1,  # important for issue in next line
                # TODO: image validator, to take the place of hacky try/except in lens_editor.cpy
                # ...theoretically we have a validator on the portraits
                # TODO: if accept unresizable files, add max size validator
                max_size=(150,150),
                sizes={'thumb':(150,50)},  # we really only care about the thumbnail height
                widget=ImageWidget(label="Logo",
                                   description=logodesc,
                                   show_content_type = False,  # only in newer, alas
                                   i18n_domain="rhaptos",)
                       )

hasLogo= ComputedField('haslogo',
                accessor="hasLogo",
                searchable=0,
                index="lens_catalog/:brains",
                expression='context.getLogo() and True or False',
                widget=StringWidget(modes=()),
                )

banner = BooleanField('banner',
                schemata='branding',
                searchable=0,
                default=0,
                write_permission=BrandContent,
                widget=BooleanWidget(label="Place a branding banner on pages in my lens.",
                                              description="Do you want to display an identification banner on pages inside this lens?")
                       )

bannerColor = StringField('bannerColor',
                         schemata='branding',
                         validators=('isHexColor',),
                         write_permission=BrandContent,
                         widget=ColorWidget(label="Branding Banner Color",
                                            description="Use the color chooser to select a color value for the branding elements.",
                                            i18n_domain="rhaptos")
                         )


urldesc= "Add a Web page you would like readers of your lens to visit, e.g. http://cnx.org/aboutus"
url = StringField('url',
                         searchable=0,
                         schemata='basic',
                         validators=('isURL',),
                         widget=URLWidget(label="External Web Page",
                                          description=urldesc,
                                          i18n_domain="rhaptos",
                                          size='75')
                         )

urltextdesc = "Text used to link to your provided URL."
urltext = StringField('urlText',
                          schemata='advanced',
                          searchable=1,
                          default="Visit Web page",
                          #schemata="url",
                          widget=StringWidget(label="Text for External Web Page",
                                              description=urltextdesc,
                                              i18n_domain="rhaptos"),
                         )

notifyOfChangesdesc = """Notifications will help you determine whether you would like to include or exclude newly published versions of content in this lens."""
notifyOfChanges = BooleanField('notifyOfChanges',
                         schemata="settings",
                         searchable=0,
                         default=1,
                         widget=BooleanWidget(label="Receive e-mails when any content included in this lens is changed.",
                                              description=notifyOfChangesdesc,)
                         )

noTagClouddesc = ""
noTagCloud = BooleanField('noTagCloud',
                         schemata='advanced',
                         searchable=0,
                         default=0,
                         widget=BooleanWidget(label="Don't show tag cloud",
                                              description=noTagClouddesc,)
                         )
masterlanguagedesc = 'Select the primary language for this lens.'
masterlanguage = StringField('master_language',
               schemata='advanced',
               searchable=0,
               required=1,
               vocabulary = LANGUAGES,
               widget=LanguageWidget(slave_fields=({'name': 'language',
                                                    'action': 'vocabulary',
                                                    'vocab_method': 'getLanguageWithSubtypes',
                                                    'control_param': 'lang'},
                                                    {'name': 'language',
                                                    'action': 'disable',
                                                    'hide_values': LANGS_NOSUB
                                                    },),
                                         label = 'Language',
                                         helper_css=('language_locale.css',),
                                         description=masterlanguagedesc,
                                         i18n_domain="rhaptos",)
                            )

languagedesc = 'The language subtype for this content, if applicable.'
language = StringField('language',
               schemata='advanced',
               searchable=0,
               vocabulary = LANGS_COMBINED,
               widget=SelectionWidget(label='Regional Variant (optional)',
                                             description=languagedesc,
                                             helper_js=('language_locale.js',),
                                             i18n_domain="rhaptos",
                                             modes=('view',),  
                                             ),
                              )

rightsdesc = ""
rights = StringField('rights',             # override DC/default field
                searchable=0,
                mode='r',
                vocabulary=LICENSES,
                enforceVocabulary=1,
                default=LICENSES[0],
                accessor="Rights",
                widget=StringWidget(modes=('view',),
                                              label="License",
                                              description=rightsdesc,
                                              i18n_domain="rhaptos"),
                              )

categorydesc = "Select the type of lens."
category = StringField('category',
                         default=LENS_TYPES[-1],
                         schemata='advanced',
                         read_permission=View,
                         write_permission=AddQualityLens,
                         index="lens_catalog/FieldIndex",
                         searchable=0,
                         vocabulary=LENS_TYPES,
                         enforceVocabulary=1,
                         widget=SelectionWidget(label="Lens Type",
                                                description=categorydesc,
                                                i18n_domain="rhaptos",
                                                modes=('edit'),
                                                format= "select",
                                                )
                         )

count = ComputedField('count',
                searchable=0,
                index="lens_catalog/:brains",
                expression="context.computeLensCount()",
                widget=StringWidget(modes=()),
                )

creatorName = ComputedField('creatorName',
                searchable=0,
                index="lens_catalog/:brains",
                expression='context.getCreatorMember().getProperty("fullname")',
                widget=StringWidget(modes=()),
                )

# This isn't neccesary if we use portal_catalog, but portal_workflow
# doesn't seem smart enough to know about other catalogs.
review_state = ComputedField('review_state',
                searchable=0,
                accessor='review_state',
                index="lens_catalog/:brains",
                expression="context.calculateReviewState()",
                widget=StringWidget(modes=()),
                )

allowedRolesAndUsers= ComputedField('allowedRolesAndUsers',
                accessor="allowedRolesAndUsers",
                searchable=0,
                expression="context.allowedRolesAndUsers()",
                index="lens_catalog/KeywordIndex:brains",
                widget=StringWidget(modes=()),
                )

reviewers= LinesField('reviewers',
                accessor="getReviewers",
                index="lens_catalog/KeywordIndex",
                widget=LinesWidget(visible=False),
                )

schema = OrderedBaseFolderSchema.copy()

# for ordering purposes... language et al are default fields
schema.delField('language')
schema.delField('title')
schema.delField('description')

schema = schema +  Schema((shortname, title, displayname, desc, masterlanguage, language,
                                      logo, hasLogo, banner, bannerColor, url, urltext, category, rights,
                                      notifyOfChanges, noTagCloud,
                                      count, creatorName, review_state, allowedRolesAndUsers, reviewers))

class ContentSelectionLens(OrderedBaseFolder, ObjectManager):  # should it be BTree?  #! changed base class needs to change reindex hook
   """List of entries that select a set of content."""
   archetype_name = "Content Selection Lens"
   use_folder_tabs = 0  # controls 'contents' and 'syndication'
   allowed_content_types = ['SelectedContent']

   schema = schema

   content_icon = 'lenses.gif'

   security = AccessControl.ClassSecurityInfo()

   actions = (
               {'id': 'view',
                'title': 'View',
                'action': Expression('string:${object_url}/lens_view'),
                'permissions': (View,),
                'visible': 0},
               {'id': 'contents',
                'title': 'Edit lens contents',
                'action': Expression('string:${object_url}/lens_content_view'),
                'permissions': (ModifyPortalContent,)},
               {'id': 'edit',
                'title': 'Edit lens properties',
                'action': Expression('string:${object_url}/lens_edit'),
                'permissions': (ModifyPortalContent,)},
               {'id': 'tagnamespaces',
                'title': 'Tag vocabularies',
                'action': Expression('string:${object_url}/lens_tagnamespaces_view'),
                'condition': 'object/isOpen',
                'permissions': (ModifyPortalContent,)},
               {'id': 'reviewers',
                'title': 'Reviewers',
                'action': Expression('string:${object_url}/lens_reviewers'),
                'condition': 'object/isOpen',
                'permissions': (ModifyPortalContent,)},
               {'id': 'preview',
                'title': 'Preview lens',
                'action': Expression('string:${object_url}/lens_preview'),
                'permissions': (ModifyPortalContent,)},
               {'id': 'metadata',  # turn off 'properties' tab
                'visible': 0},
              )

   aliases = {
          '(Default)'  : 'lens_view',
          'edit'       : 'lens_edit',
          'gethtml'    : '',
          'index.html' : '',
          'properties' : '',
          'sharing'    : '',
          'view'       : 'lens_view',
          'contents'   : 'lens_content_view',
          }

   getLanguageWithSubtypes = Collection.getLanguageWithSubtypes  # this really should come from elsewhere
   getLanguagesWithoutSubtypes = Collection.getLanguagesWithoutSubtypes

   security.declarePublic(View, 'workflowStateEditable')
   def workflowStateEditable(self):
        """Return a boolean whether or not the user may edit the workflow state of this lens."""
        return True  # not very smart at the moment, but accurate.

   # see also SelectedContent... we should be able to refactor this eventually.
   def allowedRolesAndUsers(self):
        """
        Return a list of roles and users with View permission.
        Used by PortalCatalog to filter out items you're not allowed to see.
        """
        ob = self
        allowed = {}
        for r in rolesForPermissionOn('View', ob):
            allowed[r] = 1
        localroles = _mergedLocalRoles(ob)
        for user, roles in localroles.items():
            for role in roles:
                if allowed.has_key(role):
                    allowed['user:' + user] = 1
        if allowed.has_key('Owner'):
            del allowed['Owner']
        return list(allowed.keys())
   
   security.declareProtected(View, 'getTagCloud')
   def getCreatorMember(self):
      """Return member object representing this object's creator (and, almost certainly, owner).
      """
      mtool = getToolByName(self, 'portal_membership')
      return mtool.getMemberById(self.Creator())

   def calculateReviewState(self):
      """Return the review state from the workflow_tool"""
      wf_tool = getToolByName(self,'portal_workflow')
      return wf_tool.getInfoFor(self, 'review_state', '')

   security.declareProtected(View, 'getTagCloud')
   def listDict(self):
      """Return a dictionary with the needed information from this lens for content display.
      TODO: we can probably automate this, though I don't know if it's worth it.
      """
      wf_tool = getToolByName(self, 'portal_workflow')
      try:
          creatorName = self.getCreatorName()
      except AttributeError:
          # XXX shield : fall back on CMF default method.
          creatorName = self.Creator()
      return {
          'id':self.getId(),
          'location':self.absolute_url(),
          'displayName':self.getDisplayName(),
          'creatorName':creatorName,
          'title':self.Title(),
          #'description':self.Description(),
          'logo':self.getLogo() and 'true' or None,
          #'url':self.getUrl(),
          #'urltext':self.getUrlText(),
          #'notifyOfChanges':self.getNotifyOfChanges(),
          #'noTagCloud':self.getNoTagCloud(),
          #'master_language':self.getMaster_language(),
          #'language':self.getLanguage(),
          #'rights':self.Rights(),
          'category':self.getCategory(),
          'state':wf_tool.getInfoFor(self, 'review_state', ''),
      }

   security.declareProtected(View, 'getTagCloud')
   def getTagCloud(self):
      """A weighted list of all tags in all entries in this object.
      Weights are normalized percentage of all tags.
      Returns {tagname:(level, count)} where level is integer 1-5
      """
      # could be cached pretty well...
      # when implementing: http://24ways.org/2006/marking-up-a-tag-cloud
      entries = self.listOfEntries()
      tagcloud = {}

      if not entries:
          return tagcloud

      #iterate over contents, collect tags
      for brain in entries:
          for tag in brain.getTags:
              if not tagcloud.has_key(tag):
                  tagcloud[tag] = 0
              tagcloud[tag] += 1

      # find min/max/diff in counts, for subsequent normalization purposes
      levels = float(LEVELS)
      countlist = tagcloud.values()
      maxcount = countlist and max(countlist) or 0
      mincount = countlist and min(countlist) or 0
      diffcount = maxcount - mincount
      distribution = diffcount / levels  or 1 # 5 levels now.
      # TODO: log might be a better distribution than linear, but this lets us efficiently bag by division

      for tag, count in tagcloud.items():
          bag = int(floor((count - mincount) / distribution))  # bag according to distribution
          if bag == LEVELS: bag -= 1   # max values will get bagged too high
          tagcloud[tag] = (bag, count)

      return tagcloud

   security.declareProtected(View, 'listOfEntries')
   def listOfEntries(self, tag=None, approved=None):
      """Entries in this object, filtered by presence of tag. If tag is None, no filtering.
      Returns list of brains. Probably lazy, as directly from the catalog.
      """
      # TODO: utilize for contentValues/Ids ?
      catalog = getToolByName(self, 'lens_catalog')
      query = {}
      query['portal_type'] = 'SelectedContent'
      query['path'] = '/'.join(self.getPhysicalPath())
      if tag: 
          # Seperate tag into a list of normal tabs and a list of namespace tags
          # if the index getNamespaceTags exists. This enables the code to be
          # backwards compatible for systems without getNamespaceTags.
          if 'getNamespaceTags' in catalog.indexes():
              normal_tags = []
              namespace_tags = []
              for t in tag:
                  if t.find(TAGNAMESPACE_DELIMITER) != -1:
                      namespace_tags.append(t)
                  else:
                      normal_tags.append(t)

              if normal_tags:
                  query['getTags'] = normal_tags

              if namespace_tags:
                # Find the set of namespace tag prefixes
                prefixes = {}
                for nst in namespace_tags:
                    prefix, dummy = nst.split(TAGNAMESPACE_DELIMITER)
                    prefixes.setdefault(prefix, [])
                    prefixes[prefix].append(nst)

                # If there is more than one prefix then do a query for
                # each set, else just a single query.                  
                if len(prefixes.keys()) > 1:
                    results = []
                    for prefix, nst in prefixes.items():
                        query['getNamespaceTags'] = nst
                        brains = catalog(**query)
                        results.append(set([b.getPath() for b in brains]))
                
                    # Find the intersection of the results
                    path_set = results[0]
                    for result in results[1:]:
                        path_set.intersection_update(result)

                    # Constrain query to use this set of paths
                    del query['getNamespaceTags']
                    query['path'] = list(path_set)

                else:
                    query['getNamespaceTags'] = namespace_tags

          else:
            query['getTags'] = tag

      if approved != None:
          query['getApproved'] = approved

      return catalog(**query)

   security.declareProtected(View, 'getDescription')
   def getDescription(self, tag=None, entries=None):
       """ returns descrition"""
       return Description

   security.declareProtected(View, 'contentResults')
   def contentResults(self, tag=None, entries=None):
       """Return list of result objects (catalog brains) for content in this list, filtered
       by tag, if provided, or corresponding to a list of entry brains (if present).
       Suitable (and used for) results display listing.
       """
       lens_tool = getToolByName(self, 'lens_tool')
       if not entries: entries = self.listOfEntries(tag)
       return lens_tool.entriesToContent(entries)
       # TODO: this returns latest only! Should we try to show 'last version'? (cont...)
       # if so, the most efficient way might be a new index with combined id/version
       # and also will require indexing on the versionStop of entries


   #def reindexObject(self, idxs=[]):
        #"""Called on changes to this object to make sure updated data gets into the catalog.
        #We override this to recatalog all 'SelectedContent' children because they have cataloged
        #data that they get from this object.
        #"""
        #OrderedBaseFolder.reindexObject(self, idxs)
        #for obj in self.contentValues():             # TODO: restrict to 
            #obj.reindexObject(idxs=['containingListInfo'])

   security.declareProtected(ModifyPortalContent, 'atomPost')
   def atomPost(self, content):
        """retrieves post information and creates the content """
        text = content
        dom = minidom.parseString(text)
        entryId = domEntryId(dom)
        entry = findEntryById(self, entryId)
        self.invokeFactory(id=entryId, type_name="SelectedContent")
	entry = findEntryById(self, entryId)
        editEntryFromDom(dom, entry, False)

	return

   security.declareProtected(ModifyPortalContent, 'PUT')
   def PUT(self, REQUEST):
        """retrieves put information and updates the lens appropriately """
        text = REQUEST.get('BODY', '')
        dom = minidom.parseString(text)

        retval = editLensFromDom(self, dom, True)
	if not retval is None:
	    REQUEST.response.setStatus('BadRequest') 
	    REQUEST.response.appendHeader('error', retval)

        return  

   security.declareProtected(View, 'isOpen')
   def isOpen(self):
        """
        Return True if lens is open, otherwise False
        """
        wf = getToolByName(self, 'portal_workflow')       
        return wf.getInfoFor(self, 'review_state') in ('private_open', 'published_open')

   security.declareProtected(View, 'getTagNamespaces')
   def getTagNamespaces(self, full_objects=False, flatten=False):
        """       
        Fetch entire set of available tag namespaces defined
        on this lens. This set is *not* the actual namespace tags
        that are set on content - rather, it is a "vocabulary".

        params:
            full_objects: return full objects, not just brains
            flatten: return list of strings where each string is of the form
                     {tag namespace prefix}::{tag}
        
        returns:
            see params
        """
        pc = getToolByName(self, 'lens_catalog')

        results = pc(
                portal_type='TagNamespace',
                path="/".join(self.getPhysicalPath()),
                sort_on='id'
                )

        if full_objects:
            results = [r.getObject() for r in results]
        
        if flatten:
            results = [r.getObject() for r in results]
            li = []
            for obj in results:
                li.extend(['%s%s%s' % (obj.getPrefix(), TAGNAMESPACE_DELIMITER, tag) for tag in obj.getTags()])
            return li

        return results

   security.declareProtected(View, 'getNamespaceTagsInUse')
   def getNamespaceTagsInUse(self, objectify=False):
        """
        Return the namespace tags applied to content added to this lens
        """
        pc = getToolByName(self, 'lens_catalog')

        result = pc(
                portal_type='SelectedContent',
                path="/".join(self.getPhysicalPath()),
                sort_on='id'
                )

        li = []
        for r in result:
            # Legacy data with essentially unintialized metadata
            # will not return the desired iterablke type.
            nst = r.getNamespaceTags
            if not isinstance(nst, (ListType, TupleType)):
                nst = []

            for tag in nst:
                if tag not in li:
                    li.append(tag)
        li.sort()

        if objectify:
            # xxx: maybe make it an utility?
            return self.restrictedTraverse('@@objectifyTagNamespaceList')(li)

        return li

   security.declareProtected(View, 'getReviewers')
   def getReviewers(self):
        """
        Accessor which strips out invalid member accounts
        """
        pms = getToolByName(self, 'portal_membership')
        result = []
        for memberid in self.getField('reviewers').get(self):
            member = pms.getMemberById(memberid)
            if member is not None:
                result.append(memberid)
        return result

   security.declareProtected(View, 'setReviewers')
   def setReviewers(self, value):
        """
        Manage reviewers and the associated Reviewer local roles
        """
        pms = getToolByName(self, 'portal_membership')
        oldreviewers = self.getReviewers()       

        # Remove Owner role if possible preserving other roles
        for memberid in oldreviewers:
            if memberid not in value:                
                roles = list(self.get_local_roles_for_userid(memberid))
                if 'Reviewer' in roles:
                    roles.remove('Reviewer')
                    pms.deleteLocalRoles(obj=self, member_ids=[memberid])
                    if roles:
                        self.manage_setLocalRoles(memberid, roles)
                    
        # Add Owner role
        for memberid in value:
            if memberid not in oldreviewers:
                roles = list(self.get_local_roles_for_userid(memberid)) + ['Reviewer']
                self.manage_setLocalRoles(memberid, roles)

        self.getField('reviewers').set(self, value)

   security.declareProtected(View, 'getActiveReviewers')
   def getActiveReviewers(self):
        """
        Return members that have actually reviewed content contained
        within this lens.
        """
        pms = getToolByName(self, 'portal_membership')
        lc = getToolByName(self, 'lens_catalog')

        contentFilter = dict(
                portal_type='SelectedContent',
                path='/'.join(self.getPhysicalPath()),
                getApproved=True
        )   
        reviewer_ids = []
        for brain in lc(**contentFilter):
            if brain.getApprovedBy not in reviewer_ids:
                reviewer_ids.append(brain.getApprovedBy)

        # Resolve reviewer ids into member accounts
        result = []
        reviewer_ids.sort()
        for reviewer_id in reviewer_ids:
            member = pms.getMemberById(reviewer_id)
            if member is not None:
                result.append(member)

        return result

   def computeLensCount(self):
        """
        Return number of SelectedContent item in self
        """
        return len(self.objectIds('SelectedContent'))

registerType(ContentSelectionLens)

