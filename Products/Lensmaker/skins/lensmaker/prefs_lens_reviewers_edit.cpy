## Script (Python) "prefs_lens_reviewers_edit"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=Edit lens reviewers
##

REQUEST=context.REQUEST

delete = REQUEST.get('delete', [])
deletebutton = REQUEST.get('prefs_reviewers_edit', None)

add = REQUEST.get('ids', [])
addbutton = REQUEST.get('addingaction', None)

reviewers = context.getReviewers()

if add and addbutton:
    for memberid in add:
        if memberid not in reviewers:
            reviewers.append(memberid)
    context.edit(reviewers=reviewers)

elif delete and deletebutton:
    for memberid in delete:
        if memberid in reviewers:
            reviewers.remove(memberid)
    context.edit(reviewers=reviewers)

psm = context.translate("message_lens_reviewers_updated", domain="rhaptos", default="Reviewers updated.")
return state.set(status='success', portal_status_message=psm, context=context)
