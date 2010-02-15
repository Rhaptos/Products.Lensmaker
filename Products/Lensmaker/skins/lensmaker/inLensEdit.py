## tell, based on URL, if we're "editing" a lens or lens organizer (or, really, anything under 'lenses')
## used to switch back and forth between mydashboard and lens tabs depending on editing or not
## called from actions, so we can check object and URL

request = context.REQUEST
url = request.URL
view = url.split('/')[-1]

# I chose a whitelist, because forums add a whole lot of unknown to a blacklist,
# and it seems better to fail to 'lenses' than to fail to 'mydashboard'
editmode = view in ('edit', 'contents',                                    # aliases
                    'lens_content_view', 'lens_edit', 'lens_preview',      # std lens tab templates
                    'lens_delete_confirm', 'lens_content_edit',            # other std lens edit templates
                    'folder_delete_confirm',
                    'create_lens', 'lens_chooser',                         # lens create templates
                    'lens_tagnamespaces_view', 'lens_reviewers',           # open lens tab templates
                    'lens_tagnamespaces_edit',                             # other open lens edit templates
                    'lensorganizer_view', 'base_edit',                     # lens organizer tabs
                    'delete_lens_organizer_confirmation')                  # lens org. templates
editmode = editmode or context.portal_type in ('TagNamespace')

return editmode