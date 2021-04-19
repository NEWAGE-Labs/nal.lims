from bika.lims.browser.bika_listing import BikaListingView
from bika.lims import api
from bika.lims import bikaMessageFactory as _
import collections
# from Products.Five.browser import BrowserView
import pyodbc
import pandas as pd

class ICPDisplayView(BikaListingView):
    """"""

    def query():
        conn = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
                            'Server=tcp:192.168.1.100,1433;'
                            'Database=Instrument R;'
                            'UID=linux;'
                            'PWD=password;'
                            'Trusted_Connection=no;')

        sql = "SELECT * FROM Samples as s where DATEDIFF(day, '2021/04/16', s.AcquireDate) = 0"

        data = pd.read_sql(sql,conn)
        return data


    def __init__(self, context, request):
        super(ICPDisplayView, self).__init__(context, request)

        self.catalog = "bika_catalog"
        self.contentFilter = {
            "portal_type": "Batch",
            "sort_on": "title",
            "sort_order": "descending",
            "is_active": True,
        }

        self.context_actions = {}

        self.show_select_all_checkbox = False
        self.show_select_column = True
        self.pagesize = 30

        self.title = self.context.translate(_("ICP Results"))
        self.description = ""


        self.columns = collections.OrderedDict((
            ("title", {
                "title": _("Title"),
                "index": "title", }),
            ("desc", {
                "title": _("Progress")}),
        ))

        self.review_states = [
            {
                "id": "default",
                "title": _("Open"),
                "transitions": [],
                "columns": self.columns.keys(),
            },
            {
                "id": "all",
                "title": _("All"),
                "transitions": [],
                "columns": self.columns.keys(),
            },
        ]


    def folderitem(self, obj, item, index):
        obj = api.get_object(obj)
        title = api.get_title(obj)
        desc = api.get_description(obj)
        item['title'] = title
        item['desc'] = desc
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
