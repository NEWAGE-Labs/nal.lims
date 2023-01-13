from bika.lims.interfaces import IAnalysis
from Products.ATContentTypes.content import schemata
from archetypes.schemaextender.interfaces import IOrderableSchemaExtender
from archetypes.schemaextender.interfaces import IBrowserLayerAwareExtender
from archetypes.schemaextender.interfaces import ISchemaModifier
from nal.lims.fields import ExtStringField
from nal.lims.fields import ExtBooleanField
from nal.lims.fields import ExtFloatField
from bika.lims import bikaMessageFactory as _
from zope.component import adapts
from zope.interface import implements
from nal.lims.interfaces import INalLimsLayer
from Products.Archetypes.public import StringWidget
from Products.Archetypes.public import BooleanWidget
from Products.Archetypes.Widget import DecimalWidget
from Products.CMFCore.permissions import View
from bika.lims.permissions import FieldEditAnalysisResult
from Products.Archetypes.Schema import Schema

class AnalysisSchemaExtender(object):
    adapts(IAnalysis)
    implements(IOrderableSchemaExtender, IBrowserLayerAwareExtender)
    layer = INalLimsLayer

    fields = [
        ExtBooleanField(
            'ShowTotal',
            schemata="Analysis",
            widget=BooleanWidget(
                label="Total",
                description="Toggle whether to display the word 'Total' on the report for the element. Ex. Total Nitrogen",
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
            'ShowMethodInName',
            schemata="Analysis",
            widget=BooleanWidget(
                label="Show Method",
                description="Toggle whether to display the name of the method on the report",
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
            'AnalysisDateTime',
            write_permission=View,
            read_permission=View,
            widget=StringWidget(
                label=_("Analysis Date/Time"),
            ),
        ),

        ExtBooleanField(
            'Inconclusive',
            write_permission=View,
            read_permission=View,
            widget=BooleanWidget(
                label=_("Inconclusive"),
            ),
        ),

        ExtFloatField(
            'Weight',
            write_permission=View,
            read_permission=View,
            widget=DecimalWidget(
                label=_("Weight (in Grams)"),
            )
        ),

        ExtFloatField(
            'Volume',
            write_permission=View,
            read_permission=View,
            widget=DecimalWidget(
                label=_("Volume"),
            )
        ),

        ExtFloatField(
            'Dilution',
            write_permission=View,
            read_permission=View,
            widget=DecimalWidget(
                label=_("Dilution"),
            )
        ),
    ]

    def __init__(self, context):
        self.context = context

    def getOrder(self, schematas):
        return schematas

    def getFields(self):
        return self.fields

class AnalysisSchemaModifier(object):
    adapts(IAnalysis)
    implements(ISchemaModifier)

    def __init__(self, context):
        self.context = context

    def fiddle(self, schema):

        schema['Analyst'].write_permission = View
        schema['Analyst'].read_permission = View

        return schema
