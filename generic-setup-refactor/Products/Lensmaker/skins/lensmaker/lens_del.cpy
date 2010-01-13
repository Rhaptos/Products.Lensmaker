## Script (Python) "lens_del"
##parameters=
##
## Delete the lens that is our context.

psm = "Successfully deleted lens '%s'." % context.getDisplayName()

parent = context.getParentNode()
parent.manage_delObjects([context.getId()])

return state.set(context=parent, portal_status_message=psm, status='success')
