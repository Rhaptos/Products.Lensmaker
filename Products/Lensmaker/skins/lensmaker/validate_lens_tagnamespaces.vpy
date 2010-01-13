## Script (Python) "validate_lens_tagnamespaces"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind state=state
##bind subpath=traverse_subpath
##parameters=
##
from Products.CMFPlone import PloneMessageFactory as _

errors = {}
request = context.REQUEST

obj_paths = request.get('obj_paths', [])
obj_ids = request.get('obj_ids', [])
count = 0
for objid in obj_ids:
    title   = request.get("%s-title" % objid, '').strip()
    prefix  = request.get("%s-prefix" % objid, '').strip()
    tags    = request.get("%s-tags" % objid, [])
    tags    = [t.strip() for t in tags if t.strip()]

    # Delegate to validators. We cannot call the validate method since there
    # is an issue with older Archetypes that makes validation difficult
    # without passing a request, so we validate each field individually.
    obj_path = obj_paths[count]
    tagnamespace = \
        context.portal_url.getPortalObject().restrictedTraverse(obj_path)
    new_errors = {}
    if not title:
       new_errors['title'] = _("Title is required") 
    if not prefix:
       new_errors['prefix'] = _("Prefix is required") 
    if not tags:
       new_errors['tags'] = _("Please enter tags") 
    tagnamespace.validate_field('title',    title,  new_errors)
    tagnamespace.validate_field('prefix',   prefix, new_errors)
    tagnamespace.validate_field('tags',     tags,   new_errors)
    if new_errors:
        # Prefix the error keys while adding to the global errors dictionary
        for k,v in new_errors.items():
            errors['%s-%s' % (objid, k)] = v
    count += 1
    
if errors:    
    return state.set(status='failure', errors=errors, portal_status_message='Please correct the indicated errors.')
else:
    return state
