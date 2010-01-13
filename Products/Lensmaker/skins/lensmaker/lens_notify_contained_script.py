## lens_notify_contained_template.py
##parameters=here,lensTitle,lensURL,included,lensCreator,object,contained_object
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
params['objTitle']=object.Title
params['cont_objtype']=contained_object.portal_type.lower()
params['cont_objTitle']=contained_object.Title()
history = context.content.getHistory(contained_object.objectId)
params['submitlog']=history[0].submitlog
params['newURL']=context.content.getRhaptosObject(contained_object.objectId, history[0].version).url()
params['oldURL']=context.content.getRhaptosObject(contained_object.objectId, history[1].version).url()

output="""
To: %(email)s
From: "%(email_from_name)s" <%(email_from_address)s>
Subject: Content selected by "%(lensTitle)s" has changed
Content-Type: text/plain; charset=%(charset)s

One of the %(objtype_lower)ss in your lens, "%(lensTitle)s", has changed, because an included %(cont_objtype)s has been modified.

%(objtype)s: "%(objTitle)s"
Changed %(cont_objtype)s: "%(cont_objTitle)s"
Change notes: "%(submitlog)s"

You can view the new version of the changed module at:
    %(newURL)s
You can view the old version at:
    %(oldURL)s

This new version will be included in your lens. To remove the selected collection from your lens,  please visit:
    %(lensURL)s/contents

You are receiving this email because you chose to enable notifications for your lens.  To change this preference, please visit:
    %(lensURL)s/edit

Thank you for participating in %(portal_title)s.

--
Sincerely,
The %(email_from_name)s Team
"""  % params
return output
