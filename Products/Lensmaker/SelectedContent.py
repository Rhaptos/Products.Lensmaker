"""
Contained object schema and definition.

Author: J. Cameron Cooper (jccooper@rice.edu)
Copyright (C) 2007 Rice University. All rights reserved.

This software is subject to the provisions of the GNU Lesser General
Public License Version 2.1 (LGPL).  See LICENSE.txt for details.
"""
import AccessControl

from Products.CMFCore.permissions import View, ModifyPortalContent
from Products.CMFCore.utils import getToolByName

from DateTime import DateTime
from xml.dom import minidom
from Products.Archetypes.public import Schema
from Products.Archetypes.public import DisplayList
from Products.Archetypes.public import registerType
from Products.Archetypes.public import BaseFolder, BaseFolderSchema # TODO: BTree? not ordered...
from Products.Archetypes.public import StringField, StringWidget
from Products.Archetypes.public import BooleanField, BooleanWidget
from Products.Archetypes.public import LinesField, LinesWidget
from Products.Archetypes.public import TextField, TextAreaWidget
from Products.Archetypes.public import ComputedField
from Products.Archetypes.public import ComputedWidget
from Products.Archetypes.public import SelectionWidget
from Products.Lensmaker.domTools import editEntryFromDom

from VersionField import TupleVersionField, TupleVersionWidget

from sets import Set


# allowedRolesAndUsers
from AccessControl.PermissionRole import rolesForPermissionOn
from Products.CMFCore.utils import _mergedLocalRoles
from LensPermissions import ApproveSelectedContent

NOVERSION = ""

# fields... (we might put these in separate schema file somewhere.)

# TODO: id must be set to contentId; see PCPs for inspiration...

contentIddesc = ""
contentId = StringField('contentId',
                required=1,
                searchable=0,
                default='',
                widget=StringWidget(label="Content Id",
                                    description=contentIddesc,
                                    i18n_domain="rhaptos"),
                #validators=('isModuleNumber',),
                )

title = ComputedField('title',
                accessor="Title",
                searchable=0,
                expression='context.computedTitle()',
                widget=StringWidget(label="Title",
                                           modes=('view',),
                                           i18n_domain="rhaptos"),
                )


# TODO: we have a VersionField...
versionStartdesc = ""
versionStart = TupleVersionField('versionStart',
                required=0,
                searchable=0,
                index="lens_catalog/FieldIndex:brains",  # indexes tuple of int, which is orderable, so we can select ranges
                default_method='currentVersion',
                vocabulary='moduleVersions',
                enforce_vocabulary=1,
                widget=TupleVersionWidget(label="Starting with version",
                                    description=versionStartdesc,
                                    i18n_domain="rhaptos",
                                    format='select'),
                #validators=('isVersion',),
                )

versionStopdesc = ""
versionStop = TupleVersionField('versionStop',
                required=0,
                searchable=0,
                index="lens_catalog/FieldIndex:brains",
                default=NOVERSION,
                vocabulary='moduleVersionsAndNone',
                enforce_vocabulary=1,
                widget=TupleVersionWidget(label="Ending with version",
                                    description=versionStopdesc,
                                    i18n_domain="rhaptos",
                                    format='select'),
                #validators=('isVersion',),
                )

versionLastSeendesc = ""
versionLastSeen = TupleVersionField('versionLastSeen',
                required=0,
                searchable=0,
                default=None,
                visible=0,
                vocabulary='moduleVersions',
                enforce_vocabulary=1,
                widget=TupleVersionWidget(label="Version at last visit",
                                    description=versionLastSeendesc,
                                    modes=(),
                                    i18n_domain="rhaptos"),
                #validators=('isVersion',),
                )

implicitdesc = ""
implicit = BooleanField('implicit',
                         default=0,
                         index="lens_catalog/FieldIndex:brains",
                         widget=BooleanWidget(label="Also select contents?",
                                              description=implicitdesc,
                                              i18n_domain="rhaptos")
                         )

