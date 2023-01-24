from archetypes.schemaextender.interfaces import IOrderableSchemaExtender
from archetypes.schemaextender.interfaces import IBrowserLayerAwareExtender
from archetypes.schemaextender.interfaces import ISchemaModifier
from bika.lims import bikaMessageFactory as _
from bika.lims.interfaces import ILabContact
from bika.lims.interfaces import IAnalysisProfile
from bika.lims.browser.widgets.recordswidget import RecordsWidget
from bika.lims.browser.widgets import ReferenceWidget
from nal.lims.fields import ExtBooleanField
from nal.lims.fields import ExtRecordsField
from nal.lims.interfaces import INalLimsLayer
from nal.lims.vocabularies import units_vocabulary
from Products.ATContentTypes.content import schemata
from Products.Archetypes.public import BooleanWidget
from zope.component import adapts
from zope.interface import implements

class AnalysisProfileSchemaExtender(object):
    adapts(IAnalysisProfile)
    implements(IOrderableSchemaExtender, IBrowserLayerAwareExtender)
    layer = INalLimsLayer

    fields = [

    ]

    def __init__(self, context):
        self.context = context

    def getOrder(self, schematas):
        return schematas

    def getFields(self):
        return self.fields

class AnalysisProfileSchemaModifier(object):
    adapts(IAnalysisProfile)
    implements(ISchemaModifier)

    def __init__(self, context):
        self.context = context

    def fiddle(self, schema):
        return schema
