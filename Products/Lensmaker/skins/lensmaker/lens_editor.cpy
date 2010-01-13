## Script (Python) "lens_editor"
##parameters=
##
## Like content_edit, but take care of special cases for lenses, like creation of initial content and workflow state

from Products.Lensmaker.LensPermissions import BadRequest, CopyError

REQUEST = context.REQUEST

newid = REQUEST.get('id', None) or getattr(context, 'suggestId', lambda: None)()
if not newid:
    dname = REQUEST.get('displayName', '')
    newid = context.lensNextName(context.plone_utils.normalizeString(dname))

try:
    new_context = context.portal_factory.doCreate(context, newid)
except AttributeError:
    # Fallback for AT + plain CMF where we don't have a portal_factory
    new_context = context
except (BadRequest, CopyError):
    state.setError('id', "This id is unusable, reserved, or already in use.")
    return state.set(status='failure',
                    portal_status_message="Please correct the indicated errors (check Advanced Settings).")

try:
    new_context.processForm()
except ValueError:
    state.setError('logo', "Unprocessable image file was provided.")  # TODO: replace with proper image validator
    new_context.reindexObject()
    return state.set(status='failure',
                     context=new_context,
                     portal_status_message="Please correct the indicated errors.")
except (BadRequest, CopyError):
    state.setError('id', "This id is unusable, reserved, or already in use.")
    new_context.reindexObject()
    return state.set(status='failure',
                     context=new_context,
                     portal_status_message="Please correct the indicated errors (check Advanced Settings).")

## special actions
# initial content
contentId = REQUEST.get('contentId', None)
if contentId:
    tags = REQUEST.get('tags', '')
    if tags:
        tags = tags.split()
    comment = REQUEST.get('comment', None)
    versionStart = REQUEST.get('versionStart', None)
    versionStop = REQUEST.get('versionStop', None)
    implicit = REQUEST.get('implicit', None)
    returnTo = REQUEST.get('returnTo', None)

    new_context.invokeFactory(id=contentId, type_name="SelectedContent")
    entry = new_context[contentId]
    entry.setComment(comment, mimetype="text/html")  # rely on reindex in next step
    entry.update(contentId=contentId, versionStart=versionStart, versionStop=versionStop,
                 tags=tags, implicit=implicit)
    entry.reindexObject(idxs=['Title'])

# control workflow state
reqstate = REQUEST.get('wfstate', None)
wfstate_modifier = REQUEST.get('wfstate_modifier', None)
newstate = ''
if reqstate == 'published':
    if wfstate_modifier:
        newstate = 'published_open'
    else:
        newstate = 'published'
elif reqstate == 'private':
    if wfstate_modifier:
        newstate = 'private_open'
    else:
        newstate = 'private'

wftool = context.portal_workflow
wfstate = wftool.getInfoFor(new_context, 'review_state')
# Only perform transition if state has actually changed.
if newstate and newstate != wfstate:     # newstate false for Favorites/no state change lenses
    transition = {
            'private':'hide', 
            'published':'publish', 
            'private_open':'expose_private', 
            'published_open':'expose_published'}.get(newstate)
    if transition: wftool.doActionFor(new_context, transition)
    for obj in context.contentValues():
        obj.reindexObject(idxs=['allowedRolesAndUsers'])

portal_status_message = context.translate(
    msgid='message_content_changes_saved',
    domain='archetypes',
    default='Content changes saved.')

portal_status_message = REQUEST.get('portal_status_message', portal_status_message)

time = context.lens_tool.catalogQueueInfo()
time = time and time[1] or 0
if time > 0.1:
    psm = " The system is processing lens changes. Changed properties should be viewable on content in %0.1f minutes." % time
    portal_status_message += psm

return state.set(status='success',
                 context=new_context,
                 portal_status_message=portal_status_message)