namespace_tagsdesc = "Add words you associate with this content. Separate each tag with a space."
namespaceTags = LinesField('namespaceTags',
                #required=1,
                searchable=1,
                index="lens_catalog/KeywordIndex:brains",
                widget=LinesWidget(label="Namespace Tags",             
                                    description=namespace_tagsdesc,
                                    i18n_domain="rhaptos"),
                )

# TODO: there's a TagIndex at http://svn.plone.org/svn/collective/Tags/trunk/indexes.py
tagsdesc = "Add words you associate with this content. Separate each tag with a space."
tags = LinesField('tags',
                #required=1,
                searchable=1,
                index="lens_catalog/KeywordIndex:brains",
                widget=LinesWidget(label="Tags",              # TODO: TagsWidget?
                                    description=tagsdesc,
                                    i18n_domain="rhaptos"),
                )

commentdesc = ""
comment = TextField('comment',         # overrides default
              required = 0,
              index="lens_catalog/:brains",
              widget=TextAreaWidget(label="Comments",
                                    description=commentdesc,)
              )

plaincomment= ComputedField('plainComment',
                searchable=0,
                index="lens_catalog/:brains",
                expression="context.getComment(mimetype='text/plain')",
                widget=StringWidget(modes=()),
                )

allowedRolesAndUsers= ComputedField('allowedRolesAndUsers',
                accessor="allowedRolesAndUsers",
                searchable=0,
                expression="context.allowedRolesAndUsers()",
                index="lens_catalog/KeywordIndex:brains",
                widget=StringWidget(modes=()),
                )

contentAuthors= ComputedField('contentAuthors',
                accessor="getContentAuthors",
                searchable=0,
                expression="context.getContentAuthors()",
                index="lens_catalog/:brains",
                widget=StringWidget(modes=()),
                )

approveddesc = ""
approved = BooleanField('approved',
                         default=False,
                         write_permission=ApproveSelectedContent,
                         index="lens_catalog/FieldIndex:brains",
                         widget=BooleanWidget(label="Approve content?",
                                              description=approveddesc,
                                              i18n_domain="rhaptos")
                         )

approvedBydesc = ""
approvedBy = StringField('approvedBy',
                         default=False,
                         write_permission=ApproveSelectedContent,
                         index="lens_catalog/FieldIndex:brains",
                         widget=StringWidget(label="Approved by",
                                              description=approvedBydesc,
                                              i18n_domain="rhaptos")
                         )

ratingdesc = ""
rating = ComputedField('rating',
            accessor='getRating',
            index="lens_catalog/FieldIndex:brains",
            widget=ComputedWidget(label="Rating",
               description=ratingdesc,
               i18n_domain="rhaptos")
            )

schema = BaseFolderSchema.copy() +  Schema((contentId, title, versionStart, versionStop, versionLastSeen,
                                     implicit, namespaceTags, tags, comment, plaincomment, allowedRolesAndUsers, contentAuthors, approved, approvedBy, rating))

