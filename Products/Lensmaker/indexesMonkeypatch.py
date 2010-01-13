"""
Monkey patches necessary for catalog improvements. See
http://web.archive.org/web/20050207213956/plone.org/documentation-old/howto/OptimizingCatalogs

Author: J. Cameron Cooper (jccooper@rice.edu)
Copyright (C) 2007 Rice University. All rights reserved.

This software is subject to the provisions of the GNU Lesser General
Public License Version 2.1 (LGPL).  See LICENSE.txt for details.
"""

from zLOG import LOG, INFO
from DateTime import DateTime

from Products.CMFDefault.DublinCore import DefaultDublinCoreImpl

## cannot monket patch __ attrs, I guess.
#if not getattr(DefaultDublinCoreImpl, '_old___CEILING_DATE', None):
    #LOG("Lensmaker", INFO, "Patching CMFDefault.DublinCore.DefaultDublinCoreImpl.__CEILING_DATE")
    
    #DefaultDublinCoreImpl._old___CEILING_DATE = DefaultDublinCoreImpl.__CEILING_DATE
    #DefaultDublinCoreImpl.__CEILING_DATE = DateTime(2500, 0)

if not getattr(DefaultDublinCoreImpl, '_old_expires', None):
    LOG("Lensmaker", INFO, "Patching CMFDefault.DublinCore.DefaultDublinCoreImpl.expires")
    
    DefaultDublinCoreImpl.__CEILING_DATE = DateTime(2500, 0)
    
    # exactly the same! just changing CEILING
    def expires( self ):
        """
            Dublin Core element - date resource expires,
              returned as DateTime.
        """
        date = getattr( self, 'expiration_date', None )
        return date is None and self.__CEILING_DATE or date
    
    DefaultDublinCoreImpl._old_expires = DefaultDublinCoreImpl.expires
    DefaultDublinCoreImpl.expires = expires

from Products.CMFCore.CatalogTool import CatalogTool
if not getattr(CatalogTool, '_old_searchResults', None):
    LOG("Lensmaker", INFO, "Patching CMFCore.CatalogTool.CatalogTool.searchResults")

    from Products.ZCatalog.ZCatalog import ZCatalog
    from Products.CMFCore.utils import _checkPermission, _getAuthenticatedUser
    from Acquisition import aq_base
    from Products.CMFCore.CMFCorePermissions import AccessInactivePortalContent

    # searchResults has inherited security assertions.
    def searchResults(self, REQUEST=None, **kw):
        """
            Calls ZCatalog.searchResults with extra arguments that
            limit the results to what the user is allowed to see.
        """
        user = _getAuthenticatedUser(self)
        kw[ 'allowedRolesAndUsers' ] = self._listAllowedRolesAndUsers( user )

        if not _checkPermission( AccessInactivePortalContent, self ):
            base = aq_base( self )
            #now = DateTime()
            #if hasattr( base, 'addIndex' ):   # Zope 2.4 and above
                #kw[ 'effective' ] = { 'query' : now, 'range' : 'max' }
                #kw[ 'expires'   ] = { 'query' : now, 'range' : 'min' }
            #else:                             # Zope 2.3
                #kw[ 'effective'      ] = kw[ 'expires' ] = now
                #kw[ 'effective_usage'] = 'range:max'
                #kw[ 'expires_usage'  ] = 'range:min'
            kw['effectiveRange'] = DateTime()

        return apply(ZCatalog.searchResults, (self, REQUEST), kw)
    
    CatalogTool._old_searchResults = CatalogTool.searchResults
    CatalogTool.searchResults = searchResults
    CatalogTool.__call__ = searchResults  # may not be necessary, but I want to be sure