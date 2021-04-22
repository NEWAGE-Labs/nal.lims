from bika.lims.interfaces import IAnalysisRequest
from Products.ATContentTypes.content import schemata
from archetypes.schemaextender.interfaces import IOrderableSchemaExtender
from archetypes.schemaextender.interfaces import IBrowserLayerAwareExtender
from archetypes.schemaextender.interfaces import ISchemaModifier
from bika.lims.fields import ExtStringField
from bika.lims.fields import ExtBooleanField
from bika.lims.fields import ExtDateTimeField
from bika.lims.browser.widgets import DateTimeWidget
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

        ExtDateTimeField(
            'DateOfSampling',
            widget=DateTimeWidget(
                label="Date Sampled",
                description="The Date the sample was taken",
                render_own_label=True,
                show_time=False,
                datepicker_nofuture=1,
                visible={
                    'edit':'visible',
                    'view':'visible',
                    'add':'edit',
                    'header_table':'visible',
                },
            )
        ),

        ExtStringField(
            'TimeofSampling',
            widget=StringWidget(
                label="Time Sampled",
                description="The time of day the sample was taken",
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
        schema['DateSampled'].widget.required = False

        schema['Template'].widget.visible = False
        schema['Container'].widget.visible = False
        schema['Preservation'].widget.visible = False
        schema['DatePreserved'].widget.visible = False
        schema['Preserver'].widget.visible = False
        schema['ClientOrderNumber'].widget.visible = False
        schema['Attachment'].widget.visible = False
        schema['InvoiceExclude'].widget.visible = False
        schema['Composite'].widget.visible = False
        schema['EnvironmentalConditions'].widget.visible = False
        schema['Priority'].widget.visible = False
        schema['SampleCondition'].widget.visible = False
        schema['SamplingDeviation'].widget.visible = False
        schema['ClientReference'].widget.visible = False
        schema['InternalUse'].widget.visible = False
        schema['DateSampled'].widget.visible = False
        schema['SamplingDate'].widget.visible = False
        schema['PrimaryAnalysisRequest'].widget.visible = False
        schema['Sampler'].widget.visible = False
        schema['ScheduledSamplingSampler'].widget.visible = False
        schema['StorageLocation'].widget.visible = False
        return schema
