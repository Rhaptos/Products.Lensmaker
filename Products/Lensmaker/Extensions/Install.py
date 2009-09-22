"""
Installation script for QuickInstaller use, including upgrades.

Author: J. Cameron Cooper (jccooper@rice.edu)
Copyright (C) 2007 Rice University. All rights reserved.

This software is subject to the provisions of the GNU Lesser General
Public License Version 2.1 (LGPL).  See LICENSE.txt for details.
"""

from Products.Lensmaker.config import PROJECTNAME, GLOBALS

from Products.Archetypes.public import listTypes
from Products.Archetypes.Extensions.utils import installTypes, install_subskin
from Products.CMFCore.utils import getToolByName
from Products.CMFCore import CMFCorePermissions
from Products.CMFCore.Expression import Expression

from Products.ZCatalog.ZCatalog import ZCatalog
from Products.ZCTextIndex.ZCTextIndex import PLexicon, ZCTextIndex
from Products.ManagableIndex.KeywordIndex import KeywordIndex
from Products.ManagableIndex.FieldIndex import FieldIndex
from Products.ManagableIndex.ValueProvider import ExpressionEvaluator
from Products.ZCTextIndex.Lexicon import CaseNormalizer, StopWordAndSingleCharRemover
from Products.ZCTextIndex.HTMLSplitter import HTMLWordSplitter
from Products.ExternalMethod.ExternalMethod import ExternalMethod
try:
    from Products.QueueCatalog import QueueCatalog
    lens_cat_name = 'lens_catalog_real'
    queue_cat_name = 'lens_catalog'
except:
    lens_cat_name = 'lens_catalog'
    queue_cat_name = None

class Empty: pass

from StringIO import StringIO

from Products.Lensmaker.config import ADD_LENS_SELECTED_CONTENT_PERMISSION

try: from zExceptions import BadRequest
except ImportError: BadRequest = 'BadRequest'

import logging
logger = logging.getLogger('%s.Install' % PROJECTNAME)
def log(msg, out=None, severity=None):
    logger.info(msg)
    if out: print >> out, msg
    

def upgradeTool(portal, tool, out):
    """A stateless upgrade script, to be triggered when install recognizes the tool already exists.
    Doesn't care what version it is or is going to. If we need that, we'll have to detect versions
    somehow; maybe an attribute on the class or some info from the QuickInstaller.
    """
    #log("Upgrading existing X...", out)
    #log("Upgrade done.", out)
    pass

def addColumn(catalog, fieldname, *args, **kw):
    """Create a metadata field on the given catalog if it doesn't already exist.
    Call as you would 'catalog.addColumn'.
    Returns 'fieldname' if that name is actually added; None if it exists.
    """
    if fieldname not in catalog.schema():
        catalog.addColumn(fieldname, *args, **kw)
        return fieldname
    return None


def install(self):
    """Install method for this product. It should be kept idempotent; running it at any time should be safe.
    Also, necessary upgrades to existing data should be accomplished with a reinstall (running this!) if
    at all possible.
    """

    out = StringIO()

    urltool = getToolByName(self, 'portal_url')
    portal = urltool.getPortalObject();

    log("Starting %s install" % PROJECTNAME, out)

    catalog = getattr(portal, lens_cat_name, None)
    if catalog:
        log("...lens_catalog already exists", out)
    else:
        log("...creating lens_catalog", out)
        # Create the ZCatalog instance
        portal.manage_addProduct['ZCatalog'].manage_addZCatalog(lens_cat_name, 'Lens catalog')
        catalog = portal[lens_cat_name]
        lexicon = PLexicon('lexicon', '' , HTMLWordSplitter(), CaseNormalizer(), StopWordAndSingleCharRemover())
        catalog._setObject('lexicon', lexicon)

        ZCText_extras = Empty()
        ZCText_extras.doc_attr = 'fullname'
        ZCText_extras.index_type = 'Okapi BM25 Rank'
        ZCText_extras.lexicon_id = 'lexicon'
        
        log("...creating lens_catalog indices", out)
        catalog.addIndex('Title', 'TextIndex')
        catalog.addIndex('Type', 'FieldIndex')
        catalog.addIndex('portal_type', 'FieldIndex')
        catalog.addIndex('id', 'FieldIndex')
        catalog.addIndex('review_state', 'FieldIndex')
        catalog.addIndex('Creator', 'FieldIndex')
        catalog.addIndex('path', 'PathIndex', {'indexed_attrs':'getPhysicalPath'})
        catalog.addIndex('getCategory', 'FieldIndex')
        catalog.addIndex('modified', 'FieldIndex', {'indexed_attrs':'modification_date'})

    catalog = portal[lens_cat_name]
    if  not 'modified' in catalog.indexes():
        catalog.addIndex('modified', 'FieldIndex', {'indexed_attrs':'modification_date'})
        catalog.reindexIndex('modified', None)

    log("...setting/checking lens_catalog metadata fields", out)
    newmetadata = set([None])
    newmetadata.add(addColumn(catalog, 'Title'))
    newmetadata.add(addColumn(catalog, 'Type'))
    newmetadata.add(addColumn(catalog, 'portal_type'))
    newmetadata.add(addColumn(catalog, 'id'))
    newmetadata.add(addColumn(catalog, 'getId'))
    newmetadata.add(addColumn(catalog, 'review_state'))
    #newmetadata.add(addColumn(catalog, 'path'))
    newmetadata.add(addColumn(catalog, 'getCategory'))
    newmetadata.add(addColumn(catalog, 'UID'))
    newmetadata.remove(None)
    
    if newmetadata:
        log(".....added metadata fields: %s; updating catalog" % list(newmetadata), out)
        objs = catalog.searchResults()
        for brain in objs:
            obj = brain.getObject()
            catalog.catalog_object(obj, update_metadata=1, idxs=['Title'])
                                                            ## no idxs==all, so pick one cheap one
        log(".....update done on %s objects" % len(objs), out)


