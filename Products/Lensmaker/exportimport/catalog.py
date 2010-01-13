
from Products.CMFCore.utils import getToolByName
from Products.GenericSetup.interfaces import IBody
from zope.component import queryMultiAdapter

filename = 'config-lenscatalog.xml'

def importCatalog(context):
    portal = context.getSite()
    body = context.readDataFile(filename)
    if body is None:
        logger = context.getLogger('config-lenscatalog')
        logger.info('Nothing to import')
        return
    importer = queryMultiAdapter((portal.lens_catalog, context), IBody)
    if importer:
        importer.name = 'config-lenscatalog'
        importer.filename = filename
        importer.body = body


def exportCatalog(context):
    portal = context.getSite()
    if 'lens_catalog' not in portal.objectIds():
        logger = context.getLogger('config-lenscatalog')
        logger.info('Nothing to export.')
        return
    exporter = queryMultiAdapter((portal.lens_catalog, context), IBody)
    if exporter:
        exporter.name = 'config-lenscatalog'
        body = exporter.body
        if body is not None:
            context.writeDataFile(filename, body, exporter.mime_type)


def createCatalog(context):
    if context.readDataFile('lensmaker.txt') is None:
        return
    logger = context.getLogger('create-lenscatalog')
    portal = context.getSite()
    if 'lens_catalog' not in portal.objectIds():
        portal.manage_addProduct['ZCatalog'].manage_addZCatalog(
            'lens_catalog', 'Lens catalog')
        logger.info('Created Lens Catalog')

def setCatalog(context):
    if context.readDataFile('lensmaker.txt') is None:
        return
    portal = context.getSite()
    archetype_tool = getToolByName(portal, 'archetype_tool')
    archetype_tool.setCatalogsByType('ContentSelectionLens',['lens_catalog'])
    archetype_tool.setCatalogsByType('SelectedContent',['lens_catalog'])
    archetype_tool.setCatalogsByType('FavoritesLens',['lens_catalog'])
    archetype_tool.setCatalogsByType('TagNamespace',['lens_catalog'])

