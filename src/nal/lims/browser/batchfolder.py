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
from senaite.core.catalog import SENAITE_CATALOG

class BatchFolderContentsView(BikaBatchFolderContentsView):
    """Custom Listing View for all Batches in nal.lims
    """

    def __init__(self, context, request):
        super(BatchFolderContentsView, self).__init__(context, request)

        self.catalog = SENAITE_CATALOG
        self.contentFilter = {
            "portal_type": "Batch",
            "sort_on": "created",
            "sort_order": "descending",
            "is_active": True,
        }

        self.context_actions = {}

        self.show_select_all_checkbox = True
        self.show_select_column = True
        self.pagesize = 30

        batch_image_path = "/++resource++bika.lims.images/batch_big.png"
        self.icon = "{}{}".format(self.portal_url, batch_image_path)
        self.title = self.context.translate(_("SDGs")) #Customized the Title
        self.description = ""

        self.columns = collections.OrderedDict((
            ("Title", {
                "title": _("Internal SDG ID"),
                "index": "title",
		"sortable": True}),
            ("Progress", {
                "title": _("Progress"),
                "index": "getProgress",
                "sortable": True,
                "toggle": False}),
            ("Matrices", {
                "title": _("Matrices"),
                "toggle": True, }),
            ("Platforms", {
                "title": _("Platforms"),
                "toggle": True, }),
            ("Client", {
                "title": _("Client"),
                "index": "getClientTitle", }),
            ("Grower", {
                "title": _("Grower"),
                "toggle": True,
                "sortable": True, }),
            ("ClientID", {
                "title": _("Client ID"),
                "index": "getClientID", }),
            ("Description", {
                "title": _("Description"),
                "toggle": False,
                "sortable": False, }),
            ("SDGDate", {
                "title": _("Received Date"),
                "sortable": True, }),
            ("SDGTime", {
                "title": _("Received Time"),
                "sortable": True, }),
            ("BatchID", {
                "title": _("SDG ID"),  #Customized the Title
                "index": "getId", }),
            # ("ClientBatchID", {
            #     "title": _("Client Batch ID"),
            #     "index": "getClientBatchID", }),  #Hid this field
            ("state_title", {
                "title": _("State"),
                "toggle": False,
                "sortable": False, }),
            ("created", {
                "title": _("Created"),
                "toggle": False,
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
            },
        }

        if IClient.providedBy(self.context):
            self.context_actions[_("Export All SDGs as .CSV")] = {
                "url": "@@clientcsvexport/",
                "permission": AddBatch,
                "icon": "++resource++bika.lims.images/control_big.png"
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

    def get_platforms(self, obj):
        platforms = []
        #Get Analysis Services from Analyses from Analysis Requests from Batch
        analyses = [api.get_object(an) for ar in obj.getAnalysisRequests() for an in map(api.get_object,ar.getAnalyses())]

        for analysis in analyses:
            service = analysis.getAnalysisService()
            keyword = service.Keyword
            category = service.getCategory().title
            if category == 'Metals and Trace Elements' and keyword not in ['mercury','flouride', 'chloride', 'sulfate'] and "ICP" not in platforms:
                platforms.append("ICP")
            if keyword in ['mercury'] and "Mercury" not in platforms:
                platforms.append("Mercury")
            if keyword in ['lead','copper'] and any(['EGLE' in p.title for p in analysis.aq_parent.getProfiles()]) and "EGLE Pb/Cu" not in platforms:
                platforms.append("EGLE Pb/Cu")
            if keyword in ['chloride','ammonia','ammonium','nitrogen_nitrate','nitrogen_nitrite','nitrogen_ammonia','nitrogen_ammonium','sugars','sugars_fructose','sugars_glucose','sugars_sucrose'] and "Gallery" not in platforms:
                platforms.append("Gallery")
            if keyword in ['nitrogen','carbon'] and "LECO" not in platforms:
                platforms.append("LECO")
            if keyword in ['brix'] and "Brix" not in platforms:
                platforms.append("Brix")
            if keyword in ['ph'] and "pH" not in platforms:
                platforms.append("pH")
            if keyword in ['out_of_scope'] and "Outside Scope" not in platforms:
                platforms.append("Outside Scope")
            if keyword in ["temperature","volume","weight"] and "Common" not in platforms:
                platforms.append("Common")
            if keyword in ['carbonate','bicarbonate','alkalinity'] and "Carbonates" not in platforms:
                platforms.append("Carbonates")
            if keyword in ['ec','soluble_salts'] and "Conductivity" not in platforms:
                platforms.append("Conductivity")
            if 'plate' in keyword and "Petrifilm" not in platforms:
                platforms.append("Petrifilm")
            if 'aspergillus' in keyword or keyword in ['pythium','fusarium','hop_latent_viroid','cryptosporidium_parvum'] and "External Micro" not in platforms:
                platforms.append("External Micro")
            if 'c18' in keyword and "EGLE Micro" not in platforms:
                platforms.append("EGLE Micro")
            if 'pa' in keyword and 'c18' not in keyword and "PCR" not in platforms:
                platforms.append("PCR")

        return platforms

    def get_matrices(self, obj):
        matrices = []
        moptions = ['sap','waste','drinking','water','fertilizer','soil','root','swab','tissue','solid','food','fruit','air']
        for i in obj.getAnalysisRequests():
            matrix = i.getSampleType().Title() if i.getSampleType() else ''
            for option in moptions:
                if option in matrix.lower() and option not in matrices:
                    matrices.append(option)
        return matrices

    def get_grower_contact(self, obj):
        batch = obj
        contact = batch.getReferences(relationship="SDGGrowerContact")
	if len(contact) > 0:
	    contact = contact[0]
	elif hasattr(batch,'GrowerContact') and batch.GrowerContact is not None and batch.GrowerContact != '':
	    contact = api.get_object_by_uid(batch.GrowerContact)
        else:
            contact = None
        contact_name = ''
        if contact:
            contact_name = contact.Firstname + " " + contact.Surname
        return contact_name

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
        date = obj.SDGDate.strftime("%m/%d/%Y")
	time = obj.SDGTime
        #Get Matrices
        matrices = self.get_matrices(obj)
        #Get Platforms
        platforms = self.get_platforms(obj)

        # total sample progress
        progress = obj.getProgress()
        item["Progress"] = progress
        item["replace"]["Progress"] = get_progress_bar_html(progress)

        item["BatchID"] = bid
        item["ClientBatchID"] = cbid
        item["Matrices"] = ', '.join(matrices)
        item["Platforms"] = ', '.join(platforms)
        item["replace"]["BatchID"] = get_link(url, bid)
        item["Title"] = title
        item["replace"]["Title"] = get_link(url, title)
        item["created"] = self.ulocalized_time(created, long_format=True)
        item["SDGDate"] = date
	item["SDGTime"] = time
        item["Grower"] = self.get_grower_contact(obj)

        if client:
            client_url = api.get_url(client) + "/batches"
            client_name = client.getName()
            client_id = client.getClientID()
            item["Client"] = client_name
            item["ClientID"] = client_id
            item["replace"]["Client"] = get_link(client_url, client_name)
            item["replace"]["ClientID"] = get_link(client_url, client_id)

        return item
