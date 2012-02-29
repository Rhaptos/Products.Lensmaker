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
    newBrandingCookie = ''
    cookies = [c.split('#')[0] for c in brandingCookie.split('|')]
    if location in cookies: cookies.remove(location)
    cookies.append(location)
    newBrandingCookie = '|'.join(cookies)
else:
    newBrandingCookie = location

# add a year ... safe for leapday
# The RFC-822/HTTP date-time format is required
then = (DateTime()+365).rfc822()
expires = str(then)
request.RESPONSE.setCookie('lenses', newBrandingCookie, path="/", expires=expires)
