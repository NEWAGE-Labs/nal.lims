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
            if api.is_active(i) and i.getSampleType().title == 'Sap':
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

                export_dict[cols[7]].append(i.getSamplePoint().title)
                crop = i.CropType
                if crop is None:
                    crop = ''
                export_dict[cols[8]].append(crop)
                export_dict[cols[9]].append(i.getClientSampleID())
                export_dict[cols[10]].append('')

                #EC
                ec = -0.01
                found = False
                for i in range(20, 0, -1):
                    if found==False:
                        version = 'sap_ec-'+str(i)
                        if hasattr(self,version):
                            found = True
                            ec = float(self[version].Result)
                if found == False and self.sap_ec is not None:
                    ec = float(self.sap_ec.Result)

                if ec <= 0.01:
                    ec = -0.01

                export_dict[cols[11]].append(ec)

                #Phosphorus
                phosphorus = -0.01
                found = False
                for i in range(20, 0, -1):
                    if found==False:
                        version = 'sap_phosphorus-'+str(i)
                        if hasattr(self,version):
                            found = True
                            phosphorus = float(self[version].Result)
                if found == False and self.sap_phosphorus is not None:
                    phosphorus = float(self.sap_phosphorus.Result)

                if phosphorus <= 0.01:
                    phosphorus = -0.01
                export_dict[cols[12]].append(phosphorus)

                #calcium
                calcium = -0.01
                found = False
                for i in range(20, 0, -1):
                    if found==False:
                        version = 'sap_calcium-'+str(i)
                        if hasattr(self,version):
                            found = True
                            calcium = float(self[version].Result)
                if found == False and self.sap_calcium is not None:
                    calcium = float(self.sap_calcium.Result)

                if calcium <= 0.01:
                    calcium = -0.01

                export_dict[cols[13]].append(calcium)

                #manganese
                manganese = -0.01
                found = False
                for i in range(20, 0, -1):
                    if found==False:
                        version = 'sap_manganese-'+str(i)
                        if hasattr(self,version):
                            found = True
                            manganese = float(self[version].Result)
                if found == False and self.sap_manganese is not None:
                    manganese = float(self.sap_manganese.Result)

                if manganese <= 0.01:
                    manganese = -0.01

                export_dict[cols[14]].append(manganese)

                #zinc
                zinc = -0.01
                found = False
                for i in range(20, 0, -1):
                    if found==False:
                        version = 'sap_zinc-'+str(i)
                        if hasattr(self,version):
                            found = True
                            zinc = float(self[version].Result)
                if found == False and self.sap_zinc is not None:
                    zinc = float(self.sap_zinc.Result)

                if zinc <= 0.01:
                    zinc = -0.01

                export_dict[cols[15]].append(zinc)

                #sulfur
                sulfur = -0.01
                found = False
                for i in range(20, 0, -1):
                    if found==False:
                        version = 'sap_sulfur-'+str(i)
                        if hasattr(self,version):
                            found = True
                            sulfur = float(self[version].Result)
                if found == False and self.sap_sulfur is not None:
                    sulfur = float(self.sap_sulfur.Result)

                if sulfur <= 0.01:
                    sulfur = -0.01

                export_dict[cols[16]].append(sulfur)

                #copper
                copper = -0.01
                found = False
                for i in range(20, 0, -1):
                    if found==False:
                        version = 'sap_copper-'+str(i)
                        if hasattr(self,version):
                            found = True
                            copper = float(self[version].Result)
                if found == False and self.sap_copper is not None:
                    copper = float(self.sap_copper.Result)

                if copper <= 0.01:
                    copper = -0.01

                export_dict[cols[17]].append(copper)

                #magnesium
                magnesium = -0.01
                found = False
                for i in range(20, 0, -1):
                    if found==False:
                        version = 'sap_magnesium-'+str(i)
                        if hasattr(self,version):
                            found = True
                            magnesium = float(self[version].Result)
                if found == False and self.sap_magnesium is not None:
                    magnesium = float(self.sap_magnesium.Result)

                if magnesium <= 0.01:
                    magnesium = -0.01

                export_dict[cols[18]].append(magnesium)

                #iron
                iron = -0.01
                found = False
                for i in range(20, 0, -1):
                    if found==False:
                        version = 'sap_iron-'+str(i)
                        if hasattr(self,version):
                            found = True
                            iron = float(self[version].Result)
                if found == False and self.sap_iron is not None:
                    iron = float(self.sap_iron.Result)

                if iron <= 0.01:
                    iron = -0.01

                export_dict[cols[19]].append(iron)

                #boron
                boron = -0.01
                found = False
                for i in range(20, 0, -1):
                    if found==False:
                        version = 'sap_boron-'+str(i)
                        if hasattr(self,version):
                            found = True
                            boron = float(self[version].Result)
                if found == False and self.sap_boron is not None:
                    boron = float(self.sap_boron.Result)

                if boron <= 0.01:
                    boron = -0.01

                export_dict[cols[20]].append(boron)

                #brix
                brix = -0.01
                found = False
                for i in range(20, 0, -1):
                    if found==False:
                        version = 'sap_brix-'+str(i)
                        if hasattr(self,version):
                            found = True
                            brix = float(self[version].Result)
                if found == False and self.sap_brix is not None:
                    brix = float(self.sap_brix.Result)

                if brix <= 0.01:
                    brix = -0.01

                export_dict[cols[21]].append(brix)

                #ph
                ph = -0.01
                found = False
                for i in range(20, 0, -1):
                    if found==False:
                        version = 'sap_ph-'+str(i)
                        if hasattr(self,version):
                            found = True
                            ph = float(self[version].Result)
                if found == False and self.sap_ph is not None:
                    ph = float(self.sap_ph.Result)

                if ph <= 0.01:
                    ph = -0.01

                export_dict[cols[22]].append(ph)

                #chloride
                chloride = -0.01
                found = False
                for i in range(20, 0, -1):
                    if found==False:
                        version = 'sap_chloride-'+str(i)
                        if hasattr(self,version):
                            found = True
                            manganese = float(self[version].Result)
                if found == False and self.sap_chloride is not None:
                    chloride = float(self.sap_chloride.Result)

                if chloride <= 0.01:
                    chloride = -0.01

                export_dict[cols[23]].append(chloride)

                #sodium
                sodium = -0.01
                found = False
                for i in range(20, 0, -1):
                    if found==False:
                        version = 'sap_sodium-'+str(i)
                        if hasattr(self,version):
                            found = True
                            sodium = float(self[version].Result)
                if found == False and self.sap_sodium is not None:
                    sodium = float(self.sap_sodium.Result)

                if sodium <= 0.01:
                    sodium = -0.01

                export_dict[cols[24]].append(sodium)

                #silicon
                silicon = -0.01
                found = False
                for i in range(20, 0, -1):
                    if found==False:
                        version = 'sap_silicon-'+str(i)
                        if hasattr(self,version):
                            found = True
                            silicon = float(self[version].Result)
                if found == False and self.sap_silicon is not None:
                    silicon = float(self.sap_silicon.Result)

                if silicon <= 0.01:
                    silicon = -0.01

                export_dict[cols[25]].append(silicon)

                #aluminium
                aluminium = -0.01
                found = False
                for i in range(20, 0, -1):
                    if found==False:
                        version = 'sap_aluminum-'+str(i)
                        if hasattr(self,version):
                            found = True
                            aluminium = float(self[version].Result)
                if found == False and self.sap_aluminum is not None:
                    aluminium = float(self.sap_aluminum.Result)

                if aluminium <= 0.01:
                    aluminium = -0.01

                export_dict[cols[26]].append(aluminium)

                #cobalt
                cobalt = -0.01
                found = False
                for i in range(20, 0, -1):
                    if found==False:
                        version = 'sap_cobalt-'+str(i)
                        if hasattr(self,version):
                            found = True
                            cobalt = float(self[version].Result)
                if found == False and self.sap_cobalt is not None:
                    cobalt = float(self.sap_cobalt.Result)

                if cobalt <= 0.01:
                    cobalt = -0.01

                export_dict[cols[27]].append(cobalt)

                #molybdenum
                molybdenum = -0.01
                found = False
                for i in range(20, 0, -1):
                    if found==False:
                        version = 'sap_molybdenum-'+str(i)
                        if hasattr(self,version):
                            found = True
                            molybdenum = float(self[version].Result)
                if found == False and self.sap_molybdenum is not None:
                    molybdenum = float(self.sap_molybdenum.Result)

                if molybdenum <= 0.01:
                    molybdenum = -0.01

                export_dict[cols[28]].append(molybdenum)

                #Nitrogen from Ammonium
                n_nh4 = -0.01
                found = False
                for i in range(20, 0, -1):
                    if found==False:
                        version = 'sap_nitrogen_as_ammonium-'+str(i)
                        if hasattr(self,version):
                            found = True
                            n_nh4 = float(self[version].Result)
                if found == False and self.sap_nitrogen_as_ammonium is not None:
                    n_nh4 = float(self.sap_nitrogen_as_ammonium.Result)

                if n_nh4 <= 0.01:
                    n_nh4 = -0.01

                export_dict[cols[29]].append(n_nh4)

                #Total Nitrogen
                tn = -0.01
                found = False
                for i in range(20, 0, -1):
                    if found==False:
                        version = 'sap_total_nitrogen-'+str(i)
                        if hasattr(self,version):
                            found = True
                            tn = float(self[version].Result)
                if found == False and self.sap_total_nitrogen is not None:
                    tn = float(self.sap_total_nitrogen.Result)

                if tn <= 0.01:
                    tn = -0.01

                export_dict[cols[30]].append(tn)

                #Total Sugars
                ts = -0.01
                found = False
                for i in range(20, 0, -1):
                    if found==False:
                        version = 'sap_total_sugar-'+str(i)
                        if hasattr(self,version):
                            found = True
                            ts = float(self[version].Result)
                if found == False and self.sap_total_sugar is not None:
                    ts = float(self.sap_total_sugar.Result)

                if ts <= 0.01:
                    ts = -0.01

                export_dict[cols[31]].append(ts)

                #nitrate
                # manganese = -0.01
                # found = False
                # for i in range(20, 0, -1):
                #     if found==False:
                #         version = 'sap_manganese-'+str(i)
                #         if hasattr(self,version):
                #             found = True
                #             manganese = float(self[version].Result)
                # if found == False and self.sap_manganese is not None:
                #     manganese = float(self.sap_manganese.Result)
                #
                # if manganese <= 0.01:
                #     manganese = -0.01

                export_dict[cols[32]].append('')

                #nitrogen as nitrate
                n_no3 = -0.01
                found = False
                for i in range(20, 0, -1):
                    if found==False:
                        version = 'sap_nitrogen_as_nitrate-'+str(i)
                        if hasattr(self,version):
                            found = True
                            n_no3 = float(self[version].Result)
                if found == False and self.sap_nitrogen_as_nitrate is not None:
                    n_no3 = float(self.sap_nitrogen_as_nitrate.Result)

                if n_no3 <= 0.01:
                    n_no3 = -0.01

                export_dict[cols[33]].append(n_no3)

                #k/ca ratio
                kca = -0.01
                found = False
                for i in range(20, 0, -1):
                    if found==False:
                        version = 'sap_kcaratio-'+str(i)
                        if hasattr(self,version):
                            found = True
                            kca = float(self[version].Result)
                if found == False and self.sap_kcaratio is not None:
                    kca = float(self.sap_kcaratio.Result)

                if kca <= 0.01:
                    kca = -0.01

                export_dict[cols[34]].append(kca)

                #Nitrogen conversion efficiency
                nce = ''
                if tn < 0.01:
                    nce = ''
                else:
                    if n_nh4 < 0.01:
                        n_nh4 = 0
                    if n_no3 < 0.01:
                        n_no3 = 0

                    nce = (1 - ((n_nh4 + n_no3) / tn))*100

                export_dict[cols[35]].append(nce)

        df = pd.DataFrame()
        for i in range(len(cols)):
            df[cols[i]] = export_dict[cols[i]]
        df.to_csv(fullpath)
        IStatusMessage(self.request).addStatusMessage(
                u"{} Successfully Exported to: {}".format(self.context.title, filepath)
            )
        self.request.response.redirect(api.get_url(self.context))
