from AccessControl import Unauthorized
from Products.CMFCore.utils import getToolByName

checkPermission = getToolByName(context,'portal_membership').checkPermission

if not checkPermission('Modify portal content', context):
    raise Unauthorized, "You are not allowed to edit this content"

return True