## Script (Python) "setBrandingCookie"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=
##

# called from a lens context

from DateTime import DateTime
# QueueTool uses:
#from datetime import datetime, timedelta

request = context.REQUEST

lens = context
lensDict = lens.listDict()
location = lensDict['location']

gotCookie = ( 'lenses' in request )

if gotCookie:
    brandingCookie = request['lenses']
    bFound = False
    newBrandingCookie = ''
    for entry in brandingCookie.split('|'):
        entry_location = entry.split('#')[0] # backwards compat wonk
        if entry_location == location:
            bFound = True
        else:
            newBrandingCookie = len(newBrandingCookie) == 0 and entry_location or \
                                ( newBrandingCookie + '|' + entry_location )
    newBrandingCookie = len(newBrandingCookie) == 0 and location or \
                        ( newBrandingCookie + '|' + location )
else:
    brandingCookie = ''
    newBrandingCookie = location

#context.plone_log("brandingCookie is '%s'." % str(brandingCookie))
#context.plone_log("newBrandingCookie is '%s'." % str(newBrandingCookie))
now = DateTime()
# add a year ... perhaps the hard way
expires = '%d/%d/%d %d:%d:%f %s' % (now.year()+1,now.month(),now.day(),now.hour(),now.minute(),now.second(),now.timezone())
# The RFC-822/HTTP date-time format is required
then = DateTime(expires).rfc822()
expires = str(then)
request.RESPONSE.setCookie('lenses', newBrandingCookie, path="/", expires=expires)
