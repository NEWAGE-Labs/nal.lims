from Products.Archetypes.public import StringField
from Products.Archetypes.public import StringWidget
from Products.Archetypes.references import HoldingReference
from Products.ATContentTypes.content import schemata
from Products.CMFCore.utils import getToolByName
from Products.Archetypes.atapi import FileField as ExtFileField
from Products.Archetypes.atapi import FileWidget
from Products.Archetypes.Widget import CalendarWidget
from AccessControl import ClassSecurityInfo
from archetypes.schemaextender.interfaces import IOrderableSchemaExtender
from archetypes.schemaextender.interfaces import IBrowserLayerAwareExtender
from archetypes.schemaextender.interfaces import ISchemaModifier
from bika.lims.fields import ExtStringField
from bika.lims import bikaMessageFactory as _
from bika.lims.interfaces import IBatch
from bika.lims.fields import ExtReferenceField
from bika.lims.fields import ExtDateTimeField
from bika.lims.browser.widgets import ReferenceWidget
from zope.component import adapts
from zope.interface import implements
from nal.lims.interfaces import INalLimsLayer
from datetime import date



class BatchSchemaExtender(object):
    adapts(IBatch)
    implements(IOrderableSchemaExtender, IBrowserLayerAwareExtender)
    layer = INalLimsLayer
    security = ClassSecurityInfo()

    fields = [
        ExtDateTimeField(
            "SDGDateTime",
            required=True,
            default_method="now",
            widget=CalendarWidget(
                label="Date Received",
                description="The Date the Sample Delivery Group was received by the lab.",
            )
        ),

        ExtStringField(
            'ReportContact',
            widget=StringWidget(
                label=_("Report Contact"),
                description=_("Optional field. Used if there is a secondary client the results are being tested for."),
                visible=True,
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
        ExtFileField(
            'COC',
            widget=FileWidget(
                label="Chain Of Custody",
                description="Select a printed COC to attach.",
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
        schema['title'].widget.label = _("Project Name")
        schema['title'].widget.description = _("Optional field. If no value is entered,"
                                               " the SDG ID will be used instead.")
        schema['BatchDate'].widget.visible = False
        schema['ClientBatchID'].widget.visible = False
        schema['Client'].required = True
        schema['description'].widget.label = "SDG Notes"
        schema['description'].widget.description = "Additional details about the SDG"
        schema['Remarks'].widget.visible = False

        schema.moveField('SDGDateTime', after='Client')
        schema.moveField('ProjectContact', after='SDGDateTime')
        schema.moveField('SamplerContact', after='ProjectContact')
        schema.moveField('title', after='SamplerContact')
        schema.moveField('ReportContact', after='title')
        schema.moveField('BatchLabels', after='ReportContact')
        schema.moveField('COC', after='BatchLabels')
        schema.moveField('description', after='COC')
        return schema