class SelectedContent(BaseFolder):  # should it be BTree?
    """Entry present in a set of selected content.
    Selected collection content may contain an auto-generated list of
    'SelectedContent's to provide implicit endorsement.
    """
    archetype_name = "Selected Content"
    use_folder_tabs = 1
    allowed_content_types = []

    schema = schema

    security = AccessControl.ClassSecurityInfo()
    security.setPermissionDefault(View, [])

    security.declareProtected(View, 'computedTitle')
    def computedTitle(self):  # TODO: very similar to PCP...  # TODO: could store value, and change on setContentId
        try:
            orig_title = self.getContent().Title()
            return orig_title or "#untitled#"
        except (KeyError, AttributeError):
            return '#invalid module: "%s"#' % self.getContentId()

        return "(no module)"

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

    def getContentAuthors(self):
       """
       Create comma separated list of authors for display in Atom feed
       """
       content = self.getContent()
       nameList = ''
       if content != None:
           authorTup = content.authors
           authorList = self._decodeTuple(authorTup)
           
           mship = getToolByName(self, 'portal_membership')
           count = 1
           
           for id in authorList:
               user = mship.getMemberById(id)
               name = user.getProperty('fullname','')
               if count < len(authorList) and len(authorList) > 1:
                   nameList += name
                   nameList += ', '
               else:
                   nameList += name
               count+=1    
       
       return nameList  
    
    #security.declareProtected(Edit, 'setContentId')  # TODO: ?
    def setContentId(self, value, **kwargs):
        """Override the method here to rename object to the id of the content."""
        if value: self.setId(value)
        return self.getField("contentId").set(self, value, **kwargs)

    security.declarePrivate('getContent')
    def getContent(self):  # TODO: (almost) the same as RhaptosCollection
        """Return the actual object at which this object "points"."""
        content = getToolByName(self, 'content')
        if not(getattr(self,'_v_content',None)):
            try:
                self._v_content =  content.getRhaptosObject(self.getContentId(), self.getRawVersionStop() or 'latest')
            except KeyError, details:
                return None

        return self._v_content.__of__(content)

    security.declareProtected(View, 'getInnerType')
    def getInnerType(self):
        """Return the type of the content object at which this object "points"."""
        try:
            ctype = self.getContent().portal_type
            return ctype or "#unknown#"
        except (KeyError, AttributeError):
            return '#invalid module: "%s"#' % self.getContentId()

        return ""

    security.declareProtected(View, 'getInnerIcon')
    def getInnerIcon(self):
        """Return the icon of the content object at which this object "points".
        Preferred to getContent().getIcon() because we may cache this internally in the future
        and thus avoid a getContent call.
        """
        try:
            icon = self.getContent().getIcon(1)
            return icon or ""
        except (KeyError, AttributeError):
            pass

        return ""

    security.declareProtected(View, 'representsContainer')
    def representsContainer(self):
        """True iff the "inner type" is a Collection. (But may in the future want to be true for similar types.)"""
        return self.getInnerType() == 'Collection'

    security.declarePrivate('moduleLocation')
    def moduleLocation(self):  # TODO: (almost) the same as RhaptosCollection
        m = self.getContent()
        if m:
            return m.url()
        else:
            return ""

    security.declareProtected(View, 'moduleVersions')
    def moduleVersions(self):  # TODO: (almost) the same as RhaptosCollection
        """A DisplayList of module versions"""
        retval = []
        try:
            retval = [(elt.version,elt.version) for elt in self.content.getHistory(self.getContentId())]
        except:
            pass
        return DisplayList(retval)

    security.declareProtected(View, 'moduleVersionsAndNone')
    def moduleVersionsAndNone(self):
        """A DisplayList of module versions and a choice for none (at top)."""
        versions = DisplayList(((NOVERSION, "---"),)) + self.moduleVersions()
        return versions

    security.declarePrivate('currentVersion')
    def currentVersion(self):
        """The first version for this content, or None if we don't know our content."""
        versions = self.moduleVersions().keys()
        if versions:
          return versions[-1]
        return None

    # POST on this level is intentionally a no-op
    security.declareProtected(View, 'atomPost')
    def atomPost(self, content):
        return

    security.declareProtected(ModifyPortalContent, 'PUT')
    def PUT(self, REQUEST):
         """retrieves put information and updates the lens content appropriately """
	 text = REQUEST.get('BODY', '')
	 dom = minidom.parseString(text)

	 retval = editEntryFromDom(dom, self, True)
	 if not retval is None:
             REQUEST.response.setStatus('BadRequest') 
	     REQUEST.response.appendHeader('error', retval)

         return
     
    def _decodeTuple(self,tupleToDecode):
         """ 
         Convert all values in the tuple to ASCII.
         This is to prevent Unicode values from causing an error.
         Parameter:
             tupleToDecode - the tuple to convert
         """
         
         return tuple([i.encode("ascii") for i in tupleToDecode])

    def getRating(self):      
        content = self.getContent()
        if content is None:
            # This should never happen
            return 0.0
        return getattr(content, 'rating', lambda:0.0)()

registerType(SelectedContent)
