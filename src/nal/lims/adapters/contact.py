from bika.lims.interfaces import IContact
from Products.ATContentTypes.content import schemata
from archetypes.schemaextender.interfaces import IOrderableSchemaExtender
from archetypes.schemaextender.interfaces import IBrowserLayerAwareExtender
from archetypes.schemaextender.interfaces import ISchemaModifier
from bika.lims.browser.widgets import SelectionWidget
from Products.Archetypes.public import BooleanWidget
from Products.Archetypes.public import StringWidget
# from Products.Archetypes.public import StringField as ExtStringField
from nal.lims.fields import ExtStringField
from nal.lims.fields import ExtBooleanField
from nal.lims.interfaces import INalLimsLayer
from bika.lims import bikaMessageFactory as _
from zope.component import adapts
from zope.interface import implements

class ContactSchemaExtender(object):
    adapts(IContact)
    implements(IOrderableSchemaExtender, IBrowserLayerAwareExtender)
    layer = INalLimsLayer

    fields = [
        ExtStringField(
            "Initials",
            schemata='default',
            widget=StringWidget(
                label="Initials",
            )
        ),

        ExtBooleanField(
            "Approved",
            schemata='default',
            widget=BooleanWidget(
                label="Approved for Results",
            )
        ),
    ]

    def __init__(self, context):
        self.context = context

    def getOrder(self, schematas):
        return schematas

    def getFields(self):
        return self.fields

class ContactSchemaModifier(object):
    adapts(IContact)
    implements(ISchemaModifier)
    layer = INalLimsLayer

    def __init__(self, context):
        self.context = context

    def fiddle(self, schema):
        schema.moveField('Initials', after='Middleinitial')
        schema.moveField('Approved', after='Department')
        schema['Middleinitial'].widget.visible = False
        return schema
