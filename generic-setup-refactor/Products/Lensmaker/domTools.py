class domException(Exception):
    def __init(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

def getText(nodelist):
     rc = ""
     for node in nodelist:
         if node.nodeType == node.TEXT_NODE:
             rc = rc + node.data
     return rc

def domLensHasId(dom):
     """sorts through the dom and returns the lens name"""
     return len(dom.getElementsByTagName("id")) > 0 and domLensId(dom) != ''

def domLensId(dom):
     """sorts through the dom and returns the lens name"""
     return getText(dom.getElementsByTagName("id")[0].childNodes)

def domLensHasTitle(dom):
     """sorts through the dom and returns the lens title"""
     return len(dom.getElementsByTagName("title")) > 0 and domLensTitle(dom) != ''

def domLensTitle(dom):
     """sorts through the dom and returns the lens title"""
     return getText(dom.getElementsByTagName("title")[0].childNodes)

def domLensHasAuthor(dom):
     """sorts through the dom and returns the lens author"""
     return len(dom.getElementsByTagName("author")) > 0 and domLensAuthor(dom) != ''

def domLensAuthor(dom):
     """sorts through the dom and returns the lens author"""
     return getText(dom.getElementsByTagName("author")[0].childNodes)

def domLensHasCategory(dom):
     """sorts through the dom and returns the lens category"""
     return len(dom.getElementsByTagName("category")) > 0 and domLensCategory(dom) != ''

def domLensCategory(dom):
     """sorts through the dom and returns the lens category"""
     return dom.getElementsByTagName("category")[0].getAttribute("term")

def domLensHasRights(dom):
     """sorts through the dom and returns the lens rights"""
     return len(dom.getElementsByTagName("rights")) > 0 and domLensRights(dom) != ''

def domLensRights(dom):
     """sorts through the dom and returns the lens rghts"""
     return getText(dom.getElementsByTagName("rights")[0].childNodes)

def domLensHasName(dom):
     """sorts through the dom and returns the lens suntitle/discription"""
     return len(dom.getElementsByTagName("name")) > 0 and domLensName(dom) != ''

def domLensName(dom):
     """sorts through the dom and returns the lens suntitle/discription"""
     return getText(dom.getElementsByTagName("name")[0].childNodes)

def domLensHasSubtitle(dom):
     """sorts through the dom and returns the lens title"""
     return len(dom.getElementsByTagName("subtitle")) > 0 and domLensSubtitle(dom) != ''

def domLensSubtitle(dom):
     """sorts through the dom and returns the lens title"""
     return getText(dom.getElementsByTagName("subtitle")[0].childNodes)

def domLensHasUrl(dom):
     """sorts through the dom and returns the lens url text"""
     return len(dom.getElementsByTagName("rhaptos:ownerUrl")) > 0 and domLensUrl(dom) != ''

def domLensUrl(dom):
     """sorts through the dom and returns the lens url text"""
     return getText(dom.getElementsByTagName("rhaptos:ownerUrl")[0].childNodes)

def domLensHasUrlText(dom):
     """sorts through the dom and returns the lens url text"""
     return len(dom.getElementsByTagName("rhaptos:ownerUrlText")) > 0 and domLensUrlText(dom) != ''

def domLensUrlText(dom):
     """sorts through the dom and returns the lens url text"""
     return getText(dom.getElementsByTagName("rhaptos:ownerUrlText")[0].childNodes)

def domLensHasPublic(dom):
     """sorts through the dom and returns the lens review status"""
     return len(dom.getElementsByTagName("rhaptos:public")) > 0 and domLensPublic(dom) != ''

def domLensPublic(dom):
     """sorts through the dom and returns the lens review status"""
     return getText(dom.getElementsByTagName("rhaptos:public")[0].childNodes)

def domLensHasRecieveEmailOnUpdate(dom):
     """sorts through the dom and returns the lens review status"""
     return len(dom.getElementsByTagName("rhaptos:recieveEmailOnUpdate")) > 0 and domLensRecieveEmailOnUpdate(dom) != ''

def domLensRecieveEmailOnUpdate(dom):
     """sorts through the dom and returns the lens review status"""
     return getText(dom.getElementsByTagName("rhaptos:recieveEmailOnUpdate")[0].childNodes)

def domLensHasHasTagCloud(dom):
     """sorts through the dom and returns the lens tag cloud"""
     return len(dom.getElementsByTagName("rhaptos:hasTagCloud")) > 0 and domLensHasTagCloud(dom) != ''

def domLensHasTagCloud(dom):
     """sorts through the dom and returns the lens tag cloud"""
     return getText(dom.getElementsByTagName("rhaptos:hasTagCloud")[0].childNodes)

def domLensHasLanguage(dom):
     """sorts through the dom and returns the lens tag cloud"""
     return len(dom.getElementsByTagName("rhaptos:language")) > 0 and domLensLanguage(dom) != ''

def domLensLanguage(dom):
     """sorts through the dom and returns the lens tag cloud"""
     return getText(dom.getElementsByTagName("rhaptos:language")[0].childNodes)

def domEntryHasLink(entry):
     """sorts through the entry and returns the entry link"""
     return len(entry.getElementsByTagName("link"))  > 0 and domEntryLink(dom) != ''

def domEntryLink(entry):
     """sorts through the entry and returns the entry link"""
     return entry.getElementsByTagName("link")[0]

def domEntryHasTitle(entry):
     """sorts through the entry and returns the entry id"""
     return len(entry.getElementsByTagName("title"))  > 0 and domEntryTitle(dom) != ''

def domEntryTitle(entry):
     """sorts through the entry and returns the entry id"""
     return entry.getElementsByTagName("title")[0]

def domEntryHasContent(entry):
     """sorts through the entry and returns the entry id"""
     return len(entry.getElementsByTagName("content"))  > 0 and domEntryContent(dom) != ''

def domEntryContent(entry):
     """sorts through the entry and returns the entry id"""
     return entry.getElementsByTagName("content")[0]

def domEntryHasComment(entry):
     """sorts through the entry and returns the entry id"""
     retval = False
     if domEntryHasContent(entry):
         content = domEntryContent(entry)
         pEntrys = content.getElementsByTagName("p")
         for pEntry in pEntrys:
             if pEntry.getAttribute("class") == "comment":
                 retval = True
                 break
     return retval

def domEntryComment(entry):
     """sorts through the entry and returns the entry comment"""
     content = domEntryContent(entry)
     return getText(content.getElementsByTagName("p")[0].childNodes)

def domEntryId(entry):
     """sorts through the entry and returns the entry id"""
     return getText(entry.getElementsByTagName("id")[0].childNodes)

def domEntryHasVersionStart(entry):
     """sorts through the entry and returns the entry version start"""
     return len(entry.getElementsByTagName("rhaptos:versionStart")) > 0 and domEntryVersionStart(dom) != ''

def domEntryVersionStart(entry):
     """sorts through the entry and returns the entry version start"""
     return getText(entry.getElementsByTagName("rhaptos:versionStart")[0].childNodes)

def domEntryHasVersionStop(entry):
     """sorts through the entry and returns the entry version stp"""
     return len(entry.getElementsByTagName("rhaptos:versionStop")) > 0  and domEntryVersionStop(dom) != ''

def domEntryVersionStop(entry):
     """sorts through the entry and returns the entry version stp"""
     return getText(entry.getElementsByTagName("rhaptos:versionStop")[0].childNodes)

def domEntryHasImplicit(entry):
     """sorts through the entry and returns the entry implicit"""
     return len(entry.getElementsByTagName("rhaptos:implicit")) > 0 and domEntryImplicit(dom) != ''

def domEntryImplicit(entry):
     """sorts through the entry and returns the entry implicit"""
     return getText(entry.getElementsByTagName("rhaptos:implicit")[0].childNodes)

def domEntryHasTags(entry):
     """sorts through the entry and returns the entry tags"""
     retval = False
     if domEntryHasContent(entry):
         content = domEntryContent(entry)
         ulEntrys = content.getElementsByTagName("ul")
         for ulEntry in ulEntrys:
             if ulEntry.getAttribute("class") == "tags":
                 retval = True
                 break
     return retval

def domEntryTags(entry):
    """sorts through the entry and returns the entry tags"""
    tags = []
    if domEntryHasContent(entry):
        content = domEntryContent(entry)
        ulEntrys = content.getElementsByTagName("ul")
        for ulEntry in ulEntrys:
            if ulEntry.getAttribute("class") == "tags":
                liEntrys = ulEntry.getElementsByTagName("li")
                for liEntry in liEntrys:
                    tags.append(getText(liEntry.childNodes))
    return tags

def editEntryFromDom(domEntry, entry, validate):
    """ edit selected content information in a lens """
    hasEntryChanged = False
    contentId = domEntryId(domEntry)

    ## if validate:
        ## if domEntryHasTitle(domEntry) and (entry.Title() + ' (lens entry)') != domEntryTitle(domEntry):
	    ## return 'Title on entry ' + contentId + ' may not be changed "' + entry.Title() + ' (lens entry)" != "' + domEntryTitle(domEntry) + '"'

    # comment
    comment = ''
    try:
        oldComment = entry.getComment()
        if domEntryHasComment(domEntry):
            comment = domEntryComment(domEntry)
            if oldComment() != comment:
                hasEntryChanged = True
            else:
                comment = oldComment()
    except:
        hasEntryChanged = True

    # versionStart
    versionStart = '1.1'
    try:
        oldVersionStart = entry.getVersionStart()
        if domEntryHasVersionStart(domEntry):
            versionStart = domEntryVersionStart(domEntry)
            if oldVersionStart() != versionStart:
                hasEntryChanged = True
            else:
                versionStart = oldVersionStart()
    except:
        hasEntryChanged = True

    # versionStop
    versionStop = 'latest'
    try:
        oldVersionStop = entry.getVersionStop()
        if domEntryHasVersionStop(domEntry):
            versionStop = domEntryVersionStop(domEntry)
            if oldVersionStop() != versionStop:
                hasEntryChanged = True
            else:
                versionStop = oldVersionStop()
    except:
        hasEntryChanged = True

    # implicit
    implicit = True
    try:
        oldImplicit = entry.getImplicit()
        if domEntryHasImplicit(domEntry):
            implicit = domEntryImplicit(domEntry)
            if oldImplicit() != implicit:
                hasEntryChanged = True
            else:
                implicit = oldImplicit()
    except:
        hasEntryChanged = True

    # tags
    areTagsDifferent = False
    originalTags = []
    tags = []
    try:
        originalTags = entry.getTags()
        if domEntryHasTags(domEntry):
            tags = domEntryTags(domEntry)
            # see if the new tags match the original tags
            if len(tags) == len(originalTags):
                for newTag in tags:
                    found = False
                    for oldTag in originalTags:
                        if oldTag == newTag:
                            found = True
                            break
                    if not found:
                        areTagsDifferent = True
			break
            else:
               areTagsDifferent = True
    except:
        areTagsDifferent = True

    if areTagsDifferent:
        hasEntryChanged = True
    else:
        tags = originalTags

    if hasEntryChanged:
        entry.setModificationDate()
        entry.setVersionStart(versionStart)
	entry.setUrl(entry.absolute_url())
        entry.setContentId(contentId)
        entry.setVersionStop(versionStop)
        entry.setTags(tags)
        entry.setComment(comment)
        entry.setImplicit(implicit)
        entry.reindexObject(idxs=['Title'])

    return None

def editLensFromDom(lens, dom, validate):
    """ edit lens from xml"""
    # now set the fields frm the dom
    hasLensChanged = False

    if validate:
        # validation commented out because getCreatorMember sometime returns empty string 
	# even when lens has an author
        # if domLensHasAuthor(dom) and lens.getCreatorMember() != domLensAuthor(dom):
	    # return 'Author may not be changed ' + author

        if domLensHasCategory(dom) and lens.getCategory() != domLensCategory(dom):
	    return 'Category may not be changed ' + lens.getCategory() + ' != ' +  domLensCategory(dom)
        if domLensHasRights(dom) and lens.Rights() != domLensRights(dom):
	    return 'Rights may not be changed "' + lens.Rights() + '" != "' + domLensRights(dom) + '"'

    # id 
    if domLensHasId(dom) and lens.getId() != domLensId(dom):
        lens.setId(domLensId(dom).encode('utf-8'))
        hasLensChanged = True

    # title 
    if domLensHasTitle(dom) and lens.Title() != domLensTitle(dom):
        lens.setTitle(domLensTitle(dom))
        hasLensChanged = True

    # name 
    if domLensHasName(dom) and lens.getDisplayName() != domLensName(dom):
        lens.setDisplayName(domLensName(dom))
        hasLensChanged = True

    # subtitle 
    if domLensHasSubtitle(dom) and lens.Description() != domLensSubtitle(dom):
        lens.setDescription(domLensSubtitle(dom))
        hasLensChanged = True

    # ownerUrl
    if domLensHasUrl(dom) and lens.getUrl() != domLensUrl(dom):
        lens.setUrl(domLensUrl(dom))
        hasLensChanged = True

    # ownerUrlText
    if domLensHasUrlText(dom) and lens.getUrlText() != domLensUrlText(dom):
        lens.setUrlText(domLensUrlText(dom))
        hasLensChanged = True

    # public 
    ## newPublic = domLensPublic(dom)

    # recieveEmailOnUpdate
    if domLensHasRecieveEmailOnUpdate(dom) and lens.notifyOfChanges != domLensRecieveEmailOnUpdate(dom):
        lens.setNotifyOfChanges(domLensRecieveEmailOnUpdate(dom) == 'true' and True or False) 
        hasLensChanged = True

    # cloudTag
    if domLensHasHasTagCloud(dom):
        if lens.getNoTagCloud() and 'false' or 'true' != domLensHasTagCloud(dom):
            lens.setNoTagCloud( domLensHasTagCloud(dom) == 'false')
            hasLensChanged = True

    # language 
    if domLensHasLanguage(dom) and lens.getLanguage() != domLensLanguage(dom):
        lens.setLanguage(domLensLanguage(dom))
        hasLensChanged = True

    # each entry
    domEntries = dom.getElementsByTagName("entry")
    for domEntry in domEntries:
        entryId = domEntryId(domEntry)
        entry = findEntryById(lens, entryId)
        if entry is None: # add
            lens.invokeFactory(id=entryId, type_name="SelectedContent")
            hasLensChanged = True
            entry = findEntryById(lens, entryId)
        entryMessage = editEntryFromDom(domEntry, entry, validate)
	if not entryMessage is None:
            return entryMessage

    # if update
    if hasLensChanged:
        lens.setModificationDate()
        entry.reindexObject(idxs=['Title'])
    return None

def findEntryById(lens, entryId):
    entry = None
    for loopEntry in lens.contentValues():
        if loopEntry.getId() == entryId:
            entry = loopEntry
            break;
    return entry
