## Script (Python) "validate_reviewers"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=validates lens reviewers

REQUEST=context.REQUEST
errors = {}

add = REQUEST.get('ids',[])
delete = REQUEST.get('delete', [])

if not add and not delete:
    psm = context.translate("message_no_one_selected", domain="rhaptos", default="No one selected.")
    return state.set(status='failure', portal_status_message=psm)
else:
    return state
