
from Products.CMFCore.utils import getToolByName

try: from zExceptions import BadRequest
except ImportError: BadRequest = 'BadRequest'

def createContent(context):
    if context.readDataFile('lensmaker.txt') is None:
        return
    logger = context.getLogger('lensmaker')
    portal = context.getSite()
    lens_tool = getToolByName(portal, 'lens_tool')
    lenses = lens_tool.getMajorContainer()
    try:
        # mostly to deal with problems with Yummy
        portal.invokeFactory('LensMajorContainer', id='lenses', title="Lenses")
        lenses = lens_tool.getMajorContainer()
    except BadRequest:
        logger.info(" - skipping /lenses - already exists") # already exists

    try:
        portal.invokeFactory('LensRedirectContainer', id='endorsements',
                title="Endorsements")
        endorsements = portal['endorsements']
        endorsements.setCategory('Endorsement')
    except BadRequest:
        logger.info(" - skipping /endorsements - already exists") # already exists

    try:
        portal.invokeFactory('LensRedirectContainer', id='affiliations',
                title="Affiliations")
        endorsements = portal['affiliations']
        endorsements.setCategory('Affiliation')
    except BadRequest:
        logger.info(" - skipping /affiliations - already exists") # already exists

    try:
        portal.invokeFactory('LensRedirectContainer', id='memberlists',
                title="Member lists")
        endorsements = portal['memberlists']
        endorsements.setCategory('List')
    except BadRequest:
        logger.info(" - skipping /memberlists - already exists") # already exists

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
            lens_folder.manage_addProperty('left_slots', left_slots,
                    type='lines')
        except BadRequest:
            lens_folder.manage_changeProperties(left_slots=left_slots)
        try:
            lens_folder.manage_addProperty('right_slots', right_slots,
                    type='lines')
        except BadRequest:
            lens_folder.manage_changeProperties(right_slots=right_slots)

