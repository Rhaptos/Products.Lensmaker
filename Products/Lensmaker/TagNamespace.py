"""
TagNamespace.py - the TagNamespace content type.

Author: Hedley Roos (hedley@upfrontsystems.co.za)
Copyright (C) 2007 Rice University. All rights reserved.

This software is subject to the provisions of the GNU Lesser General
Public License Version 2.1 (LGPL).  See LICENSE.txt for details.
"""

from AccessControl import ClassSecurityInfo
from Products.Archetypes.atapi import *
from Products.Lensmaker.config import *

##code-section module-header #fill in your manual code here
from Products.CMFPlone import PloneMessageFactory as _
##/code-section module-header

schema = Schema((

    StringField(
        name='prefix',
        widget=StringWidget(
            description="Prefix is usually an abbreviated form of the title, e.g. for the title Assessment Standards the prefix may be AS.",
            label='Prefix',
            label_msgid='Lensmaker_label_prefix',
            description_msgid='Lensmaker_help_prefix',
            i18n_domain='Lensmaker',
        ),
        required=True,
        index="lens_catalog/FieldIndex",
    ),

    LinesField(
        name='tags',
        widget=LinesField._properties['widget'](
            description="Enter one tag per line. A tag consists of a term and a description. The first word is the term, and the rest of the line is the description. E.g. LO1:AS4 Learning Outcome 1: Investigates numeric and geometric patterns.",
            label='Tags',
            label_msgid='Lensmaker_label_tags',
            description_msgid='Lensmaker_help_tags',
            i18n_domain='Lensmaker',
        ),
        required=True
    ),

),
)

##code-section after-local-schema #fill in your manual code here
##/code-section after-local-schema


TagNamespace_schema = BaseSchema.copy() + \
    schema.copy()

##code-section after-schema #fill in your manual code here
##/code-section after-schema

class TagNamespace(BaseContent):
    """
    TagNamespace content type
    """
    security = ClassSecurityInfo()

    # This name appears in the 'add' box
    archetype_name = 'Tag Vocabulary'

    meta_type = 'TagNamespace'
    portal_type = 'TagNamespace'
    allowed_content_types = []
    filter_content_types = 0
    global_allow = 1
    #content_icon = 'TagNamespace.gif'
    immediate_view = 'base_view'
    default_view = 'base_view'
    suppl_views = ()
    typeDescription = "Tag Vocabulary"
    typeDescMsgId = 'description_edit_tagnamespace'

    _at_rename_after_creation = True

    schema = TagNamespace_schema

    ##code-section class-header #fill in your manual code here
    ##/code-section class-header

    # Methods
    def validate_tags(self, value):
        """
        Check that the set of terms for the tags do not contain collisions
        Also, check for characters that affect url traversal
        """
        if not value:
            return None

        view = self.restrictedTraverse('@@getNamespaceTagTerm')
        terms = []
        for tag in value:
            term = view('prefix', tag)
            if term in terms:
                return _("The term for %s appears more than once" % tag)
            for char in ['?', '&', '%', '::', '#']:
              if char in term[len('prefix::'):]:
                return _("The term may not contain ?, &, %, :: or # characters")

            terms.append(term)
        
    def validate_prefix(self, value):
        """
        Check for characters that affect url traversal
        """
        for char in value:
          if char in ['?', '&', '%', ':', '#']:
            return _("The prefix may not contain ?, &, %, : or # characters")

    def showEditableBorder(self, *args, **kwargs):
        """
        Abuse this nasty hook to always hide the border

        params:
            args, kwargs: ignored. Present to ensure method can be
                          called in any way.

        return:
            False
        """
        return False

registerType(TagNamespace, PROJECTNAME)
# end of class TagNamespace

##code-section module-footer #fill in your manual code here
##/code-section module-footer



