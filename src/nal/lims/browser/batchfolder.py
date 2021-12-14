import collections
from bika.lims import api
from bika.lims import bikaMessageFactory as _
from bika.lims.api.security import check_permission
from bika.lims.browser.bika_listing import BikaListingView
from bika.lims.interfaces import IClient
from bika.lims.permissions import AddBatch
from bika.lims.utils import get_link
from bika.lims.utils import get_progress_bar_html
from bika.lims.browser.batchfolder import BatchFolderContentsView as BikaBatchFolderContentsView

class BatchFolderContentsView(BikaBatchFolderContentsView):
    """Custom Listing View for all Batches in nal.lims
    """

    def __init__(self, context, request):
        super(BatchFolderContentsView, self).__init__(context, request)

        self.catalog = "bika_catalog"
        self.contentFilter = {
            "portal_type": "Batch",
            "sort_on": "created",
            "sort_order": "descending",
            "is_active": True,
        }

        self.context_actions = {}

        self.show_select_all_checkbox = False
        self.show_select_column = True
        self.pagesize = 30

        batch_image_path = "/++resource++bika.lims.images/batch_big.png"
        self.icon = "{}{}".format(self.portal_url, batch_image_path)
        self.title = self.context.translate(_("SDGs")) #Customized the Title
        self.description = ""

        self.columns = collections.OrderedDict((
            ("Title", {
                "title": _("Title"),
                "index": "title", }),
            ("Progress", {
                "title": _("Progress"),
                "index": "getProgress",
                "sortable": True,
                "toggle": True}),
            ("BatchID", {
                "title": _("SDG ID"),  #Customized the Title
                "index": "getId", }),
            ("Matrices", {
                "title": _("Matrices"),
                "toggle": True, }),
            ("Description", {
                "title": _("Description"),
                "sortable": False, }),
            ("BatchDate", {
                "title": _("SDG Received Date"), }),
            ("Client", {
                "title": _("Client"),
                "index": "getClientTitle", }),
            ("ClientID", {
                "title": _("Client ID"),
                "index": "getClientID", }),
            # ("ClientBatchID", {
            #     "title": _("Client Batch ID"),
            #     "index": "getClientBatchID", }),  #Hid this field
            ("state_title", {
                "title": _("State"),
                "sortable": False, }),
            ("created", {
                "title": _("Created"),
                "index": "created",
            }),
        ))

        self.review_states = [
            {
                "id": "default",
                "contentFilter": {"review_state": "open"},
                "title": _("Open"),
                "transitions": [],
                "columns": self.columns.keys(),
            }, {
                "id": "closed",
                "contentFilter": {"review_state": "closed"},
                "title": _("Closed"),
                "transitions": [],
                "columns": self.columns.keys(),
            }, {
                "id": "cancelled",
                "title": _("Cancelled"),
                "transitions": [],
                "contentFilter": {"is_active": False},
                "columns": self.columns.keys(),
            }, {
                "id": "all",
                "title": _("All"),
                "transitions": [],
                "columns": self.columns.keys(),
            },
        ]

    def update(self):
        """Before template render hook
        """
        super(BatchFolderContentsView, self).update()

        if self.context.portal_type == "BatchFolder":
            self.request.set("disable_border", 1)

        # By default, only users with AddBatch permissions for the current
        # context can add batches.
        self.context_actions = {
            _("Add"): {
                "url": "createObject?type_name=Batch",
                "permission": AddBatch,
                "icon": "++resource++bika.lims.images/add.png"
            }
        }

        # If current user is a client contact and current context is not a
        # Client, then modify the url for Add action so the Batch gets created
        # inside the Client object to which the current user belongs. The
        # reason is that Client contacts do not have privileges to create
        # Batches inside portal/batches
        if not IClient.providedBy(self.context):
            # Get the client the current user belongs to
            client = api.get_current_client()
            if client and check_permission(AddBatch, client):
                add_url = self.context_actions[_("Add")]["url"]
                add_url = "{}/{}".format(api.get_url(client), add_url)
                self.context_actions[_("Add")]["url"] = add_url
                del(self.context_actions[_("Add")]["permission"])

    def folderitem(self, obj, item, index):
        """Applies new properties to the item (Batch) that is currently being
        rendered as a row in the list

        :param obj: client to be rendered as a row in the list
        :param item: dict representation of the batch, suitable for the list
        :param index: current position of the item within the list
        :type obj: ATContentType/DexterityContentType
        :type item: dict
        :type index: int
        :return: the dict representation of the item
        :rtype: dict
        """

        obj = api.get_object(obj)
        url = "{}/analysisrequests".format(api.get_url(obj))
        bid = api.get_id(obj)
        cbid = obj.getClientBatchID()
        title = api.get_title(obj)
        client = obj.getClient()
        created = api.get_creation_date(obj)
        date = obj.SDGDate.strftime("%b %d, %Y") + ' ' + obj.SDGTime
        matrices = []
        for i in obj.getAnalysisRequests():
            matrix = i.getSampleType().Title() if i.getSampleType() else ''
            if matrix == 'Sap' and 'sap' not in matrices:
                matrices.append('sap')
            elif matrix == 'Water, Drinking' and 'drinking water' not in matrices:
                matrices.append('drinking water')
            elif matrix == 'Water, Surface' and 'surface water' not in matrices:
                matrices.append('surface water')
            elif matrix == 'Water, Liquid Fertilizer' and 'liquid fertilizer' not in matrices:
                matrices.append('liquid fertilizer')

        # total sample progress
        progress = obj.getProgress()
        item["Progress"] = progress
        item["replace"]["Progress"] = get_progress_bar_html(progress)

        item["BatchID"] = bid
        item["ClientBatchID"] = cbid
        item["Matrices"] = ','.join(matrices)
        item["replace"]["BatchID"] = get_link(url, bid)
        item["Title"] = title
        item["replace"]["Title"] = get_link(url, title)
        item["created"] = self.ulocalized_time(created, long_format=True)
        item["BatchDate"] = date

        if client:
            client_url = api.get_url(client)
            client_name = client.getName()
            client_id = client.getClientID()
            item["Client"] = client_name
            item["ClientID"] = client_id
            item["replace"]["Client"] = get_link(client_url, client_name)
            item["replace"]["ClientID"] = get_link(client_url, client_id)

        return item
