## Script (Python) "lens_add_open_finish"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=lens_paths=[]
##title=Create module-lens associations
##

request = context.REQUEST

for pth in lens_paths:
    # Delegate to existing adder
    context.lensAdd(
            lensPath=pth, 
            contentId=context.objectId, 
            version=context.version, 
            namespaceTags=request.get(pth+'-namespaceTags', []), 
            tags=request.get(pth+'-tags', ''),
            comment=request.get(pth+'-comment', ''),
    )            

psm = context.translate("module_added_to_open_lenses", domain="rhaptos", default="Module added to open lens.")
return state.set(status='success', portal_status_message=psm, context=context)
