Lensmaker
=========

Provides a means to create **lenses**. Lenses are collections of content,
usually created to organize content by a single author or organization. One
can uses lenses to filter content by author, topic, subject level (k-12).
Lenses can be combined to focus on specific areas of interest.

This Zope Product is part of the `Rhaptos system <http://rhaptos.org>`_,
created to run `Connexions <http://cnx.org>`_.

The installation of this product adds indexes to the catalog, which requires the catalog be reindexed. The reindexing process can take a while.

Dependencies
------------

This product depends on Products.RhaptosCollection at the moment, but
should be separable with some work on separating some specific shared fields.

TODO
----

The original readme said, "Depends on RhaptosRepository for 'truncate'. And,
of course, all the content stuff, which is obvious." But I don't find this to
be very obvious. There are no direct references to the
Products.RhaptosRepository library. Is RhaptosRepository still a dependency?

The original readme said, "The 'count' field on ContentSelectionLens objects
currently depends on all subobjects being 'SelectedContent' objects.  If this
is changed later and more objects are allowed as children, the expression for
the 'count' field will have to be smarter and filter on type." Is this still
true?

Author and Copyright
--------------------

Author: J Cameron Cooper (jccooper@rice.edu)
Created: June 2007
Copyright: copyright (c) 2007, Rice University. All rights reserved.
