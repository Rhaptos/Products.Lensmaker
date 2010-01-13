## Script (Python) "lens_prefill"
##parameters=
##
## Inject values into the request based on selected type, title, and creator (if available)

REQUEST = context.REQUEST
member = context.portal_membership.getAuthenticatedMember()
shortname = member.getProperty('shortname', None) or member.getProperty('fullname')
fullname = member.getProperty('fullname', None)

title = REQUEST.get('title', '')
category = REQUEST.get('category', None)

lensid = None
displayName = None

if category == 'Endorsement':
  lensid = context.lensNextName('endorsements')
  displayName = shortname
elif category == 'Affiliation':
  lensid = context.lensNextName('affiliation')
  displayName = shortname
else:
  REQUEST.set('category', 'List')
  lensid = context.plone_utils.normalizeString(title)      # normalized title
  displayName = title[:20]

title = title or fullname and "%s's Lens" % fullname

url = member.getProperty('homepage')
urlText = "Visit Web page for %s" % shortname

avail_languages=context.portal_languages.listAvailableLanguages()
boundLanguages=context.portal_languages.getLanguageBindings()
prefLang=boundLanguages[0]
prefill_lang = prefLang and prefLang or 'en'
REQUEST.set('language', prefill_lang)

REQUEST.set('id', lensid)
REQUEST.set('title', title)
REQUEST.set('displayName', displayName)
REQUEST.set('url', url)
REQUEST.set('urlText', urlText)
REQUEST.set('disable_border', 1)

return state.set(status='success')
