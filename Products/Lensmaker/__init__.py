"""
Initialization and package-wide constants.

Author: J. Cameron Cooper (jccooper@rice.edu)
Copyright (C) 2007 Rice University. All rights reserved.

This software is subject to the provisions of the GNU Lesser General
Public License Version 2.1 (LGPL).  See LICENSE.txt for details.
"""

from Globals import package_home
from Products.Archetypes.public import process_types, listTypes
from Products.CMFCore import utils
from Products.CMFCore.DirectoryView import registerDirectory

from Products.GenericSetup import EXTENSION
from Products.GenericSetup import profile_registry
from Products.CMFPlone.interfaces.siteroot import IPloneSiteRoot

from config import SKINS_DIR, GLOBALS, PROJECTNAME
from config import ADD_CONTENT_PERMISSION, ADD_LENS_SELECTED_CONTENT_PERMISSION

import monkeypatch
#import indexesMonkeypatch

registerDirectory(SKINS_DIR, GLOBALS)

import BooleanWorkflow

import LensTool
tools = (LensTool.LensTool,)

# register fields/widgets/validators/etc
import VersionField
import SimpleHtmlValidator

#permissions
import LensPermissions

def initialize(context):
    ##Import Types here to register them
    import ContentSelectionLens
    import FavoritesLens
    import SelectedContent
    import ContainingFolders
    import TagNamespace

    content_types, constructors, ftis = process_types(
        listTypes(PROJECTNAME),
        PROJECTNAME)

    special_content_types = []
    normal_content_types = []
    for c in content_types:
        if c.meta_type == 'SelectedContent':
            special_content_types.append(c)
        else:
            normal_content_types.append(c)

    utils.ContentInit(
        '%s Content' % PROJECTNAME,
        content_types      = normal_content_types,
        permission         = ADD_CONTENT_PERMISSION,
        extra_constructors = constructors,
        fti                = ftis,
        ).initialize(context)

    utils.ContentInit(
        '%s Content' % PROJECTNAME,
        content_types      = special_content_types,
        permission         = ADD_LENS_SELECTED_CONTENT_PERMISSION,
        extra_constructors = constructors,
        fti                = ftis,
        ).initialize(context)

    utils.ToolInit('%s Tool' % PROJECTNAME,
                    tools = tools,
                    icon='tool.gif'
                    ).initialize(context)

    profile_registry.registerProfile('default',
                                     'Lensmaker',
                                     'Extension profile for Lensmaker',
                                     'profiles/default',
                                     'Lensmaker',
                                     EXTENSION)

from Extensions import Install  # check syntax on startup
del Install
