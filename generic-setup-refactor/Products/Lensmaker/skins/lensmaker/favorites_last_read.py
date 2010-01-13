## Script (Python) "favorites_notify_read"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=collectionId=None
##title=Notify Favorites a Module is Read
##

## If we have a Favorites lens, check it for this collection. If we have that collection,
## get the "last read" module for the 'collectionId', as per favorites_notify_read.

from Products.CMFCore.utils import getToolByName

if collectionId is None:
    collectionId = getattr(context, 'objectId', None)

if collectionId:
    ltool = getToolByName(context, 'lens_tool')
    personal = ltool.getIndividualFolder(create=False)
    if personal:
        fav = getattr(personal, 'favorites', None)
        if not fav is None:
            return fav.getLastRead(collectionId)

return None