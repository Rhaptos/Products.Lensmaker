## Script (Python) "findBrandingLenses"
##bind context=context
##parameters=cats=None, brandingCookie=None
##title=Find a branding lens

# cats has been returned from LensTool.getListsIncluding(), ie a
# list of lenses that included the content object of interest

if cats is None or cats == {}:
    return None

# brandingCookie is a string of a browser branding cookie

if brandingCookie is None or len(brandingCookie) == 0:
    return None

brandedLenses = {}
for cattype in cats:
    print cattype
    lenses = cats[cattype]
    for lens in lenses:
        print lens
        lensinfo = lenses[lens][0]
        lenscontents = lenses[lens][1]
        gotBranding = ( lensinfo['banner'] == 'true' )
        if gotBranding:
            brandedLenses[lens] =  lensinfo

if brandedLenses != {}:
    #context.plone_log("brandingCookie is %s" % brandingCookie)
    #context.plone_log("brandedLenses is %s" % str(brandedLenses))
    for entry in brandingCookie.split('|')[::-1]:  #reversed(brandingCookie.split('|')):
        lensId = entry.split('#')[0]
        #context.plone_log("looking at lens id: %s" % lensId)
        if lensId in brandedLenses:
            #context.plone_log("lens is branded")
            betterLensId = ( lensId.startswith('/') and lensId[1:] or lensId )
            betterLensInfo = brandedLenses[lensId]
            lens = context.restrictedTraverse(betterLensId)
            bannerForegroundColor = lens.bannerForegroundColor()
            betterLensInfo['bannerForegroundColor'] = bannerForegroundColor
            rv = { 'lensId':betterLensId,  'lensInfo':betterLensInfo, }
            #context.plone_log("returning %s" % str(rv))
            return rv

return None
