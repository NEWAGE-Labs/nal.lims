import collections

from bika.lims import api
from bika.lims import bikaMessageFactory as _
from Products.Five.browser import BrowserView
from Products.statusmessages.interfaces import IStatusMessage

class MBGExportView(BrowserView):

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):

        portal = api.get_portal()
        mbgexportfolder = portal.mbgexport #folder?
        print("MBGExport Folder is: {0}".format(mbgexportfolder))

        sdgs = map(api.get_object, api.search({'portal_type':'Batch'}))
        this_batch = []
        for i in sdgs:
            if u'Send to MBG' in i.getLabelNames() and api.get_workflow_status_of(i) == 'open':
                this_batch.append(i)

        samples = []
        for i in this_batch:
            for j in i.getAnalysisRequests():
                samples.append(j)

        print("Starting Analysis List")
        for i in samples:
            print(i)
        print("Ending Analysis List")

        export = api.create(mbgexportfolder,'MBGExport', count=len(this_batch))
        export.reindexObject()

        tcf_url = api.get_url(mbgexportfolder)
        print("Timeclock Folder URL is: {0}".format(tcf_url))

        IStatusMessage(self.request).addStatusMessage(
                u"Successfully Exported and Closed:"
            )
        self.request.response.redirect(tcf_url)
