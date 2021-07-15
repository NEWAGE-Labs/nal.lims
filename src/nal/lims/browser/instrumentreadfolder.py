import collections

from bika.lims import api
from bika.lims import bikaMessageFactory as _
from bika.lims.api.security import check_permission
from bika.lims.browser.bika_listing import BikaListingView
from bika.lims.interfaces import IClient
from bika.lims.permissions import AddBatch
from bika.lims.utils import get_link
from bika.lims.utils import get_progress_bar_html


class InstrumentReadFolderView(BikaListingView):
    """Listing View for all Batches in the System
    """

    def __init__(self, context, request):
        super(InstrumentReadFolderView, self).__init__(context, request)

        self.catalog = "portal_catalog"
        self.contentFilter = {
            "portal_type": "InstrumentRead",
            "sort_on": "title",
            "sort_order": "descending",
            "is_active": True,
        }

        self.context_actions = {}

        self.show_select_all_checkbox = False
        self.show_select_column = False
        self.pagesize = 30

        self.title = self.context.translate(_("Instrument Reads"))
        self.description = ""


        self.columns = collections.OrderedDict((
            # ("instrument", {
            #     "title": _("Instrument"),
            #     "index": "title", }),
            # ("start", {
            #     "title": _("Start of Read"),}),
            # ("end", {
            #     "title": _("End of Read"),}),
        ))

        self.review_states = [
            {
                "id": "default",
                "title": _("Open"),
                "transitions": [],
                "columns": self.columns.keys(),
            },
            # {
            #     "id": "all",
            #     "title": _("All"),
            #     "transitions": [],
            #     "columns": self.columns.keys(),
            # },
        ]

    def update(self):
        """Before template render hook
        """
        super(InstrumentReadFolderView, self).update()

        if self.context.portal_type == "InstrumentReadFolder":
            self.request.set("disable_border", 1)

        #Fix permissions
        self.context_actions = {
            _("Import ICP"): {
                "url": "@@icpimport/",
                "permission": AddBatch,
                "icon": "++resource++bika.lims.images/add.png"
            },
            _("Import Gallery"): {
                "url": "@@galleryimport/",
                "permission": AddBatch,
                "icon": "++resource++bika.lims.images/add.png"
            },
            _("Import pH"): {
                "url": "@@phimport/",
                "permission": AddBatch,
                "icon": "++resource++bika.lims.images/add.png"
            },
            _("Import EC or SS/TDS"): {
                "url": "@@ecimport/",
                "permission": AddBatch,
                "icon": "++resource++bika.lims.images/add.png"
            },
            _("Import Total Nitrogen"): {
                "url": "@@totalnitrogenimport/",
                "permission": AddBatch,
                "icon": "++resource++bika.lims.images/add.png"
            }
        }

    def folderitem(self, obj, item, index):
        # obj = api.get_object(obj)
        # url = api.get_url(obj)
        # instrument = obj.instrument
        # desc = api.get_description(obj)
        # item['instrument'] = instrument
        # item["replace"]["instrument"] = get_link(url, instrument)
        # item['start'] = obj.start
        # item['end'] = obj.end
        return item
    #
    # def before_render(self):
    #     """Before template render hook
    #     """
    #     # Call `before_render` from the base class
    #     super(ICPDisplayView, self).before_render()
    #
    #     # Render the Add button if the user has the AddClient permission
    #     if check_permission(AddClient, self.context):
    #         self.context_actions[_("Add")] = {
    #             "url": "createObject?type_name=Client",
    #             "icon": "++resource++bika.lims.images/add.png"
    #         }
    #
    #     # Display a checkbox next to each client in the list if the user has
    #     # rights for ModifyPortalContent
    #     self.show_select_column = check_permission(ModifyPortalContent,
    #                                                self.context)
