## Script (Python) "lens_view_view"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=tag=None
##title=
##
# organize results data for lens listing view
# hopefully to turn into a Zope 3 view.

request = context.REQUEST
content = context.portal_url.getPortalObject().content
searchhash = context.expanded_searchhash(request.form)

if context.isOpen():
    sorton_default = 'getApproved'
else:
    sorton_default = 'portal_type'

sorton = request.get('sorton', sorton_default)
recent = request.get('recent', False)
request.set('sorton', sorton)
request.set('recent', recent)

cached_results = content.cache.resultsCacheLookup(searchhash,sorton,recent)

subpath =  traverse_subpath
tag = tag or (len(subpath) and subpath) or request.get('tag',[])
creator = context.getCreatorMember()
creatorName = creator.getProperty('fullname')

companion = context.listOfEntries(tag=tag)
raw_results = []
if companion:
    raw_results = context.contentResults(entries=companion)
results = content.sortSearchResults(list(raw_results),sorton,recent)

#if results is None: # TODO: doesn't actually use cache
content.cache.resultsCacheInject(searchhash, (results, {}, sorton, recent))

retvals = {}
retvals['searchhash'] = searchhash
retvals['results'] = results
retvals['tag'] = tag
retvals['companion'] = companion
retvals['creator'] = creator
retvals['creatorName'] = creatorName
return retvals
