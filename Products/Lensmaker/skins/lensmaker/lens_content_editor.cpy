## lens_content_editor.py : Handle submissions from lens_content_edit form
##parameters=

request = context.REQUEST

obj_ids = request.get('obj_ids', None)
if not obj_ids: return "Invalid submission."

#del_list = request.get('del_list', [])
#obj_ids = [x for x in obj_ids if x not in del_list]  # del_list goes away when used! so filter obj_ids first.

#context.manage_delObjects(del_list)

for objid in obj_ids:
    tags = request.get("%s-tags" % objid, '')
    # namespaceTags lookup is different since we re-use a macro with 
    # differently named inputs
    namespaceTags=request.get('%s/%s-namespaceTags' % ('/'.join(context.getPhysicalPath()), objid), [])
    comment = request.get("%s-comment" % objid)
    implicit = request.get("%s-implicit" % objid)
    versionStart = request.get("%s-versionStart" % objid)
    versionStop = request.get("%s-versionStop" % objid)

    tags = tags.split()

    # if you get the versions backwards, we set them straight # TODO: should we error instead?
    if versionStop:  # ...not latest
        lstart = [int(x) for x in versionStart.split('.')]
        lstop  = [int(x) for x in versionStop.split('.')]
        if lstart > lstop:
            tmp = versionStart
            versionStart = versionStop
            versionStop = tmp
            #state.set(status='failure', portal_status_message="%s > %s" % (lstart, lstop))
            # ... but we don't have error handling in the form

    obj = context[objid]
    obj.setComment(comment, mimetype="text/html")  # rely on reindex in next step
    obj.update(tags=tags, implicit=implicit, versionStart=versionStart, 
            versionStop=versionStop, namespaceTags=namespaceTags)

context.setModificationDate()
context.reindexObject(idxs=['modified'])

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
