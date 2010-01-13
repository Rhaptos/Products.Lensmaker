## Script (Python) "validate_lens_add_select"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=lens_paths=[]
##title=validates selection of open lens

if not lens_paths:
    psm = context.translate("message_please_select_open_lens", domain="rhaptos", default="Please select an open lens.")
    return state.set(status='failure', portal_status_message=psm)

return state
