Lensmaker
Provides "lenses": provides collections of content, with possible tags and comments.
Eventually, one will be able to see the whole site using these lists as filters, singly and in combination.
Thus: "lens"

author: J Cameron Cooper (jccooper@rice.edu)
June 2007
Copyright (c) 2007, Rice University. All rights reserved.

This Zope Product is part of the Rhaptos system (http://rhaptos.org), created to run Connexions (http://cnx.org.)

Depends on RhaptosCollection at the moment, but should be separable with some work on separating some specific shared fields.

Image functionality requires PIL to be installed in the Python running Zope.

Install through QuickInstaller. Adds indexes to the catalog, so installation requires reindexing. This can take a while.

Depends on RhaptosRepository for 'truncate'. And, of course, all the content stuff, which is obvious.

The 'count' field on ContentSelectionLens objects currently depends on
all subobjects being 'SelectedContent' objects.  If this is changed
later and more objects are allowed as children, the expression for the
'count' field will have to be smarter and filter on type.