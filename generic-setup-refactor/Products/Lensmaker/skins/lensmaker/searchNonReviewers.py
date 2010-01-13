## Script (Python) "searchReviewers"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=search, exclude
##title= Search for members who are not reviewers on the lens

members = context.portal_membership.searchForMembers(name=search)
return [m for m in members if m.getId not in exclude]
