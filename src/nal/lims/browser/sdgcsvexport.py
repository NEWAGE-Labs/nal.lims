import collections

from bika.lims import api
from bika.lims import bikaMessageFactory as _
from Products.Five.browser import BrowserView
from Products.statusmessages.interfaces import IStatusMessage
import pandas as pd
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
        #Get a Column list based on:
        # 1) Client Fields
        # 2) SDG Fields
        # 3) Relevant Sample fields (Crop details)
        # 4) The unique list of analyses on all samples of the SDG
        cols = [
            'nal_number',
            'client_name',
            'client_address',
            'sample_delivery_group',
            'date_received',
            'time_received',
            'project_contact',
            'sampler_contact'
            ]
        if hasattr(sdg,'GrowerContact'):
            cols.append('grower_contact')

        xtra_cols = [
            'client_sample_id',
            'nal_sample_id',
            'date_sampled',
            'time_sampled',
            'sample_type',
            'sample_location'
        ]
        cols = cols + xtra_cols
        ARs = self.context.getAnalysisRequests()
        for i in ARs:
            if i.getSampleType().title == 'Sap' and 'plant_type' not in cols and api.get_workflow_status_of(i) not in ['cancelled','invalid']:
                sap_cols = [
                    'plant_type',
                    'variety',
                    'growth_stage',
                    'vigor',
                    'new_old',
                    'nitrogen_conversion_effeciency'
                ]
                cols = cols + sap_cols

            for j in map(api.get_object,i.getAnalyses()):
                if j.Keyword not in cols:
                    cols.append(str(j.Keyword))

        #initialize dictionary of lists
        for i in range(len(cols)):
            export_dict[cols[i]] = []

        sample_count = 0
        for i in ARs:
            if api.get_workflow_status_of(i) not in ['cancelled','invalid']:

                sample_count = sample_count+1

                client = sdg.getClient()

                #NAL Number
                export_dict['nal_number'].append(client.getClientID())

                #Client Name
                export_dict['client_name'].append(client.getName())

                #Client Address
                addressdict = client.getPhysicalAddress()
                exportaddress = ''
                if addressdict['address'] != '':
                    exportaddress = exportaddress + addressdict['address']
                if addressdict['city'] != '':
                    exportaddress = exportaddress + ', ' + addressdict['city']
                if addressdict['state'] != '':
                    exportaddress = exportaddress + ', ' + addressdict['state']
                if addressdict['zip'] != '':
                    exportaddress = exportaddress + ' ' + addressdict['zip']
                export_dict['client_address'].append(exportaddress)

                #SDG
                export_dict['sample_delivery_group'].append(sdg.title)

                #Date Received
                dreceived = sdg.SDGDate.strftime('%m-%d-%Y')
                export_dict['date_received'].append(dreceived)

                #Time Received
                export_dict['time_received'].append(sdg.SDGTime)

                #Project Contact
                project_contact = sdg.getReferences(relationship="SDGProjectContact")[0]
                project_contact_name = project_contact.Firstname + " " + project_contact.Surname
                export_dict['project_contact'].append(project_contact_name)

                #Sampler Contact
                sampler_contact = sdg.getReferences(relationship="SDGSamplerContact")[0]
                sampler_contact_name = sampler_contact.Firstname + " " + sampler_contact.Surname
                export_dict['sampler_contact'].append(sampler_contact_name)

                #Grower Contact
                grower_contact = sdg.getReferences(relationship="SDGGrowerContact")
                if len(grower_contact) > 0 and 'grower_contact' in cols:
                    grower_contact_name = grower_contact.Firstname + " " + grower_contact.Surname
                    export_dict['grower_contact'].append(grower_contact_name)

                #Client Sample ID
                export_dict['client_sample_id'].append(i.getClientSampleID())

                #NAL Sample ID
                export_dict['nal_sample_id'].append(i.id)

                #Date Sampled
                export_dict['date_sampled'].append(i.DateOfSampling.strftime('%m-%d-%Y'))

                #Time Sampled
                export_dict['time_sampled'].append(i.TimeOfSampling)

                #Sample Type
                export_dict['sample_type'].append(i.getSampleType().title)

                #Sample Location
                if i.getSamplePoint() is not None:
                    export_dict['sample_location'].append(i.getSamplePoint().title)
                else:
                    export_dict['sample_location'].append('')

                if 'plant_type' in cols:
                    #Plant Type
                    export_dict['plant_type'].append(i.PlantType)

                    #Variety
                    export_dict['variety'].append(i.Variety)

                    #Growth Stage
                    export_dict['growth_stage'].append(i.GrowthStage)

                    #Vigor
                    if hasattr(i,'Vigor'):
                        export_dict['vigor'].append(i.Vigor)

                    #New/Old
                    new_old = ''
                    ## If Sample has a Pair, Then assign a 'New' or 'Old'
                    if i.getSampleType().title == 'Sap' and hasattr(i,'SubGroup'):
                        if i.NewLeaf == True:
                            new_old = 'New'
                        elif i.NewLeaf == False:
                            new_old = 'Old'
                    export_dict['new_old'].append(new_old)

                for j in map(api.get_object,i.getAnalyses()):
                    if api.get_workflow_status_of(j) not in ['cancelled','invalid','retracted','rejected']:
                        sigfigs = 3
                        result = float(j.Result)
                        if i.getSampleType().title == 'Sap':
                            if result < 0.01:
                                result = '< 0.01'
                            else:
                                result = round(result, sigfigs-int(floor(log10(abs(result))))-1)
                            export_dict[j.Keyword].append(result)
                        else:
                            if result < float(j.getLowerDetectionLimit()):
                                result = '< ' + str(j.getLowerDetectionLimit())
                            else:
                                result = round(result, sigfigs-int(floor(log10(abs(result))))-1)
                            export_dict[j.Keyword].append(result)

                # #Nitrogen conversion efficiency
                # nce = ''
                # if tn < 0.01 or n_nh4 == '':
                #     nce = ''
                # else:
                #     if n_nh4 < 0.01:
                #         n_nh4 = 0
                #     if n_no3 < 0.01:
                #         n_no3 = 0
                #
                #     nce = (1 - ((n_nh4 + n_no3) / tn))*100
                #
                #     nce = round(nce, 3-int(floor(log10(abs(nce))))-1)
                #
                # export_dict[cols[36]].append(nce)
                if i.getSampleType().title == 'Sap':
                    nh4 = export_dict['sap_nitrogen_as_ammonium'][-1]
                    no3 = export_dict['sap_nitrogen_as_nitrate'][-1]
                    tn = float(export_dict['sap_total_nitrogen'][-1])
                    nce = 0

                    if nh4 == '< 0.01':
                        nh4 = 0
                    if no3 == '< 0.01':
                        no3 = 0

                    nce = (1 - ((float(nh4) + float(no3)) / float(tn)))*100
                    nce = round(nce, sigfigs-int(floor(log10(abs(nce))))-1)
                    export_dict['nitrogen_conversion_effeciency'].append(nce)

                for j in cols:
                    if len(export_dict[j]) < sample_count:
                        export_dict[j].append('')

                #EC
                # ec = -0.01
                # found = False
                # for j in range(20, 0, -1):
                #     if found==False:
                #         version = 'sap_ec-'+str(j)
                #         if hasattr(i,version) and api.get_workflow_status_of(i[version]) not in ['retracted','rejected','cancelled','invalid']:
                #             found = True
                #             if i[version].Result is None:
                #                 ec = ''
                #             else:
                #                 ec = float(i[version].Result)
                # if found == False and hasattr(i,'sap_ec'):
                #     if i.sap_ec.Result is None or i.sap_ec.Result == '':
                #         ec = ''
                #     else:
                #         ec = float(i.sap_ec.Result)
                # if ec != '':
                #     if ec <= 0.01:
                #         ec = -0.01
                #     else:
                #         ec = round(ec, 3-int(floor(log10(abs(ec))))-1)
                #
                # export_dict[cols[11]].append(ec)
                #
                # #Phosphorus
                # phosphorus = -0.01
                # found = False
                # for j in range(20, 0, -1):
                #     if found==False:
                #         version = 'sap_phosphorous-'+str(j)
                #         if hasattr(i,version) and api.get_workflow_status_of(i[version]) not in ['retracted','rejected','cancelled','invalid']:
                #             found = True
                #             phosphorus = float(i[version].Result)
                # if found == False and hasattr(i,'sap_phosphorous'):
                #     phosphorus = float(i.sap_phosphorous.Result)
                #
                # if phosphorus <= 0.01:
                #     phosphorus = -0.01
                # else:
                #     phosphorus = round(phosphorus, 3-int(floor(log10(abs(phosphorus))))-1)
                #
                # export_dict[cols[12]].append(phosphorus)
                #
                # #Potassium
                # potassium = -0.01
                # found = False
                # for j in range(20, 0, -1):
                #     if found==False:
                #         version = 'sap_potassium-'+str(j)
                #         if hasattr(i,version) and api.get_workflow_status_of(i[version]) not in ['retracted','rejected','cancelled','invalid']:
                #             found = True
                #             potassium = float(i[version].Result)
                # if found == False and hasattr(i,'sap_potassium'):
                #     potassium = float(i.sap_potassium.Result)
                #
                # if potassium <= 0.01:
                #     potassium = -0.01
                # else:
                #     potassium = round(potassium, 3-int(floor(log10(abs(potassium))))-1)
                #
                # export_dict[cols[13]].append(potassium)
                #
                # #calcium
                # calcium = -0.01
                # found = False
                # for j in range(20, 0, -1):
                #     if found==False:
                #         version = 'sap_calcium-'+str(j)
                #         if hasattr(i,version) and api.get_workflow_status_of(i[version]) not in ['retracted','rejected','cancelled','invalid']:
                #             found = True
                #             calcium = float(i[version].Result)
                # if found == False and hasattr(i,'sap_calcium'):
                #     calcium = float(i.sap_calcium.Result)
                #
                # if calcium <= 0.01:
                #     calcium = -0.01
                # else:
                #     calcium = round(calcium, 3-int(floor(log10(abs(calcium))))-1)
                #
                # export_dict[cols[14]].append(calcium)
                #
                # #manganese
                # manganese = -0.01
                # found = False
                # for j in range(20, 0, -1):
                #     if found==False:
                #         version = 'sap_manganese-'+str(j)
                #         if hasattr(i,version) and api.get_workflow_status_of(i[version]) not in ['retracted','rejected','cancelled','invalid']:
                #             found = True
                #             manganese = float(i[version].Result)
                # if found == False and hasattr(i,'sap_manganese'):
                #     manganese = float(i.sap_manganese.Result)
                #
                # if manganese <= 0.01:
                #     manganese = -0.01
                # else:
                #     manganese = round(manganese, 3-int(floor(log10(abs(manganese))))-1)
                #
                # export_dict[cols[15]].append(manganese)
                #
                # #zinc
                # zinc = -0.01
                # found = False
                # for j in range(20, 0, -1):
                #     if found==False:
                #         version = 'sap_zinc-'+str(j)
                #         if hasattr(i,version) and api.get_workflow_status_of(i[version]) not in ['retracted','rejected','cancelled','invalid']:
                #             found = True
                #             zinc = float(i[version].Result)
                # if found == False and hasattr(i,'sap_zinc'):
                #     zinc = float(i.sap_zinc.Result)
                #
                # if zinc <= 0.01:
                #     zinc = -0.01
                # else:
                #     zinc = round(zinc, 3-int(floor(log10(abs(zinc))))-1)
                #
                # export_dict[cols[16]].append(zinc)
                #
                # #sulfur
                # sulfur = -0.01
                # found = False
                # for j in range(20, 0, -1):
                #     if found==False:
                #         version = 'sap_sulfur-'+str(j)
                #         if hasattr(i,version) and api.get_workflow_status_of(i[version]) not in ['retracted','rejected','cancelled','invalid']:
                #             found = True
                #             sulfur = float(i[version].Result)
                # if found == False and hasattr(i,'sap_sulfur'):
                #     sulfur = float(i.sap_sulfur.Result)
                #
                # if sulfur <= 0.01:
                #     sulfur = -0.01
                # else:
                #     sulfur = round(sulfur, 3-int(floor(log10(abs(sulfur))))-1)
                #
                # export_dict[cols[17]].append(sulfur)
                #
                # #copper
                # copper = -0.01
                # found = False
                # for j in range(20, 0, -1):
                #     if found==False:
                #         version = 'sap_copper-'+str(j)
                #         if hasattr(i,version) and api.get_workflow_status_of(i[version]) not in ['retracted','rejected','cancelled','invalid']:
                #             found = True
                #             copper = float(i[version].Result)
                # if found == False and hasattr(i,'sap_copper'):
                #     copper = float(i.sap_copper.Result)
                #
                # if copper <= 0.01:
                #     copper = -0.01
                # else:
                #     copper = round(copper, 3-int(floor(log10(abs(copper))))-1)
                #
                # export_dict[cols[18]].append(copper)
                #
                # #magnesium
                # magnesium = -0.01
                # found = False
                # for j in range(20, 0, -1):
                #     if found==False:
                #         version = 'sap_magnesium-'+str(j)
                #         if hasattr(i,version) and api.get_workflow_status_of(i[version]) not in ['retracted','rejected','cancelled','invalid']:
                #             found = True
                #             magnesium = float(i[version].Result)
                # if found == False and hasattr(i,'sap_magnesium'):
                #     magnesium = float(i.sap_magnesium.Result)
                #
                # if magnesium <= 0.01:
                #     magnesium = -0.01
                # else:
                #     magnesium = round(magnesium, 3-int(floor(log10(abs(magnesium))))-1)
                #
                # export_dict[cols[19]].append(magnesium)
                #
                # #iron
                # iron = -0.01
                # found = False
                # for j in range(20, 0, -1):
                #     if found==False:
                #         version = 'sap_iron-'+str(j)
                #         if hasattr(i,version) and api.get_workflow_status_of(i[version]) not in ['retracted','rejected','cancelled','invalid']:
                #             found = True
                #             iron = float(i[version].Result)
                # if found == False and hasattr(i,'sap_iron'):
                #     iron = float(i.sap_iron.Result)
                #
                # if iron <= 0.01:
                #     iron = -0.01
                # else:
                #     iron = round(iron, 3-int(floor(log10(abs(iron))))-1)
                #
                # export_dict[cols[20]].append(iron)
                #
                # #boron
                # boron = -0.01
                # found = False
                # for j in range(20, 0, -1):
                #     if found==False:
                #         version = 'sap_boron-'+str(j)
                #         if hasattr(i,version) and api.get_workflow_status_of(i[version]) not in ['retracted','rejected','cancelled','invalid']:
                #             found = True
                #             boron = float(i[version].Result)
                # if found == False and hasattr(i,'sap_boron'):
                #     boron = float(i.sap_boron.Result)
                #
                # if boron <= 0.01:
                #     boron = -0.01
                # else:
                #     boron = round(boron, 3-int(floor(log10(abs(boron))))-1)
                #
                # export_dict[cols[21]].append(boron)
                #
                # #brix
                # brix = -0.01
                # found = False
                # for j in range(20, 0, -1):
                #     if found==False:
                #         version = 'sap_brix-'+str(j)
                #         if hasattr(i,version) and api.get_workflow_status_of(i[version]) not in ['retracted','rejected','cancelled','invalid']:
                #             found = True
                #             brix = float(i[version].Result)
                # if found == False and hasattr(i,'sap_brix'):
                #     brix = float(i.sap_brix.Result)
                #
                # if brix <= 0.01:
                #     brix = -0.01
                # else:
                #     brix = round(brix, 3-int(floor(log10(abs(brix))))-1)
                #
                # export_dict[cols[22]].append(brix)
                #
                # #ph
                # ph = -0.01
                # found = False
                # for j in range(20, 0, -1):
                #     if found==False:
                #         version = 'sap_ph-'+str(j)
                #         if hasattr(i,version) and api.get_workflow_status_of(i[version]) not in ['retracted','rejected','cancelled','invalid']:
                #             found = True
                #             if i[version].Result is None:
                #                 ph = ''
                #             else:
                #                 ph = float(i[version].Result)
                # if found == False and hasattr(i,'sap_ph'):
                #     if i.sap_ph.Result is None or i.sap_ph.Result == '':
                #         ph = ''
                #     else:
                #         ph = float(i.sap_ph.Result)
                #
                # if ph != '':
                #     if ph <= 0.01:
                #         ph = -0.01
                #     else:
                #         ph = round(ph, 3-int(floor(log10(abs(ph))))-1)
                #
                # export_dict[cols[23]].append(ph)
                #
                # #chloride
                # chloride = -0.01
                # found = False
                # for j in range(20, 0, -1):
                #     if found==False:
                #         version = 'sap_chloride-'+str(j)
                #         if hasattr(i,version) and api.get_workflow_status_of(i[version]) not in ['retracted','rejected','cancelled','invalid']:
                #             found = True
                #             manganese = float(i[version].Result)
                # if found == False and hasattr(i,'sap_chloride'):
                #     chloride = float(i.sap_chloride.Result)
                #
                # if chloride <= 0.01:
                #     chloride = -0.01
                # else:
                #     chloride = round(chloride, 3-int(floor(log10(abs(chloride))))-1)
                #
                # export_dict[cols[24]].append(chloride)
                #
                # #sodium
                # sodium = -0.01
                # found = False
                # for j in range(20, 0, -1):
                #     if found==False:
                #         version = 'sap_sodium-'+str(j)
                #         if hasattr(i,version) and api.get_workflow_status_of(i[version]) not in ['retracted','rejected','cancelled','invalid']:
                #             found = True
                #             sodium = float(i[version].Result)
                # if found == False and hasattr(i,'sap_sodium'):
                #     sodium = float(i.sap_sodium.Result)
                #
                # if sodium <= 0.01:
                #     sodium = -0.01
                # else:
                #     sodium = round(sodium, 3-int(floor(log10(abs(sodium))))-1)
                #
                # export_dict[cols[25]].append(sodium)
                #
                # #silicon
                # silica = -0.01
                # found = False
                # for j in range(20, 0, -1):
                #     if found==False:
                #         version = 'sap_silica-'+str(j)
                #         if hasattr(i,version) and api.get_workflow_status_of(i[version]) not in ['retracted','rejected','cancelled','invalid']:
                #             found = True
                #             silica = float(i[version].Result)
                # if found == False and hasattr(i,'sap_silica'):
                #     silica = float(i.sap_silica.Result)
                #
                # if silica <= 0.01:
                #     silica = -0.01
                # else:
                #     silica = round(silica, 3-int(floor(log10(abs(silica))))-1)
                #
                # export_dict[cols[26]].append(silica)
                #
                # #aluminium
                # aluminium = -0.01
                # found = False
                # for j in range(20, 0, -1):
                #     if found==False:
                #         version = 'sap_aluminum-'+str(j)
                #         if hasattr(i,version) and api.get_workflow_status_of(i[version]) not in ['retracted','rejected','cancelled','invalid']:
                #             found = True
                #             aluminium = float(i[version].Result)
                # if found == False and hasattr(i,'sap_aluminum'):
                #     aluminium = float(i.sap_aluminum.Result)
                #
                # if aluminium <= 0.01:
                #     aluminium = -0.01
                # else:
                #     aluminium = round(aluminium, 3-int(floor(log10(abs(aluminium))))-1)
                #
                # export_dict[cols[27]].append(aluminium)
                #
                # #cobalt
                # cobalt = -0.01
                # found = False
                # for j in range(20, 0, -1):
                #     if found==False:
                #         version = 'sap_cobalt-'+str(j)
                #         if hasattr(i,version) and api.get_workflow_status_of(i[version]) not in ['retracted','rejected','cancelled','invalid']:
                #             found = True
                #             cobalt = float(i[version].Result)
                # if found == False and hasattr(i,'sap_cobalt'):
                #     cobalt = float(i.sap_cobalt.Result)
                #
                # if cobalt <= 0.01:
                #     cobalt = -0.01
                # else:
                #     cobalt = round(cobalt, 3-int(floor(log10(abs(cobalt))))-1)
                #
                # export_dict[cols[28]].append(cobalt)
                #
                # #molybdenum
                # molybdenum = -0.01
                # found = False
                # for j in range(20, 0, -1):
                #     if found==False:
                #         version = 'sap_molybdenum-'+str(j)
                #         if hasattr(i,version) and api.get_workflow_status_of(i[version]) not in ['retracted','rejected','cancelled','invalid']:
                #             found = True
                #             molybdenum = float(i[version].Result)
                # if found == False and hasattr(i,'sap_molybdenum'):
                #     molybdenum = float(i.sap_molybdenum.Result)
                #
                # if molybdenum <= 0.01:
                #     molybdenum = -0.01
                # else:
                #     molybdenum = round(molybdenum, 3-int(floor(log10(abs(molybdenum))))-1)
                #
                # export_dict[cols[29]].append(molybdenum)
                #
                # #Nitrogen from Ammonium
                # n_nh4 = -0.01
                # found = False
                # for j in range(20, 0, -1):
                #     if found==False:
                #         version = 'sap_nitrogen_as_ammonium-'+str(j)
                #         if hasattr(i,version) and api.get_workflow_status_of(i[version]) not in ['retracted','rejected','cancelled','invalid']:
                #             found = True
                #             n_nh4 = float(i[version].Result)
                # if found == False and hasattr(i,'sap_nitrogen_as_ammonium'):
                #     if i.sap_nitrogen_as_ammonium.Result is None or i.sap_nitrogen_as_ammonium.Result == '':
                #         n_nh4 = ''
                #     else:
                #         n_nh4 = float(i.sap_nitrogen_as_ammonium.Result)
                #
                # if n_nh4 <= 0.01:
                #     n_nh4 = -0.01
                # elif n_nh4 != '':
                #     n_nh4 = round(n_nh4, 3-int(floor(log10(abs(n_nh4))))-1)
                #
                # export_dict[cols[30]].append(n_nh4)
                #
                # #Total Nitrogen
                # tn = -0.01
                # found = False
                # for j in range(20, 0, -1):
                #     if found==False:
                #         version = 'sap_total_nitrogen-'+str(j)
                #         if hasattr(i,version) and api.get_workflow_status_of(i[version]) not in ['retracted','rejected','cancelled','invalid']:
                #             found = True
                #             tn = float(i[version].Result)
                # if found == False and hasattr(i,'sap_total_nitrogen'):
                #     tn = float(i.sap_total_nitrogen.Result)
                #
                # if tn <= 0.01:
                #     tn = -0.01
                # else:
                #     tn = round(tn, 3-int(floor(log10(abs(tn))))-1)
                #
                # export_dict[cols[31]].append(tn)
                #
                # #Total Sugars
                # ts = -0.01
                # found = False
                # for j in range(20, 0, -1):
                #     if found==False:
                #         version = 'sap_total_sugar-'+str(j)
                #         if hasattr(i,version) and api.get_workflow_status_of(i[version]) not in ['retracted','rejected','cancelled','invalid']:
                #             found = True
                #             ts = float(i[version].Result)
                # if found == False and hasattr(i,'sap_total_sugar'):
                #     ts = float(i.sap_total_sugar.Result)
                #
                # if ts <= 0.01:
                #     ts = -0.01
                # else:
                #     ts = round(ts, 3-int(floor(log10(abs(ts))))-1)
                #
                # export_dict[cols[32]].append(ts)
                #
                # #nitrate
                # # manganese = -0.01
                # # found = False
                # # for j in range(20, 0, -1):
                # #     if found==False:
                # #         version = 'sap_manganese-'+str(j)
                # #         if hasattr(i,version) and api.get_workflow_status_of(i[version]) not in ['retracted','rejected','cancelled','invalid']:
                # #             found = True
                # #             manganese = float(i[version].Result)
                # # if found == False and hasattr(i,'sap_manganese'):
                # #     manganese = float(i.sap_manganese.Result)
                # #
                # # if manganese <= 0.01:
                # #     manganese = -0.01
                #
                # export_dict[cols[33]].append('')
                #
                # #nitrogen as nitrate
                # n_no3 = -0.01
                # found = False
                # for j in range(20, 0, -1):
                #     if found==False:
                #         version = 'sap_nitrogen_as_nitrate-'+str(j)
                #         if hasattr(i,version) and api.get_workflow_status_of(i[version]) not in ['retracted','rejected','cancelled','invalid']:
                #             found = True
                #             n_no3 = float(i[version].Result)
                # if found == False and hasattr(i,'sap_nitrogen_as_nitrate'):
                #     n_no3 = float(i.sap_nitrogen_as_nitrate.Result)
                #
                # if n_no3 <= 0.01:
                #     n_no3 = -0.01
                # else:
                #     n_no3 = round(n_no3, 3-int(floor(log10(abs(n_no3))))-1)
                #
                # export_dict[cols[34]].append(n_no3)
                #
                # #k/ca ratio
                # kca = -0.01
                # found = False
                # for j in range(20, 0, -1):
                #     if found==False:
                #         version = 'sap_kcaratio-'+str(j)
                #         if hasattr(i,version) and api.get_workflow_status_of(i[version]) not in ['retracted','rejected','cancelled','invalid']:
                #             found = True
                #             kca = float(i[version].Result)
                # if found == False and hasattr(i,'sap_kcaratio'):
                #     kca = float(i.sap_kcaratio.Result)
                #
                # if kca <= 0.01:
                #     kca = -0.01
                # else:
                #     kca = round(kca, 3-int(floor(log10(abs(kca))))-1)
                #
                # export_dict[cols[35]].append(kca)
                #
                # #Nitrogen conversion efficiency
                # nce = ''
                # if tn < 0.01 or n_nh4 == '':
                #     nce = ''
                # else:
                #     if n_nh4 < 0.01:
                #         n_nh4 = 0
                #     if n_no3 < 0.01:
                #         n_no3 = 0
                #
                #     nce = (1 - ((n_nh4 + n_no3) / tn))*100
                #
                #     nce = round(nce, 3-int(floor(log10(abs(nce))))-1)
                #
                # export_dict[cols[36]].append(nce)


        print(cols)
        print(export_dict)
        for i in export_dict:
            print(len(export_dict[i]))
            print(export_dict[i])
        df = pd.DataFrame()

        for i in cols:
            df[i] = export_dict[i]

        df.to_csv(fullpath)

        IStatusMessage(self.request).addStatusMessage(
                u"{} Successfully Exported to: {}".format(self.context.title, filepath)
            )

        self.request.response.redirect(api.get_url(self.context))
