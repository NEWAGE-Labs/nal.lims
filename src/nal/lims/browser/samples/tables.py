from bika.lims import api
from bika.lims.browser.analyses.qc import QCAnalysesView
from nal.lims.browser.analyses.view import AnalysesView


class LabAnalysesTable(AnalysesView):
    """Lab Analyses Listing Table for ARs
    """

    def __init__(self, context, request):
        """ Odd use case where we DO have to copy the core method's code because:
        Instead of giving a core or custom parent a custom child, we're giving a
        core child a custom parent, so we need to treat the core child like a
        custom child.

        Could potentially solve by overriding the inheritance of the core child
        from here, and calling its __init__() """


        super(LabAnalysesTable, self).__init__(context, request)

        self.contentFilter.update({
            "getPointOfCapture": "lab",
            "getAncestorsUIDs": [api.get_uid(context)]
        })

        self.form_id = "lab_analyses"
        self.allow_edit = True
        self.show_workflow_action_buttons = True
        self.show_select_column = True
        self.show_search = False
