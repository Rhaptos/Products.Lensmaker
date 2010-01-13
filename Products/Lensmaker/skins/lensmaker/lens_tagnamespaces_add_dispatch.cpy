## Handle submissions from lens_tagnamespaces form
##parameters=

request = context.REQUEST

folder = context['tag-namespaces']
id = folder.generateUniqueId('TagNamespace')
#folder.invokeFactory(
#        type_name='TagNamespace', 
#        id=id)
#o = folder.restrictedTraverse('portal_factory/TagNamespace/' + id)

#request.set('selected_ids', [id])
request.set('new_id', id)
#return state.set(status='success')
return state.set(status='success')
