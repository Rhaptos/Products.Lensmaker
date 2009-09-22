"""
Monkey patches necessary for Lensmaker operation.

Author: J. Cameron Cooper (jccooper@rice.edu)
Copyright (C) 2007 Rice University. All rights reserved.

This software is subject to the provisions of the GNU Lesser General
Public License Version 2.1 (LGPL).  See LICENSE.txt for details.
"""

from zLOG import LOG, INFO

# AT in 'reindexObjectSecurity' calls a method on the catalog that is only available in portal_catalog
# Fix this to work with regular ZCatalogs as well (a bug that should be fixed in AT)
from Acquisition import aq_base
from Products.CMFCore.utils import getToolByName
from Products.Archetypes.debug import log
from Products.Archetypes.config import TOOL_NAME

from Products.Archetypes.CatalogMultiplex import CatalogMultiplex

if not getattr(CatalogMultiplex, '_old_reindexObjectSecurity', None):
    LOG("Lensmaker", INFO, "Patching Products.Archetypes.CatalogMultiplex.CatalogMultiplex.reindexObjectSecurity")

    def reindexObjectSecurity(self, skip_self=False):
        """update security information in all registered catalogs.
        """
        at = getToolByName(self, TOOL_NAME, None)
        if at is None:
            return

        catalogs = [c for c in at.getCatalogsByType(self.meta_type)
                                if c is not None]
        path = '/'.join(self.getPhysicalPath())

        for catalog in catalogs:
            unrestrictedSearchResults = getattr(catalog, 'unrestrictedSearchResults', catalog.searchResults) # PATCH
            for brain in unrestrictedSearchResults(path=path):
                brain_path = brain.getPath()
                if brain_path == path and skip_self:
                    continue

                # Get the object
                if hasattr(aq_base(brain), '_unrestrictedGetObject'):
                    ob = brain._unrestrictedGetObject()
                else:
                    # BBB: Zope 2.7
                    ob = self.unrestrictedTraverse(brain_path, None)
                if ob is None:
                    # BBB: Ignore old references to deleted objects.
                    # Can happen only in Zope 2.7, or when using
                    # catalog-getObject-raises off in Zope 2.8
                    log("reindexObjectSecurity: Cannot get %s from catalog" %
                        brain_path, level=WARNING)
                    continue

                # Recatalog with the same catalog uid.
                # PATCH:
                lst = [i for i in self._cmf_security_indexes if i in c.indexes()]   # only valid indexes
                if lst: catalog.catalog_object(ob, uid=brain_path, idxs=lst, update_metadata=0)
                # this is only valid for portal_catalog...
                #catalog.reindexObject(ob, idxs=self._cmf_security_indexes, update_metadata=0, uid=brain_path)
    
    CatalogMultiplex._old_reindexObjectSecurity = CatalogMultiplex.reindexObjectSecurity
    CatalogMultiplex.reindexObjectSecurity = reindexObjectSecurity