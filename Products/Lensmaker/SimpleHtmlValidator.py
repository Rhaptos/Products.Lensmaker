"""
Archetypes validator for safe HTML, compatible with Plone 2.0.

Author: J. Cameron Cooper (jccooper@rice.edu)
Copyright (C) 2007 Rice University. All rights reserved.

This software is subject to the provisions of the GNU Lesser General
Public License Version 2.1 (LGPL).  See LICENSE.txt for details.
"""

from Products.validation.config import validation
from Products.validation.interfaces.IValidator import IValidator

from Products.CMFDefault.utils import scrubHTML

# the only users of this (either scrubHTML, isHTMLSafe, or safe_html trasnform) are other transforms
# so it's okay to monkey patch it. unfortunate that we must, though.
# value in VALID is apparently singleton-ness, and in NASTY whether it's really invalid or not
VALID_TAGS = { 'a'          : 1
             , 'b'          : 1
             , 'code'       : 1
             , 'div'        : 1
             , 'em'         : 1
             , 'i'          : 1
             , 'p'          : 1
             , 'span'       : 1
             , 'strong'     : 1
             , 'u'          : 1
             , 'br'         : 0
             }
NASTY_TAGS = { 'script'     : 1
             , 'object'     : 1
             , 'embed'      : 1
             , 'applet'     : 1
             , 'base'       : 1 #0
             , 'blockquote' : 1
             , 'body'       : 1
             , 'ul'         : 1
             , 'table'      : 1
             , 'tbody'      : 1
             , 'td'         : 1
             , 'th'         : 1
             , 'title'      : 1
             , 'tr'         : 1
             , 'tt'         : 1
             , 'pre'        : 1
             , 'img'        : 1 #0
             , 'kbd'        : 1
             , 'li'         : 1
             , 'link'       : 1 #type="script" hoses us
             , 'meta'       : 1 #0
             , 'ol'         : 1
             , 'h1'         : 1
             , 'h2'         : 1
             , 'h3'         : 1
             , 'h4'         : 1
             , 'h5'         : 1
             , 'h6'         : 1
             , 'head'       : 1
             , 'hr'         : 1 #0
             , 'html'       : 1
             , 'caption'    : 1
             , 'cite'       : 1
             , 'dl'         : 1
             , 'dt'         : 1
             , 'dd'         : 1
             }
from Products.CMFDefault import utils
utils._OLD_VALID_TAGS = utils.VALID_TAGS
utils.VALID_TAGS = VALID_TAGS
utils._OLD_NASTY_TAGS = utils.NASTY_TAGS
utils.NASTY_TAGS = NASTY_TAGS

from Products.CMFDefault.utils import StrippingParser, IllegalHTML
if not getattr(StrippingParser, '_old_unknown_starttag', None):
    StrippingParser._old_unknown_starttag = StrippingParser.unknown_starttag
    # monkey patch to disallow attrs other than a href. We actually could do this more elegantly,
    def unknown_starttag(self, tag, attrs):
        """ Delete all tags except for legal ones.
        """
        for k, v in attrs:
            if tag != 'a' and k.lower() != 'href':
                raise IllegalHTML, 'Attribute "%s" not allowed on <%s>.' % (k, tag)
        return self._old_unknown_starttag(tag, attrs)

    StrippingParser.unknown_starttag = unknown_starttag

class SimpleHtmlValidator:
    """Succeed only if a limited list of HTML tags is found. Also, HTML must be good.
    """

    __implements__ = IValidator
    
    def __init__(self, name, title='', description=''):
        self.name = name
        self.title = title or name
        self.description = description
    
    def __call__(self, value, *args, **kw):
        try:
            scrubHTML(value)
        except IllegalHTML, e:
            valid_tags = ",".join(["<%s>" % x for x in VALID_TAGS.keys()])
            return '%s Only the HTML tags %s accepted, and only the "href" attribute on <a>.' % (str(e), valid_tags)

validation.register(SimpleHtmlValidator('simple_safe_html'))
