from bika.lims.interfaces import ILabContact
from Products.ATContentTypes.content import schemata
from archetypes.schemaextender.interfaces import IOrderableSchemaExtender
from archetypes.schemaextender.interfaces import IBrowserLayerAwareExtender
from archetypes.schemaextender.interfaces import ISchemaModifier
from bika.lims.browser.widgets import ReferenceWidget
from bika.lims import bikaMessageFactory as _
from zope.component import adapts
from zope.interface import implements
from nal.lims.interfaces import INalLimsLayer
from Products.Archetypes.public import BooleanWidget
from bika.lims.fields import ExtBooleanField

class LabContactSchemaExtender(object):
    adapts(ILabContact)
    implements(IOrderableSchemaExtender, IBrowserLayerAwareExtender)
    layer = INalLimsLayer

    fields = [
        ExtBooleanField(
            'is_clocked_in',
            default=False,
            widget=BooleanWidget(
                label="Is the personnel clocked in?",
                visible=True,
            )
        ),
    ]

    def __init__(self, context):
        self.context = context

    def getOrder(self, schematas):
        return schematas

    def getFields(self):
        return self.fields

class LabContactSchemaModifier(object):
    adapts(ILabContact)
    implements(ISchemaModifier)

    def __init__(self, context):
        self.context = context

    def fiddle(self, schema):
        return schema
