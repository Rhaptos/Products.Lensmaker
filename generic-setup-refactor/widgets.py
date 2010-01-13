from Products.Archetypes.public import StringWidget
from Products.Archetypes.Registry import registerWidget

class ColorWidget(StringWidget):
    _properties = StringWidget._properties.copy()
    _properties.update({
        'macro' : "colorchooser",
        })


registerWidget(ColorWidget,
             title='Color',
             description='Like StringWidget, stores the hex value of a color.',
             used_for=('Products.Archetypes.Field.StringField',)
             )


from Products.validation import validation
from Products.validation.validators import RegexValidator
validation.register(RegexValidator('isHexColor', r'^[0-9a-fA-F]{6}$', title='', description='',
                   errmsg='is not a hexadecimal color code.'))

