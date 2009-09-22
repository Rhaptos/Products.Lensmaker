## lens_content_editor.py : Handle submissions from lens_content_edit form
##parameters=

request = context.REQUEST

del_list = request.get('paths', [])

if not del_list:
    return state.set(status='failure', portal_status_message="No entries specified.")

psm = "Removed from list: %s." % ", ".join(del_list)  # del_list is blanked by manage_delObjects!
context.manage_delObjects(del_list)
context.setModificationDate()
context.reindexObject(idxs=['count', 'modified'])

return state.set(status='success', portal_status_message=psm)
