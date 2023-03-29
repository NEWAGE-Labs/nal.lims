from bika.lims.interfaces import IClient
from Products.ATContentTypes.content import schemata
from archetypes.schemaextender.interfaces import IOrderableSchemaExtender
from archetypes.schemaextender.interfaces import IBrowserLayerAwareExtender
from archetypes.schemaextender.interfaces import ISchemaModifier
# from Products.Archetypes.public import StringField as ExtStringField
from nal.lims.fields import ExtStringField
from nal.lims.fields import ExtBooleanField
from nal.lims.fields import ExtFileField
from Products.Archetypes.atapi import ReferenceField as ExtReferenceField
from bika.lims.browser.widgets import ReferenceWidget
from bika.lims import bikaMessageFactory as _
from zope.component import adapts
from zope.interface import implements
from nal.lims.interfaces import INalLimsLayer
from Products.Archetypes.public import StringField
from Products.Archetypes.public import StringWidget
from Products.Archetypes.public import BooleanWidget
from Products.Archetypes.atapi import FileWidget

class ClientSchemaExtender(object):
    adapts(IClient)
    implements(IOrderableSchemaExtender, IBrowserLayerAwareExtender)
    layer = INalLimsLayer

    fields = [
        ExtStringField(
            "MBGGrowerNumber",
            schemata="Grower Info",
            required=False,
            widget=StringWidget(
                label="MBG Grower Number",
                description="",
            )
        ),
        ExtStringField(
            "TBGrowerNumber",
            schemata="Grower Info",
            required=False,
            widget=StringWidget(
                label="True Blue Grower Number",
                description="",
            )
        ),
        ExtBooleanField(
            "CSV",
            required=False,
            widget=BooleanWidget(
                label="Send CSV",
                description="Does this client get a .CSV file sent with their results?",
            )
        ),
         ExtReferenceField(
            'GrowerList',
            schemata="Grower Info",
            multiValued=1,
            relationship="ClientDistributor",
            allowed_types=('Client',),
            mode="rw",
            widget=ReferenceWidget(
                label=_("List of Client Growers"),
                description=_("A list of associated Growers for Consultants."),
                size=20,
                catalog_name="portal_catalog",
                base_query={"is_active": True,
                            "sort_limit": 30,
                            "sort_on": "sortable_title",
                            "sort_order": "ascending"},
                showOn=True,
                popup_width='400px',
                colModel=[
                    {'columnName': 'Name', 'width': '50',
                     'label': _('Name')},
                    {'columnName': 'ClientID', 'width': '50',
                     'label': _('Email Address')},
                ],
                ui_item='Name',
            ),
        ),
        ExtFileField(
            'Logo',
            widget=FileWidget(
                label="Logo",
                description="Logo for the client to add to reports",
                visible = True,
            )
        ),
        ExtStringField(
            "ReferralComment",
            required=False,
            widget=StringWidget(
                label="Referral Comment",
                description="How was this Client referred to NEW AGE?",
            )
        ),
    ]

    def __init__(self, context):
        self.context = context

    def getOrder(self, schematas):
        return schematas

    def getFields(self):
        return self.fields

class ClientSchemaModifier(object):
    adapts(IClient)
    implements(ISchemaModifier)

    def __init__(self, context):
        self.context = context

    def fiddle(self, schema):
	schema.moveField('ReferralComment', after='EmailAddress')

        schema["BulkDiscount"].widget.visible = False
        schema["MemberDiscountApplies"].widget.visible = False
        schema["TaxNumber"].widget.visible = False
        schema["ClientID"].widget.label = "NAL Number"
	schema["ClientID"].widget.description = "The Unique ID associated with the client. Example: 'NAL23-456'"
        schema["PhysicalAddress"].required = True
        schema["CSV"].widget.visible = True
        # schema["PhysicalAddress"].schemata = "default"
        return schema
