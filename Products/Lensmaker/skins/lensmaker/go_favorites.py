## Python Script "go_favorites"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=Redirect to Favorites lens; create if not already created (through portal_factory)
##

from AccessControl import Unauthorized

o = context.favorites_get()
if o is None:
    raise Unauthorized
url = o.absolute_url()

if traverse_subpath:
    method = "/".join(traverse_subpath)
else:
    method = "contents"

return context.REQUEST.response.redirect("%s/%s" % (url, method))