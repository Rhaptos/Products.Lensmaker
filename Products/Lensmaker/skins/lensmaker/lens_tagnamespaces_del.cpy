## Handle submissions from lens_tagnamespaces form
##parameters=

request = context.REQUEST

del_list = request.get('selected_ids', [])

if not del_list:
    return state.set(status='failure', portal_status_message="No entries specified.")

psm = "Removed from list: %s." % ", ".join(del_list)  # del_list is blanked by manage_delObjects!
context['tag-namespaces'].manage_delObjects(del_list)

return state.set(status='success', portal_status_message=psm)
