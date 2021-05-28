from bika.lims.interfaces import IAnalysis
from Products.ATContentTypes.content import schemata
from archetypes.schemaextender.interfaces import IOrderableSchemaExtender
from archetypes.schemaextender.interfaces import IBrowserLayerAwareExtender
from archetypes.schemaextender.interfaces import ISchemaModifier
from bika.lims.fields import ExtStringField
from bika.lims import bikaMessageFactory as _
from zope.component import adapts
from zope.interface import implements
from nal.lims.interfaces import INalLimsLayer
from Products.Archetypes.public import StringWidget
from Products.CMFCore.permissions import View
from Products.Archetypes.Schema import Schema

class AnalysisSchemaExtender(object):
    adapts(IAnalysis)
    implements(IOrderableSchemaExtender, IBrowserLayerAwareExtender)
    layer = INalLimsLayer

    fields = [
        ExtStringField(
            'AnalysisDateTime',
            write_permission=View,
            read_permission=View,
            widget=StringWidget(
                label=_("Analysis Date/Time"),
            ),
        )
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
        return schema
