
def addRoles(context):
    if context.readDataFile('lensmaker.txt') is None:
        return
    portal = context.getSite()
    portal.acl_users.addRole('Endorser')
    portal.acl_users.addRole('Branding')
    portal.acl_users.addRole('PermaBranding')

