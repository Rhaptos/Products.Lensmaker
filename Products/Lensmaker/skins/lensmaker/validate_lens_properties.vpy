## Script (Python) "validate_reviewers"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=validates lens reviewers
context.plone_log('validate lens properties 0.')

REQUEST=context.REQUEST
errors = {}

banner = hasattr(REQUEST,'banner') and  REQUEST.banner or '0'
bannerColor = hasattr(REQUEST,'bannerColor') and REQUEST.bannerColor or ''

gotBranding = ( banner == '1' )
if gotBranding:
    if bannerColor is not None and len(bannerColor) == 0:
        # associate an error message with the invalid field
        bannermsg = context.translate("branding_color_must_be_selected", domain="rhaptos",default="A branding banner color must be selected.")
        state.setError('bannerColor', bannermsg)

if state.getErrors():
    psm = context.translate("message_please_correct_errors", domain="rhaptos", default="Please correct the indicated errors.")
    return state.set(status='failure', portal_status_message=psm)
else:
    return state
