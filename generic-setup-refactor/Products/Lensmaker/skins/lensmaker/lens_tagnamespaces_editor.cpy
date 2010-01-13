## Handle submissions from lens_tagnamespaces_edit form
##parameters=

import logging
logger = logging.getLogger("TagNamespace")
request = context.REQUEST

obj_ids = request.get('obj_ids', None)
if not obj_ids: return "Invalid submission."

new_id = request.get('new_id', None)
logger.info("New id = %s", new_id)
if not new_id:
    for objid in obj_ids:
        title = request.get("%s-title" % objid, '').strip()
        prefix = request.get("%s-prefix" % objid, '').strip()
        tags = request.get("%s-tags" % objid, [])
        tags = [t.strip() for t in tags if t.strip()]

        obj = context['tag-namespaces'][objid]
        obj.processForm(
                values=dict(id=objid, title=title, prefix=prefix, tags=tags))
else:
    title = request.get("%s-title" % new_id, '').strip()
    prefix = request.get("%s-prefix" % new_id, '').strip()
    tags = request.get("%s-tags" % new_id, [])
    tags = [t.strip() for t in tags if t.strip()]

    obj_path = request.get('obj_paths')[0]
    obj = context.portal_url.getPortalObject().restrictedTraverse(obj_path)
    folder = context['tag-namespaces']
    new_context = folder.portal_factory.doCreate(obj, new_id)
    new_context.processForm(
        values=dict(id=new_id, title=title, prefix=prefix, tags=tags))



#Calculate the redirect URL, to avoid any extra parameters.
#If you add anything here, make sure it has a : in it.
actions = context.portal_actions.listFilteredActionsFor(context)['object']
action = [x for x in actions if x['id'] == 'contents'][0]
viewurl = action['url']
next_action='redirect_to:string:%s' % viewurl
ops={}
for op in ['b_start:int','b_size:int']:
    rop = request.get(op[:op.index(':')],0)
    if rop:
        ops[op]=str(rop)
qstr='&'.join([k+'='+v for k,v in ops.items()])

return state.set(status='success', portal_status_message="Changed",
                 next_action=next_action + (qstr and '?'+qstr or ''))
