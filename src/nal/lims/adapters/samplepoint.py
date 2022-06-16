from bika.lims.interfaces import ISamplePoint
from Products.ATContentTypes.content import schemata
from archetypes.schemaextender.interfaces import IOrderableSchemaExtender
from archetypes.schemaextender.interfaces import IBrowserLayerAwareExtender
from archetypes.schemaextender.interfaces import ISchemaModifier
from nal.lims.vocabularies import MBGTypes
from bika.lims.browser.widgets import SelectionWidget
from Products.Archetypes.public import StringWidget
# from Products.Archetypes.public import StringField as ExtStringField
from nal.lims.fields import ExtStringField
from nal.lims.interfaces import INalLimsLayer
from bika.lims import bikaMessageFactory as _
from zope.component import adapts
from zope.interface import implements

class SamplePointSchemaExtender(object):
    adapts(ISamplePoint)
    implements(IOrderableSchemaExtender, IBrowserLayerAwareExtender)
    layer = INalLimsLayer

    fields = [
        ExtStringField(
            "MBGType",
            vocabulary=MBGTypes,
            widget=SelectionWidget(
                label="MBG Location Type",
                format="radio",
                render_own_label=False,
            )
        ),
        ExtStringField(
            "WSSN",
            widget=StringWidget(
                label="WSSN",
            )
        ),
        ExtStringField(
            "FormattedAddress",
            widget=StringWidget(
                label=_("Formatted Address"),
                description="How the address should appear on a Report if different from the \"title\""
            ),
        ),
    ]

    def __init__(self, context):
        self.context = context

    def getOrder(self, schematas):
        return schematas

    def getFields(self):
        return self.fields

class SamplePointSchemaModifier(object):
    adapts(ISamplePoint)
    implements(ISchemaModifier)
    layer = INalLimsLayer

    def __init__(self, context):
        self.context = context

    def fiddle(self, schema):
        schema['Latitude'].widget.visible = False
        schema['Longitude'].widget.visible = False
        schema['Elevation'].widget.visible = False
        schema['SamplingFrequency'].widget.visible = False
        schema['Composite'].widget.visible = False
        schema['SampleTypes'].widget.visible = False

        schema.moveField('FormattedAddress', after='description')
        schema.moveField('MBGType', after='FormattedAddress')
        schema.moveField('WSSN', after='MBGType')
        schema.moveField('AttachmentFile', after='WSSN')
        return schema
