from bika.lims.interfaces import IAnalysisRequest
from Products.ATContentTypes.content import schemata
from archetypes.schemaextender.interfaces import IOrderableSchemaExtender
from archetypes.schemaextender.interfaces import IBrowserLayerAwareExtender
from archetypes.schemaextender.interfaces import ISchemaModifier
from bika.lims.fields import ExtStringField
from bika.lims.fields import ExtBooleanField
from bika.lims import bikaMessageFactory as _
from zope.component import adapts
from zope.interface import implements
from nal.lims.interfaces import INalLimsLayer
from Products.Archetypes.public import StringWidget
from Products.Archetypes.public import BooleanWidget

class AnalysisRequestSchemaExtender(object):
    adapts(IAnalysisRequest)
    implements(IOrderableSchemaExtender, IBrowserLayerAwareExtender)
    layer = INalLimsLayer

    fields = [
        ExtStringField(
            'PlantType',
            widget=StringWidget(
                label="Plant Type (Sap Samples)",
                description="The Plant Species or Crop the sample was taken from",
                render_own_label=True,
                visible={
                    'edit':'visible',
                    'view':'visible',
                    'add':'edit',
                    'header_table':'visible',
                },
            )
        ),

        ExtStringField(
            'Variety',
            widget=StringWidget(
                label="Variety (Sap Samples)",
                description="The Plant Variety or Cultivar the sample was taken from",
                render_own_label=True,
                visible={
                    'edit':'visible',
                    'view':'visible',
                    'add':'edit',
                    'header_table':'visible',
                },
            )
        ),

        ExtStringField(
            'GrowthStage',
            widget=StringWidget(
                label="Growth Stage (Sap Samples)",
                description="The development stage of the plant the sample was taken from",
                render_own_label=True,
                visible={
                    'edit':'visible',
                    'view':'visible',
                    'add':'edit',
                    'header_table':'visible',
                },
            )
        ),

        ExtBooleanField(
            'NewLeaf',
            widget=BooleanWidget(
                label="New Leaf (Sap Samples)",
                description="The sample is from the new growth of a plant",
                render_own_label=True,
                visible={
                    'edit':'visible',
                    'view':'visible',
                    'add':'edit',
                    'header_table':'visible',
                },
            )
        ),
    ]

    def __init__(self, context):
        self.context = context

    def getOrder(self, schematas):
        return schematas

    def getFields(self):
        return self.fields

class AnalysisRequestSchemaModifier(object):
    adapts(IAnalysisRequest)
    implements(ISchemaModifier)

    def __init__(self, context):
        self.context = context

    def fiddle(self, schema):
        schema['Batch'].widget.label = _("SDG")
        schema['Batch'].widget.description = _("The SDG of this sample")
        schema['Batch'].widget.colModel = [
            {'columnName': 'getId', 'width': '20',
             'label': _('SDG ID'), 'align': 'left'},
            {'columnName': 'Title', 'width': '20',
             'label': _('Title'), 'align': 'left'},
            # {'columnName': 'getClientBatchID', 'width': '20',
            #  'label': _('CBID'), 'align': 'left'},
            {'columnName': 'getClientTitle', 'width': '30',
             'label': _('Client'), 'align': 'left'},
        ]

        schema['SubGroup'].widget.label = _("Sample Pairings")
        schema['SubGroup'].widget.description = _("If this sample is part of a pair, assign both samples to the same Pair #")
        schema['Template'].widget.visible = False
        schema['Container'].widget.visible = False
        schema['Preservation'].widget.visible = False
        schema['ClientOrderNumber'].widget.visible = False
        return schema
