import collections

from bika.lims import api
from bika.lims import bikaMessageFactory as _
from Products.Five.browser import BrowserView
from Products.statusmessages.interfaces import IStatusMessage
import pandas as pd

class SDGCSVExportView(BrowserView):

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):

        rootpath = '/mnt'
        path = '/Data/LIMS Sap CSV Exports/'
        filepath = path + self.context.title + '.csv'
        fullpath = rootpath + filepath
        export_dict = {}
        cols = [
            'Sample Number',
            'Received',
            'dSampled',
            'dResultsConfirmed',
            'dReportIssued',
            'dRecCompleted',
            'Grower',
            'Block',
            'Crop',
            'Specimen #',
            'Customer Code',
            'EC (W)',
            'Phosphorus (Sap-ICP)',
            'Calcium (Sap-ICP)',
            'Manganese (Sap-ICP)',
            'Zinc (Sap-ICP)',
            'Sulfur (Sap-ICP)',
            'Copper (Sap-ICP)',
            'Magnesium (Sap-ICP)',
            'Iron (Sap-ICP)',
            'Boron (Sap-ICP)',
            'Brix (Sap)',
            'pH (sap)',
            'Cl (sap)',
            'Sodium (Sap-ICP)',
            'Silicon (Sap-ICP)',
            'Aluminium (Sap-ICP)',
            'Cobalt (Sap-ICP)',
            'Molybdenum (Sap-ICP)',
            'NH4-N',
            'TN~',
            'Total Sugars',
            'N (sap)',
            'Nitrogen as Nitrate',
            'K/Ca Ratio',
            'Nitrogen Conversion Efficiency',
        ]
        #initialize dictionary of lists
        for i in range(len(cols)):
            export_dict[cols[i]] = []
        for i in self.context.getAnalysisRequests():
            if api.is_active(i) and i.getSampleType() == 'Sap':
                export_dict[cols[0]].append(i.id)

                received = self.context.SDGDate.strftime('%m-%d-%Y') + " " + self.context.SDGTime
                export_dict[cols[1]].append(received)

                sampled = i.DateOfSampling.strftime('%m-%d-%Y') + " " + i.TimeOfSampling
                export_dict[cols[2]].append(sampled)

                confirmed = i.getDateVerified()
                export_dict[cols[3]].append(confirmed)

                export_dict[cols[4]].append('')
                export_dict[cols[5]].append('')

                export_dict[cols[6]].append(i.getClient().Name)

                export_dict[cols[7]].append('')
                export_dict[cols[8]].append('')
                export_dict[cols[9]].append('')
                export_dict[cols[10]].append('')
                export_dict[cols[11]].append('')
                export_dict[cols[12]].append('')
                export_dict[cols[13]].append('')
                export_dict[cols[14]].append('')
                export_dict[cols[15]].append('')
                export_dict[cols[16]].append('')
                export_dict[cols[17]].append('')
                export_dict[cols[18]].append('')
                export_dict[cols[19]].append('')
                export_dict[cols[20]].append('')
                export_dict[cols[21]].append('')
                export_dict[cols[22]].append('')
                export_dict[cols[23]].append('')
                export_dict[cols[24]].append('')
                export_dict[cols[25]].append('')
                export_dict[cols[26]].append('')
                export_dict[cols[27]].append('')
                export_dict[cols[28]].append('')
                export_dict[cols[29]].append('')
                export_dict[cols[30]].append('')
                export_dict[cols[31]].append('')
                export_dict[cols[32]].append('')
                export_dict[cols[33]].append('')
                export_dict[cols[34]].append('')
                export_dict[cols[35]].append('')



        df = pd.DataFrame()
        for i in range(len(cols)):
            df[cols[i]] = export_dict[cols[i]]
        df.to_csv(fullpath)
        IStatusMessage(self.request).addStatusMessage(
                u"{} Successfully Exported to: {}".format(self.context.title, filepath)
            )
        self.request.response.redirect(api.get_url(self.context))
