## lens_notify_derived.py
##parameters=here,lensTitle,lensURL,included,lensCreator,object,modified_object
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
params['obj_url']=object.url
params['copy_objtype']=modified_object.portal_type.lower()
params['copy_objTitle']=modified_object.Title()
params['copy_obj_url']=modified_object.url()

output="""
To: %(email)s
From: "%(email_from_name)s" <%(email_from_address)s>
Subject: Object derived in your %(portal_title)s Lens
Content-Type: text/plain; charset=%(charset)s

One of the %(objtype_lower)ss in your lens, "%(lensTitle)s", has had a new derived copy published. You might be interested in adding the new %(objtype_lower)s to your lens.

You can view the new %(objtype_lower)s at:
    %(copy_obj_url)s
You can view the original %(objtype_lower)s at:
    %(obj_url)s

You are receiving this email because you chose to enable notifications for your lens.  To change this preference, please visit:
    %(lensURL)s/edit

Thank you for participating in %(portal_title)s.

--
Sincerely,
The %(email_from_name)s Team
"""  % params
return output
