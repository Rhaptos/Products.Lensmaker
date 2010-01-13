## Script (Python) "tags_browse_view"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=
##
# organize results data for tags browse view
# hopefully to turn into a Zope 3 view.

request = context.REQUEST
content = context.portal_url.getPortalObject().content
searchhash = context.expanded_searchhash(request.form)
sorton = request.get('sorton', 'title')
recent = request.get('recent', False)
request.set('sorton',sorton)
request.set('recent',recent)

cached_results = content.cache.resultsCacheLookup(searchhash,sorton,recent)

tag = request.get('tag')
prefix = request.get('prefix', '')

if prefix:
    prefixed_tag = '%s::%s' % (prefix, tag)
else:
    prefixed_tag = tag

if cached_results is None:
    entries = tag and context.lens_tool.getContentForTag(prefixed_tag) or None
    raw_results = entries and context.lens_tool.entriesToContent(entries) or []
    results = sorton != 'title' and content.sortSearchResults(list(raw_results),sorton,recent) or raw_results
    content.cache.resultsCacheInject(searchhash, (results, {}, sorton, recent))
else:
    results = cached_results[0]

retvals = {}
retvals['searchhash'] = searchhash
retvals['results'] = results
retvals['tag'] = tag
retvals['prefix'] = prefix
return retvals
