## lens_notify_revised_script.py
##parameters=here,lensTitle,lensURL,included,lensCreator,object
##bind context=context

params={}
params['email'] = context.desecured.getMemberById(lensCreator).email
params['email_from_name']= context.email_from_name
params['email_from_address']= context.email_from_address
params['lensTitle']=lensTitle
params['lensURL']=lensURL
params['charset']=context.portal_properties.site_properties.default_charset
params['portal_title']=context.portal_url.getPortalObject().Title()
params['objtype_lower']=object.portal_type.lower()
params['objtype']=object.portal_type
params['version_or_toc'] = (object.portal_type == 'Module') and 'version' or 'table of contents'
params['not'] = not(included) and 'not' or ''
params['objTitle']=object.Title()
history = context.content.getHistory(object.objectId)
params['submitlog']=history[0].submitlog
params['newURL']=context.content.getRhaptosObject(object.objectId, history[0].version).url()
params['oldURL']=context.content.getRhaptosObject(object.objectId, history[1].version).url()

output="""
To: %(email)s
From: "%(email_from_name)s" <%(email_from_address)s>
Subject: Content selected by "%(lensTitle)s" has changed
Content-Type: text/plain; charset=%(charset)s

One of the %(objtype_lower)ss in your lens, "%(lensTitle)s", has been modified.

%(objtype)s: "%(objTitle)s"
Change notes: "%(submitlog)s"

You can view the new %(version_or_toc)s at:
    %(newURL)s
You can view the old %(version_or_toc)s at:
    %(oldURL)s

With your current settings, this new version will %(not)s be included in your lens. To change these settings,  please visit:
    %(lensURL)s/contents

You are receiving this email because you chose to enable notifications for your lens.  To change this preference, please visit:
    %(lensURL)s/edit

Thank you for participating in %(portal_title)s.

--
Sincerely,
The %(email_from_name)s Team
"""  % params
return output
