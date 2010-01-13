## Handle submissions from lens_tagnamespaces form
##parameters=

request = context.REQUEST

ids_list = request.get('selected_ids', [])

if not ids_list:
    return state.set(status='failure', portal_status_message="Please select one or more items to edit.")

return state.set(status='success')
