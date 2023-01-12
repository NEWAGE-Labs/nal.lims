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
# from Products.Archetypes.public import BooleanField as ExtBooleanField
from nal.lims.fields import ExtBooleanField
# from senaite.core.browser.fields.records import RecordsField
from nal.lims.fields import ExtRecordsField
from bika.lims.browser.widgets.recordswidget import RecordsWidget
from bika.lims.interfaces import IAnalysisService

class AnalysisServiceSchemaExtender(object):
    adapts(IAnalysisService)
    implements(IOrderableSchemaExtender, IBrowserLayerAwareExtender)
    layer = INalLimsLayer

    fields = [
        ExtRecordsField(
            "MethodRecords",
            schemata="Method",
            required=0,
            type="methods",
            subfields=(
                "methodid",
                "loq",
                "iso",
                "egle",
            ),
            required_subfields=(
                "methodid",
                "loq",
                "iso",
                "egle",
            ),
            subfield_labels={
                "methodid": _("Method"),
                "loq": _("Detection Limit"),
                "iso": _("ISO 17025 Accredited?"),
                "egle": _("EGLE Accredited?"),
            },
            subfield_types={
                "methodid": "string",
                "loq": "string",
                "iso": "boolean",
                "egle": "boolean",
            },
            subfield_sizes={
                "methodid": 1,
                "loq": 1,
            },
            subfield_vocabularies={
                "methodid": "_methods_vocabulary",
            },
            widget=RecordsWidget(
                label=_("Methods"),
                description=_(
                    "Available methods to perform the test"),
            )
        )
    ]

    def __init__(self, context):
        self.context = context

    def getOrder(self, schematas):
        return schematas

    def getFields(self):
        return self.fields

class AnalysisServiceSchemaModifier(object):
    adapts(IAnalysisService)
    implements(ISchemaModifier)

    def __init__(self, context):
        self.context = context

    def fiddle(self, schema):

        schema['ExponentialFormatPrecision'].required = False
        schema['ExponentialFormatPrecision'].widget.visible = False
        schema['LowerDetectionLimit'].required = False
        schema['LowerDetectionLimit'].widget.visible = False
        schema['UpperDetectionLimit'].required = False
        schema['UpperDetectionLimit'].widget.visible = False
        schema['DetectionLimitSelector'].required = False
        schema['DetectionLimitSelector'].widget.visible = False
        schema['AllowManualDetectionLimit'].required = False
        schema['AllowManualDetectionLimit'].widget.visible = False
        schema['AttachmentRequired'].required = False
        schema['AttachmentRequired'].widget.visible = False
        schema['DuplicateVariation'].required = False
        schema['DuplicateVariation'].widget.visible = False
        schema['Accredited'].required = False
        schema['Accredited'].widget.visible = False
        schema['PointOfCapture'].required = False
        schema['PointOfCapture'].widget.visible = False
        schema['VAT'].required = False
        schema['VAT'].widget.visible = False
        schema['Department'].required = False
        schema['Department'].widget.visible = False
        schema['CommercialID'].required = False
        schema['CommercialID'].widget.visible = False
        schema['ProtocolID'].required = False
        schema['ProtocolID'].widget.visible = False
        schema['Remarks'].required = False
        schema['Remarks'].widget.visible = False
        schema['ScientificName'].required = False
        schema['ScientificName'].widget.visible = False
        schema['BulkPrice'].required = False
        schema['BulkPrice'].widget.visible = False
        schema['Precision'].required = False
        schema['Precision'].widget.visible = False
        schema['SelfVerification'].required = False
        schema['SelfVerification'].widget.visible = False
        schema['StringResult'].required = False
        schema['StringResult'].widget.visible = False
        schema['DefaultResult'].required = False
        schema['DefaultResult'].widget.visible = False
        schema['ShortTitle'].required = False
        schema['ShortTitle'].widget.visible = False
        schema['SortKey'].required = False
        schema['SortKey'].widget.visible = False
        schema['Price'].widget.label = _("Price (Excluding Tax)")
        schema['Keyword'].widget.label = _("Keyword")
        schema['Keyword'].widget.description = _("The unqiue keyword used to identify the analysis in imports, exports, and calculations regardless of if the Title changes. Cannot be changed once at least 1 analysis has been made.")

        schema['Methods'].widget.visible = False
        schema.moveField('MethodRecords', before='Method')
        return schema
