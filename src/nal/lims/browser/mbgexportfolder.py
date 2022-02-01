import collections

from bika.lims import api
from bika.lims import bikaMessageFactory as _
from bika.lims.api.security import check_permission
from bika.lims.browser.bika_listing import BikaListingView
from bika.lims.interfaces import IClient
from bika.lims.permissions import AddBatch
from bika.lims.utils import get_link
from bika.lims.utils import get_progress_bar_html


class MBGExportFolderView(BikaListingView):
    """Listing View for all Batches in the System
    """

    def __init__(self, context, request):
        super(MBGExportFolderView, self).__init__(context, request)

        self.catalog = "portal_catalog"
        self.contentFilter = {
            "portal_type": "MBGExport",
            "sort_on": "created",
            "sort_order": "descending",
            "is_active": True,
        }

        self.context_actions = {}

        self.show_select_all_checkbox = True
        self.show_select_column = True
        self.pagesize = 10

        self.title = self.context.translate(_("MBGExport"))
        self.description = ""


        self.columns = collections.OrderedDict((
            ("date", {
                "title": _("Date of Export"),
                "index": "created", }),
            ("count", {
                "title": _("Number of SDGs Exported"),}),
        ))

        self.review_states = [
            {
                "id": "default",
                "title": _("All"),
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
        super(MBGExportFolderView, self).update()

        if self.context.portal_type == "MBGExportFolder":
            self.request.set("disable_border", 1)

        #Fix permissions
        self.context_actions = {
            _("Export Open MBG SDGs"): {
                "url": "@@mbgexport/",
                "permission": AddBatch,
                "icon": "++resource++bika.lims.images/control_big.png"
            },
        }

    def folderitem(self, obj, item, index):
        obj = api.get_object(obj)
        url = api.get_url(obj)
        desc = api.get_description(obj)
        item['count'] = obj.count
        item['date'] = api.get_creation_date(obj).strftime('%m/%d/%Y %H:%M')
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
