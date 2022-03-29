import collections

from bika.lims import api
from bika.lims import bikaMessageFactory as _
from Products.Five.browser import BrowserView
from Products.statusmessages.interfaces import IStatusMessage
import pandas as pd
from math import floor
from math import log10

class ClientCSVExportView(BrowserView):

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):

        rootpath = '/mnt'
        path = '/Data/LIMS CSV Exports/'
        client = self.context
        filepath = path + client.getName() + '.csv'
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
            'sampler_contact',
            'grower_contact',
            'client_sample_id',
            'nal_sample_id',
            'date_sampled',
            'time_sampled',
            'sample_type',
            'sample_location'
        ]
        sdgs_full = map(api.get_object,api.search({'portal_type':'Batch'}))
        sdgs_active = []
        sdgs = []
        for i in sdgs_full:
            if api.get_workflow_status_of(i) != 'cancelled':
                sdgs_active.append(i)

        for i in sdgs_active:
            if i.getClient().id == client.id:
                sdgs.append(i)

        print(sdgs)

        ARs = []
        for i in sdgs:
            ARs = ARs + map(api.get_object,i.getAnalysisRequests())

        for i in ARs:
            if api.get_workflow_status_of(i) in ['cancelled','invalid']:
                ARs.remove(i)

            if i.getSampleType().title == 'Sap' and 'plant_type' not in cols and api.get_workflow_status_of(i) not in ['cancelled','invalid']:
                sap_cols = [
                    'plant_type',
                    'variety',
                    'growth_stage',
                    'vigor',
                    'new_old',
                    'nitrogen_conversion_efficiency'
                ]
                cols = cols + sap_cols

    	    ar_cols = []
            for j in map(api.get_object,i.getAnalyses()):
                if j.Keyword not in cols and j.Keyword not in ar_cols:
                    ar_cols.append(str(j.Keyword))
    	    ar_cols.sort()

    	    cols = cols + ar_cols

        #initialize dictionary of lists
        for i in range(len(cols)):
            export_dict[cols[i]] = []

        sample_count = 0
        for i in ARs:
            if api.get_workflow_status_of(i) not in ['cancelled','invalid']:

                print("Exporting Sample: "+str(sample_count)+"-"+str(i.id))

                sdg = api.get_object(i.getBatch())

                sample_count = sample_count+1

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
                    grower_contact = grower_contact[0]
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
                    if i.getSampleType().title == 'Sap' and i.getSubGroup() is not None:
                        if i.NewLeaf is True:
                            new_old = 'New'
                        elif i.NewLeaf is False:
                            new_old = 'Old'
                    export_dict['new_old'].append(new_old)

                for j in map(api.get_object,i.getAnalyses()):
                    if api.get_workflow_status_of(j) not in ['cancelled','invalid','retracted','rejected']:
                        sigfigs = 3
                        result = j.Result
                        if result.replace('.','',1).replace('-','',1).isdigit() is False:
                            export_dict[j.Keyword].append(result)
                        else:
                            result = float(result)
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

                if i.getSampleType().title == 'Sap':
                    nh4 = export_dict['sap_nitrogen_as_ammonium'][-1]
                    no3 = export_dict['sap_nitrogen_as_nitrate'][-1]
                    tn = export_dict['sap_total_nitrogen'][-1]
                    nce = 0

                    if nh4 is None or nh4 == '< 0.01' or nh4 == '':
                        nh4 = 0
                    if no3 is None or no3 == '< 0.01' or no3 == '':
                        no3 = 0
                    if tn is None or tn == '< 0.01' or tn == '':
                        tn = 0
                    else:
                        tn = float(tn)

                    if tn > 0:
                        nce = (1 - ((float(nh4) + float(no3)) / float(tn)))*100
                        nce = round(nce, sigfigs-int(floor(log10(abs(nce))))-1)
                        export_dict['nitrogen_conversion_efficiency'].append(nce)
                    else:
                        export_dict['nitrogen_conversion_efficiency'].append('')
                    print('NCE List is: {0}'.format(export_dict['nitrogen_conversion_efficiency']))

                for j in cols:
                    if len(export_dict[j]) < sample_count:
                        export_dict[j].append('')
                        print('Added a blank to {0}'.format(j))

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