#TODO handle case where we move lens_catalog, so it exists, but is wrong type
    if queue_cat_name:
        if hasattr(portal,queue_cat_name):
            log("...lens_catalog queue already exists, leave it alone", out)
        else:
            portal.manage_addProduct['QueueCatalog'].manage_addQueueCatalog(queue_cat_name, 'Lens catalog queue', lens_cat_name)

    log("...installing types", out)

    # Move any existing objects from the portal_catalog to the lens_catalog
    selected_contents = [o.getObject() for o in self.portal_catalog(Type='Selected Content')]
    existing_lenses = [o.getObject() for o in self.portal_catalog(Type='Content Selection Lens')]
    for obj in selected_contents + existing_lenses:
        # Delete them from portal_catalog
        try:
            obj.unindexObject()
        except AttributeError: # The object must already be gone
            pass

    installTypes(self, out,
                 listTypes(PROJECTNAME),
                 PROJECTNAME,
                 refresh_references=0
                 )

    # Change the catalog they will live in
    self.archetype_tool.setCatalogsByType('ContentSelectionLens',['lens_catalog'])
    self.archetype_tool.setCatalogsByType('SelectedContent',['lens_catalog'])
    self.archetype_tool.setCatalogsByType('FavoritesLens',['lens_catalog'])
    self.archetype_tool.setCatalogsByType('TagNamespace',['lens_catalog'])

    ## this screws up the portal_catalog's review_state index for some reason, so we can't actually do this.
    #cat = getToolByName(self,'portal_catalog')
    #lenses = cat({'portal_type':'ContentSelectionLens'})
    #if lenses:
        #log( "%i lenses to reindex" % len(lenses), out)
    
        ## now reindex anything that was there
        #for brain in lenses:
            #brain.getObject().reindexObject()
    
    for obj in selected_contents + existing_lenses:
        # Add them to the new catalog
        try:
            obj.indexObject()
        except AttributeError:
            pass

    f_tool = getToolByName(portal, 'portal_factory')
    types = f_tool.getFactoryTypes()
    types['ContentSelectionLens'] = 1
    types['FavoritesLens'] = 1
    f_tool.manage_setPortalFactoryTypes(listOfTypeIds=types.keys())
    
    log("...installing subsksins", out)
    install_subskin(self, out, GLOBALS)

    log("...adding roles", out)
    portal._addRole('Endorser')

    log("...installing tool", out)
    try:
        portal.manage_addProduct[PROJECTNAME].manage_addTool('Lens Tool', None)
    except BadRequest:
        log("   - leaving existing Tool in place", out)
        #upgradeTool(portal, portal.toolname, out)
        pass # that's okay

    log("...adding workflow", out)
    lens_tool = getToolByName(portal, 'lens_tool')
    wf_tool = getToolByName(self, 'portal_workflow')
    wf_tool.manage_addWorkflow(id='boolean_workflow',
                                workflow_type='boolean_workflow (Boolean Workflow, DCWorkflow based)')
    wf_tool.setChainForPortalTypes(['FavoritesLens'], 'boolean_workflow')
    wf_tool.setChainForPortalTypes(['SelectedContent'], '')

    # Workflow installation copied from Archgenerated code
    try:
        installWorkflows = ExternalMethod('temp', 'temp',
                                          PROJECTNAME+'.InstallWorkflows',
                                          'installWorkflows').__of__(self)
    except NotFound:
        installWorkflows = None

    if installWorkflows:
        print >>out,'Workflow Install:'
        res = installWorkflows(self,self,out)
        print >>out,res or 'no output'
    else:
        print >>out,'no workflow install'

    # update permission mappings for extant lenses due to version-after-0.5.2 changes to workflow permissions
    # it might be appropriate to condition this on version in the future, or just plain drop it
    log(" - updating permissions on existing lenses", out) 
    wf = wf_tool.getWorkflowById('boolean_workflow')
    wfs = {wf.getId():wf}
    lenses = lens_tool.searchResults(portal_type="ContentSelectionLens")
    for brain in lenses:
        lens = brain.getObject()
        count = wf_tool._recursiveUpdateRoleMappings(lens, wfs)  # don't do it globally--naive tree walk v. slow

    log("...adding/configuring content", out)
    lenses = lens_tool.getMajorContainer()
    try:
        portal.invokeFactory('LensMajorContainer', id='lenses', title="Lenses")  # mostly to deal with problems with Yummy
        lenses = lens_tool.getMajorContainer()
    except BadRequest:
        log(" - skipping /lenses - already exists", out) # already exists

    try:
        portal.invokeFactory('LensRedirectContainer', id='endorsements', title="Endorsements")
        endorsements = portal['endorsements']
        endorsements.setCategory('Endorsement')
    except BadRequest:
        log(" - skipping /endorsements - already exists", out) # already exists
    
    try:
        portal.invokeFactory('LensRedirectContainer', id='affiliations', title="Affiliations")
        endorsements = portal['affiliations']
        endorsements.setCategory('Affiliation')
    except BadRequest:
        log(" - skipping /affiliations - already exists", out) # already exists
    
    try:
        portal.invokeFactory('LensRedirectContainer', id='memberlists', title="Member lists")
        endorsements = portal['memberlists']
        endorsements.setCategory('List')
    except BadRequest:
        log(" - skipping /memberlists - already exists", out) # already exists
  
    left_slots = ['context/workspaces_slot/macros/portlet']
    right_slots = [
            'here/portlet_login/macros/portlet',
            'here/portlet_loggedin/macros/portlet',
            'here/portlet_lenses/macros/portlet',
            'here/portlet_recentview/macros/portlet']
    for lens_cont_id in ['lenses','endorsements','affiliations','memberlists']:
        lens_folder = portal[lens_cont_id]
        # todo: refactor to use hasProperty and not BadRequest exception
        try:
            lens_folder.manage_addProperty('left_slots', left_slots, type='lines')
        except BadRequest:
            lens_folder.manage_changeProperties(left_slots=left_slots)
        try:
            lens_folder.manage_addProperty('right_slots', right_slots, type='lines')
        except BadRequest:
            lens_folder.manage_changeProperties(right_slots=right_slots)
    
    log("...configuring actions", out)
    pa_tool = getToolByName(portal, 'portal_actions')

    # modify and add by way of Generic Setup XML profile
    log(" - applying profile", out)
    setup_tool = getToolByName(portal, 'portal_setup')
    prevcontext = setup_tool.getImportContextID()
    setup_tool.setImportContext('profile-CMFPlone:plone')
    setup_tool.setImportContext('profile-Lensmaker:default')
    # FIXME: in the future, we would like to just run all steps. the existing steps, however,
    # are probably not re-install safe
    status = setup_tool.runImportStep('actions')
    log(status['messages']['actions'], out)
    setup_tool.setImportContext(prevcontext)

    # position lens tab actions
    # not very elegant, but  GS profile doesn't support action ordering
    log(" - moving actions", out)
    # view
    idx = 0
    idx_content = 0
    idx_lensestab_view = 0
    for a in pa_tool._actions:
        if a.id == 'content':
            idx_content = idx
        elif a.id == 'lensestab-viewing':
            idx_lensestab_view = idx
        idx += 1

    if idx_lensestab_view > idx_content + 1:
        log("Reposition lenses tab action for viewing", out)
        new_actions = pa_tool._cloneActions()
        action = new_actions[idx_lensestab_view]
        del new_actions[idx_lensestab_view]
        new_actions.insert(idx_content+1, action)
        pa_tool._actions = tuple(new_actions)
    
    # edit
    idx = 0
    idx_content = 0
    idx_lensestab_edit = 0
    for a in pa_tool._actions:
        if a.id == 'content':
            idx_content = idx
        elif a.id == 'lensestab-editing':
            idx_lensestab_edit = idx
        idx += 1

    if idx_lensestab_edit > idx_content + 1:
        log("Reposition lenses tab action for editing", out)
        new_actions = pa_tool._cloneActions()
        action = new_actions[idx_lensestab_edit]
        del new_actions[idx_lensestab_edit]
        new_actions.insert(idx_content+1, action)
        pa_tool._actions = tuple(new_actions)
    
    # move contents action to top
    log(" - type actions", out)
    types_tool = getToolByName(portal, 'portal_types')
    actions = types_tool.ContentSelectionLens._actions
    contents = None
    for a in actions:
        if a.id == 'contents':
            contents = a
    actions = [contents] + [act for act in actions if act != contents]
    types_tool.ContentSelectionLens._actions = actions
    
    actions = types_tool.FavoritesLens._actions
    contents = None
    for a in actions:
        if a.id == 'contents':
            contents = a
    actions = [contents] + [act for act in actions if act != contents]
    types_tool.FavoritesLens._actions = actions

    self.manage_permission(ADD_LENS_SELECTED_CONTENT_PERMISSION, ('Manager','Owner'), acquire=1)

    log("Successfully installed %s." % PROJECTNAME, out)
    return out.getvalue()
