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
        schema['Methods'].widget.visible = False
        schema.moveField('MethodRecords', before='Method')
        return schema
