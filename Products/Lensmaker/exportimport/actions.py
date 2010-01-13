
from Products.CMFCore.utils import getToolByName

def reorderActions(context):

    if context.readDataFile('lensmaker.xml') is None:
        return
    portal = context.getSite()
    pa_tool = getToolByName(portal, 'portal_actions')
    # position lens tab actions
    # not very elegant, but  GS profile doesn't support action ordering
    log(" - moving actions", out)
    # view
    idx = 0
    idx_content = 0
    idx_lensestab_view = 0
    for a in pa_tool._actions:
        if a.id == 'content':
            idx_content = idx
        elif a.id == 'lensestab-viewing':
            idx_lensestab_view = idx
        idx += 1

    if idx_lensestab_view > idx_content + 1:
        log("Reposition lenses tab action for viewing", out)
        new_actions = pa_tool._cloneActions()
        action = new_actions[idx_lensestab_view]
        del new_actions[idx_lensestab_view]
        new_actions.insert(idx_content+1, action)
        pa_tool._actions = tuple(new_actions)

    # edit
    idx = 0
    idx_content = 0
    idx_lensestab_edit = 0
    for a in pa_tool._actions:
        if a.id == 'content':
            idx_content = idx
        elif a.id == 'lensestab-editing':
            idx_lensestab_edit = idx
        idx += 1

    if idx_lensestab_edit > idx_content + 1:
        log("Reposition lenses tab action for editing", out)
        new_actions = pa_tool._cloneActions()
        action = new_actions[idx_lensestab_edit]
        del new_actions[idx_lensestab_edit]
        new_actions.insert(idx_content+1, action)
        pa_tool._actions = tuple(new_actions)

    # move contents action to top
    log(" - type actions", out)
    types_tool = getToolByName(portal, 'portal_types')
    actions = types_tool.ContentSelectionLens._actions
    contents = None
    for a in actions:
        if a.id == 'contents':
            contents = a
    actions = [contents] + [act for act in actions if act != contents]
    types_tool.ContentSelectionLens._actions = actions

    actions = types_tool.FavoritesLens._actions
    contents = None
    for a in actions:
        if a.id == 'contents':
            contents = a
    actions = [contents] + [act for act in actions if act != contents]
    types_tool.FavoritesLens._actions = actions

