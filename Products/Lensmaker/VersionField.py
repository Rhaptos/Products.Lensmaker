"""
Archetypes Field for storage (and specifically indexing) of X.y version as orderable tuple of ints.

Author: J. Cameron Cooper (jccooper@rice.edu)
Copyright (C) 2007 Rice University. All rights reserved.

This software is subject to the provisions of the GNU Lesser General
Public License Version 2.1 (LGPL).  See LICENSE.txt for details.
"""
from AccessControl import ClassSecurityInfo

from Products.Archetypes.public import Field
from Products.Archetypes.public import StringField, SelectionWidget

from config import PROJECTNAME

class TupleVersionField(StringField):
    """A field that falls back (when provided with no data) to some expression."""
    _properties = Field._properties.copy()
    _properties.update({
        'type' : 'fallback',
        'searchable': 0,
        #'index_method': '_at_edit_accessor',  # use getRaw to index,
        })

    security  = ClassSecurityInfo()
    
    #security.declarePrivate('set')
    #def set(self, instance, value, **kwargs):
        #"""Store 'value', a string representing a version.
        #"""
        #ObjectField.set(self, instance, value, **kwargs)


    security.declarePrivate('getRaw')
    def getRaw(self, instance, aslist=False, **kwargs):
        """Return the value of the version as a string. Example: '1.10'
        """
        return StringField.get(self, instance, **kwargs)

    security.declarePrivate('get')
    def get(self, instance, aslist=False, **kwargs):
        """Return the value of the version as a list of integers. Example: [1,10]
        Except (and this is important!) if there is no value or our value is 'latest', then
        return an empty list: []
        
        The OOBTree, probably through Python cmp(), sorts all tuples after all lists. So
        if we make the versions as lists and the "no version" as a tuple, we will get no-version
        entries as "high" values instead of low. Only tuples, apparently, order above tuples.
        
        This is not guaranteed to be stable, and we absolutely must have a test for at least this! TODO!
        """
        val = StringField.get(self, instance, **kwargs)
        if not val or val == 'latest': # 'latest' and '' sort to end...
            return tuple()  # ...tricksy. See docstring.
        else:
            try:
                return [int(x) for x in val.split('.')]
            except ValueError:  # probably a mistake. TODO: should we just let this float?
                return val      #                           not doing so, we could get bad comparisons...

try:
    from Products.Archetypes.Registry import registerField

    registerField(TupleVersionField,
                  title='TupleVersionField',
                  description=('Store versions as orderable tuple of ints.',))
except ImportError:
    pass   # we are probably in a < 1.2 version of Archetypes

#############################################################################

class TupleVersionWidget(SelectionWidget):
    """Widget for TupleVersionField that displays split version as a version string.
    """
    _properties = SelectionWidget._properties.copy()
    _properties.update({
        'macro' : "tupleversion",  # TODO: implement macro
        })
try:
  from Products.Archetypes.Registry import registerWidget

  registerWidget(TupleVersionWidget,
                 title='TupleVersion',
                 description='Display tuple of integers as normal version string.',
                 used_for=('Products.%s.FallBack.FallBackField' % PROJECTNAME,)
                 )
except ImportError:
  pass # this is expected for Archetypes pre-1.2

