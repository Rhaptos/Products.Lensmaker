## lensDel.py : Remove content from a specific lens.
##parameters=lensPath, contentId, returnTo=None

request = context.REQUEST
msg = "Failed."

if lensPath.startswith('/'):
    lensPath = lensPath[1:]
lens = context.restrictedTraverse(lensPath)
if lens:
    lens.manage_delObjects([contentId,])
    msg = "Deleted: %s." % contentId
else:
    msg = "No lens at: %s" % lensPath

if returnTo:
    request.RESPONSE.redirect(returnTo)
else:
    request.RESPONSE.redirect(request.URL1)
return msg
