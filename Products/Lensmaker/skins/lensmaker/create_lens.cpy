## create_lens.py : Driver to create a new lens
##parameters=

from AccessControl import Unauthorized
from Products.Lensmaker.LensPermissions import AddQualityLens

ltool = context.lens_tool
namedfolder = ltool.getIndividualFolder()
member = context.portal_membership.getAuthenticatedMember()
if str(member) == 'Anonymous User':
    raise Unauthorized

# we emulate createObject, mostly because we can figure out what exactly it created
type_name = "ContentSelectionLens"
tmpid = context.generateUniqueId(type_name)
o = namedfolder.restrictedTraverse('portal_factory/' + type_name + '/' + tmpid)
#o.setTitle('(Untitled)')

fullname = member.getProperty('fullname', None)
if fullname: o.setTitle("%s's Lens" % fullname)

if member.has_permission(AddQualityLens, context):
    state.setStatus('choose')

return state.set(context=o)
