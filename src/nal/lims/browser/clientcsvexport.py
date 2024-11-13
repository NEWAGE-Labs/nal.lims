import collections

from bika.lims import api
from bika.lims import bikaMessageFactory as _
from Products.Five.browser import BrowserView
from Products.statusmessages.interfaces import IStatusMessage
from nal.lims import api as napi

class ClientCSVExportView(BrowserView):

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):

        rootpath = '/mnt'
        path = '/Data/LIMS CSV Exports/'
        path2 = '/Temp/LIMS Exports/'
        client = self.context
        filepath = path + client.getName().replace('/','_') + '.csv'
        filepath2 = path2 + client.getName().replace('/','_') + '.csv'
        fullpath = rootpath + filepath
        fullpath2 = rootpath + filepath2
        sdgs_full = map(api.get_object,api.search({'portal_type':'Batch'}))
        sdgs_active = []
        sdgs = []
        for i in sdgs_full:
            if api.get_workflow_status_of(i) != 'cancelled' and len(i.getAnalysisRequests()) > 0:
                sdgs_active.append(i)

        for i in sdgs_active:
            if i.getClient().id == client.id:
                sdgs.append(i)

        ARs = []
        for i in sdgs:
	    if api.get_workflow_status_of(i) not in ['cancelled','invalid']:
            	ARs = ARs + [ar for ar in map(api.get_object,i.getAnalysisRequests()) if api.get_workflow_status_of(ar) not in ['retracted','rejected','invalid','cancelled']]

        df = napi.getCSVDFbyAR(ARs)

        df.to_csv(fullpath)
        df.to_csv(fullpath2)

        IStatusMessage(self.request).addStatusMessage(
                u"{} Successfully Exported to: {}".format(self.context.title, filepath)
            )

        self.request.response.redirect(api.get_url(self.context))
