## Python Script "favorites_get"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=Get the Favorites lens object, either portal_factory or real (if authenticated)
##

anonymous = context.portal_membership.isAnonymousUser()
if anonymous:
    return None

ltool = context.lens_tool
type_name = "FavoritesLens"
lid = "favorites"
namedfolder = ltool.getIndividualFolder()

if getattr(namedfolder, lid, None) is None:
    #namedfolder.invokeFactory(type_name=type_name, id=lid)  # alternate method: creating an actual object
    tmpid = context.generateUniqueId(type_name)
    o = namedfolder.restrictedTraverse('portal_factory/' + type_name + '/' + tmpid)
else:
    o = namedfolder[lid]

return o