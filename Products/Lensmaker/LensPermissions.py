"""
Permissions for the Lensemaker Product

Author: Ross Reedstrom, Cameron Cooper
(C) 2007 Rice University

This software is subject to the provisions of the GNU Lesser General
Public License Version 2.1 (LGPL).  See LICENSE.txt for details.
"""

from Products.CMFCore.CMFCorePermissions import setDefaultRoles

from AccessControl import allow_module
allow_module('Products.Lensmaker.LensPermissions')

# Permissions
AddQualityLens = 'Add quality lens'
EditHiddenFields = 'Lensmaker: Edit Hidden Fields'
ApproveSelectedContent = 'Lensmaker: Approve Selected Content'

# Set up default roles for permissions
setDefaultRoles(AddQualityLens, ('Manager', 'Endorser'))
setDefaultRoles(EditHiddenFields, ('Manager',))
setDefaultRoles(ApproveSelectedContent, ('Manager','Owner','Reviewer'))

# allow some other permissions from Zope
from zExceptions import BadRequest
from OFS.CopySupport import CopyError
