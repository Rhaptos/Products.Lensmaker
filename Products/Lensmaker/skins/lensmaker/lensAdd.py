## lensAdd.py : Add content to a specific lens.
##parameters=lensPath, contentId, version, namespaceTags=[], tags='', comment='', approved=False, approved_marker=False, implicit=True, returnTo=None, batched=False
## call with 'batched' if you're doing a lot of these (does commit) and will take care of updating the lens count

import transaction

lenstool = context.lens_tool

history = context.content.getHistory(contentId)

# previous version selection calculations
## params: lensVersionStart='this', lensVersionStop='latest',
## Valid values for lensVersionStart are 'this' and 'first'
## Valid values for lensVersionStart are 'this' and 'latest'
#versionStart = lensVersionStart == 'this' and version or history[-1].version
#versionStop = lensVersionStop == 'this' and version or None

# new version defaults
versionStart = version  # current
versionStop = 'latest'  # latest

cmpVersion = [int(x) for x in version.split('.')]

try:
    if lensPath == '__new__':
      # go to creation...
      from ZTUtils import make_query
      querystr = make_query(contentId=contentId, namespaceTags=namespaceTags, tags=tags, comment=comment,
                            versionStart=versionStart, versionStop=versionStop, implicit=implicit,
                            approved=approved,
                            returnTo=returnTo)
      context.REQUEST.RESPONSE.redirect('/create_lens?%s' % querystr)
      return "Need to create"
    else:
      lens = context.restrictedTraverse(lensPath)
      if context.portal_factory.isTemporary(lens):
          # make concrete...
          newid = getattr(lens, 'suggestId', lambda: None)() or lens.getId()
          lens = context.portal_factory.doCreate(lens, newid)

    tags = tags.split()
    entry = getattr(lens, contentId, None)
    made = False
    if entry is None:
        lens.invokeFactory(id=contentId, type_name="SelectedContent")
        entry = lens[contentId]
        made = True

    # unchosen version behavior:
    #  - if end is latest, do nothing
    #  - if end <= current, do nothing
    #  - if end > current, set version to current
    # we don't pay attention to beginning ranges. versionStart is left alone (except in creation, of course)
    if not made:  # we will accept the values above for new content
        origStart = entry.getRawVersionStart()  # string version, like '1.1'
        versionStart = origStart

        origStop = entry.getRawVersionStop()
        if origStop:   # latest is (), so only true for explicit stop versions
            cmpOrigStop = entry.getVersionStop()     # list version, like [1,1]
            if cmpVersion > cmpOrigStop:
                versionStop = version      # current is newer, so set stop to current
            else:
                versionStop = origStop     # otherwise, leave it alone

    # Only set approved if it is present on the form. This is determined
    # by checking approved_marker.
    attrs = dict(contentId=contentId, versionStart=versionStart, versionStop=versionStop,
                 namespaceTags=namespaceTags, tags=tags, comment=comment, implicit=implicit)
    if approved_marker:
        attrs['approved'] = approved
    entry.update(**attrs)

    if batched:
        pass
        #transaction.commit()  # may not pass security, haven't checked
    else:
        lens.setModificationDate()
        lens.reindexObject(idxs=['count', 'modified'])

except KeyError:
    return "Error: no such lens"

if returnTo:
    context.REQUEST.RESPONSE.redirect(returnTo)
return "Sucessful."
