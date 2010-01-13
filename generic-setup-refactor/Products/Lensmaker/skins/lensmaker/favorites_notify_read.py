## Script (Python) "favorites_notify_read"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=collectionId, moduleId
##title=Notify Favorites a Module is Read
##

## If we have a Favorites lens, check it for this collection. If we have that collection,
## inform the Favorites lens that we've just read 'moduleId' in 'collectionId'. It will
## note that as the "last read" module.

from Products.CMFCore.utils import getToolByName

ltool = getToolByName(context, 'lens_tool')
personal = ltool.getIndividualFolder(create=False)
if personal:
    fav = getattr(personal, 'favorites', None)
    if not fav is None:
        fav.notifyRead(collectionId, moduleId)