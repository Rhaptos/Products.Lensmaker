## lens_view.py : Usually display lens_folder_view. If only one lens, show it.
## Respects context.getCategory, so must be in a LensMajorContainer.
##parameters=

organisers = context.objectIds(spec='LensOrganizer')
if len(organisers) > 0:
    return context.lensorganizer_listing()

onlyCat = context.REQUEST.get('getCategory', context.getCategory())
path = '/'.join(context.getPhysicalPath())

args = {'path':path, 'all':True, 'inclzero':True}
if onlyCat: args['category'] = onlyCat
elts = context.lens_tool.getListsBy(**args)

from Products.CMFCore.utils import getToolByName
mtool = getToolByName(context, 'portal_membership')
user = mtool.getAuthenticatedMember()
mine = user.getId() == context.getId()

if (not mine or onlyCat) and len(elts) == 1:
    lensobj = elts[0].getObject()
    context.REQUEST.set('PUBLISHED', lensobj)
    return lensobj.lens_view()

return context.lens_folder_view(showonly=onlyCat, mine=mine)
