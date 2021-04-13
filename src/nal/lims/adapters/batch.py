from bika.lims.interfaces import IBatch
from Products.ATContentTypes.content import schemata
from archetypes.schemaextender.interfaces import IOrderableSchemaExtender
from archetypes.schemaextender.interfaces import IBrowserLayerAwareExtender
from archetypes.schemaextender.interfaces import ISchemaModifier
from bika.lims.fields import ExtStringField
from bika.lims import bikaMessageFactory as _
from zope.component import adapts
from zope.interface import implements
from nal.lims.interfaces import INalLimsLayer
from Products.Archetypes.public import StringField
from Products.Archetypes.public import StringWidget

class BatchSchemaExtender(object):
    adapts(IBatch)
    implements(IOrderableSchemaExtender, IBrowserLayerAwareExtender)
    layer = INalLimsLayer

    fields = [
        ExtStringField(
            "SDGDateTime",
            required=True,
            widget=StringWidget(
                label="SDG Received Date/Time",
                description="The Date and Time the Sample Delivery Group was received by the lab.",
            )
        ),
    ]

    def __init__(self, context):
        self.context = context

    def getOrder(self, schematas):
        return schematas

    def getFields(self):
        return self.fields

class BatchSchemaModifier(object):
    adapts(IBatch)
    implements(ISchemaModifier)

    def __init__(self, context):
        self.context = context

    def fiddle(self, schema):
        schema['BatchID'].widget.label = "SDG ID"
        schema['BatchLabels'].widget.label = "SDG Labels"
        schema['title'].widget.label = _("Project Name")
        schema['title'].widget.description = _("If no value is entered,"
                                               " the SDG ID will be used instead.")
        schema['BatchDate'].widget.visible = False
        schema['ClientBatchID'].widget.visible = False
        schema.moveField('SDGDateTime', after='Client')
        return schema
