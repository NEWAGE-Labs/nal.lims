import collections

from bika.lims import api
from bika.lims import bikaMessageFactory as _
from bika.lims.api.security import check_permission
from bika.lims.browser.bika_listing import BikaListingView
from bika.lims.interfaces import IClient
from bika.lims.permissions import AddBatch
from bika.lims.utils import get_link
from bika.lims.utils import get_progress_bar_html


class TimeclockFolderView(BikaListingView):
    """Listing View for all Batches in the System
    """

    def __init__(self, context, request):
        super(TimeclockFolderView, self).__init__(context, request)

        self.catalog = "portal_catalog"
        self.contentFilter = {
            "portal_type": "Timeclock",
            "sort_on": "created",
            "sort_order": "descending",
            "is_active": True,
        }

        self.context_actions = {}

        self.show_select_all_checkbox = True
        self.show_select_column = True
        self.pagesize = 10

        self.title = self.context.translate(_("Timeclock"))
        self.description = ""


        self.columns = collections.OrderedDict((
            ("personnel", {
                "title": _("Personnel"),
                "index": "title", }),
            ("type", {
                "title": _("Clock In/Out"),}),
            ("date", {
                "title": _("Date/Time"),}),
            ("hours", {
                "title": _("Hours"),}),
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
        super(TimeclockFolderView, self).update()

        if self.context.portal_type == "TimeClockFolder":
            self.request.set("disable_border", 1)

        #Fix permissions
        self.context_actions = {
            _("Clock In/Out"): {
                "url": "@@timeclock/",
                "permission": AddBatch,
                "icon": "++resource++bika.lims.images/to_follow.png"
            },
        }

    def folderitem(self, obj, item, index):
        obj = api.get_object(obj)
        url = api.get_url(obj)
        desc = api.get_description(obj)
        item['personnel'] = obj.personnel
        item['type'] = obj.type
        item['hours'] = obj.hours
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
