import collections

from bika.lims import api
from bika.lims import bikaMessageFactory as _
from bika.lims.api.security import check_permission
from bika.lims.browser.bika_listing import BikaListingView
from bika.lims.interfaces import IClient
from bika.lims.permissions import AddBatch
from bika.lims.utils import get_link
from bika.lims.utils import get_progress_bar_html
from nal.lims.interfaces import IPurchaseOrderFolder


from bika.lims.browser.bika_listing import BikaListingView
from bika.lims.config import PROJECTNAME
from plone.app.folder.folder import ATFolder
from plone.app.folder.folder import ATFolderSchema
from Products.Archetypes import atapi
from Products.ATContentTypes.content import schemata
from senaite.core.interfaces import IHideActionsMenu
from zope.interface.declarations import implements

from senaite.core.catalog import SETUP_CATALOG





class PurchaseOrderFolderView(BikaListingView):
    """Listing View for all Batches in the System
    """

    def __init__(self, context, request):
        super(PurchaseOrderFolderView, self).__init__(context, request)

        self.catalog = "portal_catalog"
        self.contentFilter = {
            "portal_type": "PurchaseOrder",
            "sort_on": "created",
            "sort_order": "descending",
            "is_active": True,
        }

        self.context_actions = {
            _("Add"): {
                "url": "createObject?type_name=PurchaseOrder",
                "permission": AddBatch,
                "icon": "++resource++bika.lims.images/add.png"}
        }

        self.show_select_all_checkbox = True
        self.show_select_column = True
        self.pagesize = 20

        self.title = self.context.translate(_("Purchase Orders"))
        self.description = ""


        self.columns = collections.OrderedDict((
            ("po_num", {
                "title": _("Purchase Order Number"),
                "index": "title", }),
            ("details", {
                "title": _("Order Details"),}),
            ("est_arrival", {
                "title": _("Estimated Arrival"),}),
            ("cost", {
                "title": _("Total Cost"),}),
            ("types", {
                "title": _("Purchase Types"),}),
        ))

        self.review_states = [
            {
                "id": "default",
                "title": _("All"),
                "transitions": [],
                "columns": self.columns.keys(),
            },
        ]

    def update(self):
        """Before template render hook
        """
        super(PurchaseOrderFolderView, self).update()

        if self.context.portal_type == "PurchaseOrderFolder":
            self.request.set("disable_border", 1)

        #Fix permissions
        """self.context_actions = {
            _("Clock In/Out"): {
                "url": "@@timeclock/",
                "permission": AddBatch,
                "icon": "++resource++bika.lims.images/to_follow.png"
            },
        }"""

    def folderitem(self, obj, item, index):
        obj = api.get_object(obj)
        url = api.get_url(obj)
        desc = api.get_description(obj)
        item['po_num'] = obj.po_num
	item['details'] = obj.details
        item['est_arrival'] = '' if obj.est_arrival is None else obj.est_arrival.strftime('%m/%d/%Y')
        item['cost'] = obj.total_price
#	item['types'] = '' if obj.line_items is None else set(sorted([li.type for li in obj.line_items]))

        return item

schema = ATFolderSchema.copy()


class PurchaseOrderFolder(ATFolder):
    implements(IPurchaseOrderFolder, IHideActionsMenu)
    displayContentsTab = False
    schema = schema


schemata.finalizeATCTSchema(schema, folderish=True, moveDiscussion=False)
atapi.registerType(PurchaseOrderFolder, PROJECTNAME)
