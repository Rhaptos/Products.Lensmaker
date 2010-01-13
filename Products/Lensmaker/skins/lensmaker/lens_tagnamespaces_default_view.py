# We do not want the normal plone UI machinery at work so we
# redirect to a fixed view.
context.REQUEST.RESPONSE.redirect(context.aq_parent.absolute_url() + '/lens_tagnamespaces_view')
