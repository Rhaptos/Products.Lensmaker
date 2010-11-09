"""
Derivative lens type, primarily for restricting available fields.
Used for storing "Favorites": bookmarks, etc.

Author: J. Cameron Cooper (jccooper@rice.edu)
Copyright (C) 2008 Rice University. All rights reserved.

This software is subject to the provisions of the GNU Lesser General
Public License Version 2.1 (LGPL).  See LICENSE.txt for details.
"""
import AccessControl

from Products.CMFCore.permissions import View, ModifyPortalContent
from Products.CMFCore.Expression import Expression
from Products.Archetypes.public import registerType
from Products.Archetypes.public import DisplayList

from ContentSelectionLens import ContentSelectionLens, schema as BaseSchema
from LensPermissions import EditHiddenFields

FAVORITE_ID = "favorites"
FAVORITES_TYPES = DisplayList((
                              ("Favorites","Favorites"),
                              ))

schema = BaseSchema.copy()

# in Favorites, we want to make uneditable pretty much everything but:
#  - tag cloud, notify on change, language
# a few things get defaults, like id, title, displayName
# category is set to a special value
# state should always be private
# we do the hiding with a write permission that's not available to Owner

# hide
schema['id'].default = FAVORITE_ID
schema['id'].write_permission = EditHiddenFields

schema['displayName'].default = "My Favorites"
schema['displayName'].write_permission = EditHiddenFields

schema['title'].default = "My Favorites"
schema['title'].write_permission = EditHiddenFields

schema['description'].write_permission = EditHiddenFields

schema['logo'].write_permission = EditHiddenFields
schema['banner'].write_permission = EditHiddenFields
schema['bannerColor'].write_permission = EditHiddenFields

schema['url'].write_permission = EditHiddenFields

schema['urlText'].write_permission = EditHiddenFields

schema['notifyOfChanges'].default = 0

schema['category'].default = FAVORITES_TYPES[0]
schema['category'].vocabulary = FAVORITES_TYPES
schema['category'].write_permission = EditHiddenFields

schema['tagScheme'].default = "FreeForm"

# keep, but rearrange
schema['language'].schemata = 'settings'
schema['noTagCloud'].schemata = 'settings'
#schema['notifyOfChanges'].schemata = 'settings'

class FavoritesLens(ContentSelectionLens):
    """A restricted sort of lens, for holding personal bookmarks, etc."""
    archetype_name = "Favorites Lens"
    content_icon = 'star.png'

    security = AccessControl.ClassSecurityInfo()

    schema = schema

    actions = (
               {'id': 'view',
                'title': 'View',
                'action': Expression('string:${object_url}/lens_view'),
                'permissions': (View,),
                'visible': 0},
               {'id': 'contents',
                'title': 'Edit lens contents',
                'action': Expression('string:${object_url}/favorite_content_view'),
                'permissions': (ModifyPortalContent,)},
               {'id': 'edit',
                'title': 'Edit lens properties',
                'action': Expression('string:${object_url}/lens_edit'),
                'permissions': (ModifyPortalContent,)},
               {'id': 'preview',
                'title': 'Preview lens',
                'action': Expression('string:${object_url}/lens_preview'),
                'permissions': (ModifyPortalContent,)},
               {'id': 'metadata',  # turn off 'properties' tab
                'visible': 0},
              )

    aliases = {
          '(Default)'  : '',
          'edit'       : 'lens_edit',
          'gethtml'    : '',
          'index.html' : '',
          'properties' : '',
          'sharing'    : '',
          'view'       : 'lens_view',
          'contents'   : 'favorite_content_view',
          }

    security.declarePublic('workflowStateEditable')
    def workflowStateEditable(self):
          """Return a boolean whether or not the user may edit the workflow state of this lens."""
          return False # not very smart at the moment, but accurate.

    security.declarePublic('suggestId')
    def suggestId(self):
          """Return the suggested id of this lens; used particularly for portal_factory create."""
          return FAVORITE_ID

    security.declareProtected(View, 'notifyRead')
    def notifyRead(self, collectionId, moduleId):
        """The user read 'moduleId' in 'collectionId'. If we have that collection, mark that module
        as the "last read". No return value.
        """
        if collectionId:
            entry = getattr(self, collectionId, None)
            if not entry is None:
                if getattr(entry, 'lastRead', None) != moduleId:  # avoid touching object if possible
                    entry.lastRead = moduleId

    security.declareProtected(View, 'getLastRead')
    def getLastRead(self, collectionId):
        """Return the 'moduleId' in 'collectionId' (if we have that collection) "last read"
        by the owner. If no collection by that id, return None.
        """
        if collectionId:
            entry = getattr(self, collectionId, None)
            if not entry is None:
                moduleId = getattr(entry, 'lastRead', None)
                return moduleId

registerType(FavoritesLens, 'Lensmaker')
