## Script (Python) "lensNextObject"
##parameters=category
##
## Return the name of the next object of type 'category'
## If no object named 'category', use 'category'
## If object named such, return 'category1'. If 'category1' exists, return 'category2', etc

memberid = context.portal_membership.getAuthenticatedMember().getId()
lensfolder = context.lenses[memberid]
objids = lensfolder.contentIds()

if not category in objids:
    return category

catlen = len(category)
ints = (0,)

for x in objids:  # ... I'd do this as a list comprehension, but I can't do the try/except in one.
    if x.startswith(category):
        try:
            i = int(x[catlen:])
            ints = ints + (i,)
        except ValueError:
            pass

next = max(ints)+1
return category + str(next)