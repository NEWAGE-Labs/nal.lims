
from Products.Archetypes.references import HoldingReference
from Products.ATContentTypes.content import schemata
from Products.CMFCore.utils import getToolByName
from AccessControl import ClassSecurityInfo
from archetypes.schemaextender.interfaces import IOrderableSchemaExtender
from archetypes.schemaextender.interfaces import IBrowserLayerAwareExtender
from archetypes.schemaextender.interfaces import ISchemaModifier
from bika.lims import bikaMessageFactory as _
from bika.lims.interfaces import IBatch
from Products.Archetypes.atapi import FileField as ExtFileField
from nal.lims.fields import ExtReferenceField
# from Products.Archetypes.public import StringField as ExtStringField
# from Products.Archetypes.public import DateTimeField as ExtDateTimeField
from nal.lims.fields import ExtStringField
from nal.lims.fields import ExtDateTimeField
from Products.Archetypes.public import StringWidget
from Products.Archetypes.atapi import FileWidget
from bika.lims.browser.widgets import DateTimeWidget
from bika.lims.browser.widgets import ReferenceWidget
from zope.component import adapts
from zope.interface import implements
from nal.lims.interfaces import INalLimsLayer

class BatchSchemaExtender(object):
    adapts(IBatch)
    implements(IOrderableSchemaExtender, IBrowserLayerAwareExtender)
    layer = INalLimsLayer
    security = ClassSecurityInfo()

    fields = [
        ExtDateTimeField(
            "SDGDate",
            required=True,
            widget=DateTimeWidget(
                label="Date Received",
                description="The Date the Sample Delivery Group was received by the lab.",
                show_time=False,
                datepicker_nofuture=1,
            )
        ),

        ExtStringField(
            'SDGTime',
            required=True,
            widget=StringWidget(
                label=_("Time Received"),
                description=_("The Time the Sample Delivery Group was received by the lab."),
            ),
        ),

        ExtStringField(
            'ReportContact',
            widget=StringWidget(
                label=_("Report Contact"),
                description=_("Optional field. Used if there is a secondary client the results are being tested for."),
            ),
        ),

        ExtReferenceField(
            'ProjectContact',
            required=True,
            default_method='getContactUIDForUser',
            allowed_types=('Contact',),
            referenceClass=HoldingReference,
            relationship="SDGProjectContact",
            mode="rw",
            widget=ReferenceWidget(
                label=_("Project Contact"),
                size=20,
                helper_js=("bika_widgets/referencewidget.js",
                           "++resource++bika.lims.js/contact.js"),
                description=_("The main contact for the project"),
                catalog_name="portal_catalog",
                base_query={"is_active": True,
                            "sort_limit": 50,
                            "sort_on": "sortable_title",
                            "sort_order": "ascending"},
                showOn=True,
                popup_width='400px',
                colModel=[
                    {'columnName': 'Fullname', 'width': '50',
                     'label': _('Name')},
                    {'columnName': 'EmailAddress', 'width': '50',
                     'label': _('Email Address')},
                ],
                ui_item='Fullname',
            ),
        ),

        ExtReferenceField(
            'SamplerContact',
            required=True,
            default_method='getContactUIDForUser',
            allowed_types=('Contact',),
            referenceClass=HoldingReference,
            relationship="SDGSamplerContact",
            mode="rw",
            widget=ReferenceWidget(
                label=_("Sampled By"),
                size=20,
                helper_js=("bika_widgets/referencewidget.js",
                           "++resource++bika.lims.js/contact.js"),
                description=_("The person who performed the sampling method."),
                catalog_name="portal_catalog",
                base_query={"is_active": True,
                            "sort_limit": 50,
                            "sort_on": "sortable_title",
                            "sort_order": "ascending"},
                showOn=True,
                popup_width='400px',
                colModel=[
                    {'columnName': 'Fullname', 'width': '50',
                     'label': _('Name')},
                    {'columnName': 'EmailAddress', 'width': '50',
                     'label': _('Email Address')},
                ],
                ui_item='Fullname',
            ),
        ),

        ExtReferenceField(
            'GrowerContact',
            required=False,
            default_method='getContactUIDForUser',
            allowed_types=('Contact',),
            referenceClass=HoldingReference,
            relationship="SDGGrowerContact",
            mode="rw",
            widget=ReferenceWidget(
                label=_("Grower Contact"),
                size=20,
                helper_js=("bika_widgets/referencewidget.js",
                           "++resource++bika.lims.js/contact.js"),
                description=_("Optional. Independant grower testing via a consultation client."),
                catalog_name="portal_catalog",
                base_query={"is_active": True,
                            "sort_limit": 50,
                            "sort_on": "sortable_title",
                            "sort_order": "ascending"},
                showOn=True,
                popup_width='400px',
                colModel=[
                    {'columnName': 'Fullname', 'width': '50',
                     'label': _('Name')},
                    {'columnName': 'EmailAddress', 'width': '50',
                     'label': _('Email Address')},
                ],
                ui_item='Fullname',
            ),
        ),
        ExtFileField(
            'COC',
            widget=FileWidget(
                label="Chain Of Custody",
                description="Select a printed COC to attach.",
                visible=False,
            )
        ),
    ]

#Custom function for Contact Fields
    security.declarePublic('getContactUIDForUser')
    security.declarePublic('getCurrentDate')

    def getContactUIDForUser(self):
        """get the UID of the contact associated with the authenticated user
        """
        mt = getToolByName(self, 'portal_membership')
        user = mt.getAuthenticatedMember()
        user_id = user.getUserName()
        pc = getToolByName(self, 'portal_catalog')
        r = pc(portal_type='Contact',
               getUsername=user_id)
        if len(r) == 1:
            return r[0].UID

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
        schema['title'].widget.label = _("Internal SDG ID")
        schema['title'].widget.description = _("The 12-character ID based on the received date/time of the sample."
                                              "Example: 0101230800FL")
        schema['BatchDate'].widget.visible = False
        schema['BatchDate'].widget.required = False
        schema['ClientBatchID'].widget.visible = False
        schema['Client'].widget.visible = True
        schema['Client'].required = False
        schema['description'].widget.label = "SDG Notes"
        schema['description'].widget.description = "Additional details about the SDG"
        schema['Remarks'].widget.visible = False

        schema.moveField('SDGDate', after='Client')
        schema.moveField('SDGTime', after='SDGDate')
        schema.moveField('title', after='SDGTime')
        schema.moveField('ProjectContact', after='title')
        schema.moveField('SamplerContact', after='ProjectContact')
        schema.moveField('GrowerContact', after='SamplerContact')
        schema.moveField('ReportContact', after='GrowerContact')
        schema.moveField('BatchLabels', after='ReportContact')
        schema.moveField('COC', after='BatchLabels')
        schema.moveField('description', after='COC')
        return schema
