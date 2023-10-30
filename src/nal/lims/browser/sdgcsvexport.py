import collections

from bika.lims import api
from bika.lims import bikaMessageFactory as _
from Products.Five.browser import BrowserView
from Products.statusmessages.interfaces import IStatusMessage
import pandas as pd
from nal.lims import api as napi
from math import floor
from math import log10

class SDGCSVExportView(BrowserView):

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):

        rootpath = '/mnt'
        path = '/Data/LIMS CSV Exports/'
        sdg = self.context
        filepath = path + sdg.title + '.csv'
        fullpath = rootpath + filepath
        export_dict = {}

	df = napi.getSDGCSV(sdg)

        df.to_csv(fullpath)

        IStatusMessage(self.request).addStatusMessage(
                u"{} Successfully Exported to: {}".format(self.context.title, filepath)
            )

        self.request.response.redirect(api.get_url(self.context))
