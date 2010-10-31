"""
Product configuration

Author: J. Cameron Cooper (jccooper@rice.edu)
Copyright (C) 2007 Rice University. All rights reserved.

This software is subject to the provisions of the GNU Lesser General
Public License Version 2.1 (LGPL).  See LICENSE.txt for details.
"""

from Products.CMFCore.permissions import AddPortalContent
from Products.Archetypes.public import DisplayList
from Products.PloneLanguageTool import availablelanguages

ADD_CONTENT_PERMISSION = AddPortalContent
ADD_LENS_SELECTED_CONTENT_PERMISSION = 'Add lens selected content'

PROJECTNAME = "Lensmaker"    # this and an import in Extensions.Install are the only places product name appears
SKINS_DIR = 'skins'

GLOBALS = globals()

KNOWN_LENS_TYPES = ['ContentSelectionLens', 'FavoritesLens']  # TODO: this can be smarter

NO_CAT_TOKEN = ""  # logic in lenses_listing, lens_folder currently requires this to be a false value
QUALITY_LENSES = DisplayList((
                              ("Endorsement","Endorsement"),
                              ("Affiliation","Affiliation"),
                              ))

LENS_TYPES = QUALITY_LENSES + DisplayList(( ("List","List"),))

LENS_TYPES_OR_NONE = DisplayList(((NO_CAT_TOKEN,'--'),)) + LENS_TYPES

TAGNAMESPACE_DELIMITER = '::'

TAG_SCHEMES = DisplayList ((
        ('FreeForm','Freeform Tags'), 
        ('Vocabulary', 'Tag Vocabularies'),
        ))

