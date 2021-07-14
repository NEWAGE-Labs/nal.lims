from bika.lims.browser.bika_listing import BikaListingView
from bika.lims import api
from bika.lims import bikaMessageFactory as _
import collections
from Products.Five.browser import BrowserView
import pyodbc
import pandas as pd
import datetime as date

class ICPJSView(BrowserView):

    def getDFHeaders(self):
        conn = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
                              'Server=10.1.10.49\ITEVA;'
                              'Database=Instrument R;'
                              'Port=15555;'
                              'UID=sa;'
                              'PWD=Thermo-123;')

        today = date.date.today()
        today = "'{0}'".format(today)
        sql = "SELECT top 1 m.Name as [Method Name], se.Name as [Run Name], sa.Name as [Sample Name], el.ElementSymbol as [Element], el.AverageResult as [Average Read], el.PrintAverageResult as [Formatted Result], el.PercentRSD as [RSD], CAST('' as VARCHAR(8)) as [RSD Flag], CAST(NULL as FLOAT(5)) as [First Read], CAST(NULL as FLOAT(5)) as [Second Read], CAST(NULL as FLOAT(5)) as [Third Read], sa.Id as [Sample Id], el.LineIndex as [Line Index] " \
        + "FROM ElementLines el "\
        + "JOIN Samples sa on el.SampleId=sa.Id "\
        + "JOIN Sequences se on sa.sequenceid = se.id "\
        + "JOIN Methods m on m.Id = se.MethodId "\
        + "WHERE DATEDIFF(day, {0}, sa.AcquireDate) > -5".format(today)

        data = pd.read_sql(sql,conn)
        return data.columns

    def getDFBody(self):
        conn = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
                              'Server=10.1.10.49\ITEVA;'
                              'Database=Instrument R;'
                              'Port=15555;'
                              'UID=sa;'
                              'PWD=Thermo-123;')

        today = date.date.today()
        today = "'{0}'".format(today)
        sql = "SELECT m.Name as [Method Name], se.Name as [Run Name], sa.Name as [Sample Name], el.ElementSymbol as [Element], el.AverageResult as [Average Read], el.PrintAverageResult as [Formatted Result], el.PercentRSD as [RSD], CAST('' as VARCHAR(8)) as [RSD Flag], CAST(NULL as FLOAT(5)) as [First Read], CAST(NULL as FLOAT(5)) as [Second Read], CAST(NULL as FLOAT(5)) as [Third Read], sa.Id as [Sample Id], el.LineIndex as [Line Index] " \
        + "FROM ElementLines el "\
        + "JOIN Samples sa on el.SampleId=sa.Id "\
        + "JOIN Sequences se on sa.sequenceid = se.id "\
        + "JOIN Methods m on m.Id = se.MethodId "\
        + "WHERE DATEDIFF(day, {0}, sa.AcquireDate) > -5".format(today)

        data = pd.read_sql(sql,conn)
        body = []
        for i, row in data.iterrows():
            body.append(row)
        # html = sql_query.to_html()
        return body

class ICPDisplayView(BikaListingView):
    """"""

    def query():
        conn = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
                              'Server=10.1.10.49\ITEVA;'
                              'Database=Instrument R;'
                              'Port=15555;'
                              'UID=sa;'
                              'PWD=Thermo-123;')

        today = date.date.today()
        today = "'{0}'".format(today)
        sql = "SELECT m.Name as [Method Name], se.Name as [Run Name], sa.Name as [Sample Name], el.ElementSymbol as [Element], el.AverageResult as [Average Read], el.PrintAverageResult as [Formatted Result], el.PercentRSD as [RSD], CAST('' as VARCHAR(8)) as [RSD Flag], CAST(NULL as FLOAT(5)) as [First Read], CAST(NULL as FLOAT(5)) as [Second Read], CAST(NULL as FLOAT(5)) as [Third Read], sa.Id as [Sample Id], el.LineIndex as [Line Index] " \
        + "FROM ElementLines el "\
        + "JOIN Samples sa on el.SampleId=sa.Id "\
        + "JOIN Sequences se on sa.sequenceid = se.id "\
        + "JOIN Methods m on m.Id = se.MethodId "\
        + "WHERE DATEDIFF(day, {0}, sa.AcquireDate) > -5".format(today)

        data = pd.read_sql(sql,conn)
        return data


    def __init__(self, context, request):
        super(ICPDisplayView, self).__init__(context, request)

        self.catalog = "portal_catalog"
        self.contentFilter = {
            "portal_type": "InstrumentResult",
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
            ("sample", {
                "title": _("Sample"),
                "index": "title", }),
            ("analyte", {
                "title": _("Analyte"),}),
            ("result", {
                "title": _("Result"),}),
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
        item['sample'] = obj.sample
        item['analyte'] = obj.analyte
        item['result'] = obj.result
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
