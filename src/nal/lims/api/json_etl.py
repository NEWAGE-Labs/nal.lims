import json
from bika.lims import api
from plone import api as papi
from math import floor
from math import log10
import pandas as pd
from management import *
from retract import *
from DateTime import DateTime
import jwt
import requests
from nal.lims.secrets import aea_webhook_url, aea_webhook_key
import datetime

bad_status = ['invalid','cancelled','rejected','retracted']

def aea_webhook(batch, url=None):

    try:
        jobj = get_json_for_batch(batch)
        if url is None:
            url = aea_webhook_url
        key = aea_webhook_key
        req = send_with_jwt(url,key,jobj)
        batch.Sent = True
    except Exception as e:
        raise(e)

    return req

def send_with_jwt(url,key,jobj):

    jwt_head = {}
    jwt_head['exp'] = datetime.datetime.now() + datetime.timedelta(seconds=60)
    jwt_head['issuer'] = 'newage'
    token = jwt.encode(jwt_head,key,algorithm='HS256')
    headers = {'Authorization':'{}'.format(token),'Content-Type':'application/json', 'Connection':'close'}
    req = requests.post(url,headers=headers,json=jobj)

    return req

def get_json_for_client(client):
    return

def get_json_for_batch(batch):
    jobj = {}

    if batch is None:
        print('No batch sent')
        return jobj

    if not hasattr(batch,'getClient') or not hasattr(batch,'getAnalysisRequests'):
        print('Not a batch')
        return jobj

    client = batch.getClient()
    ARs = batch.getAnalysisRequests()

    if client is None or len(ARs) == 0:
        print('Batch has no client or no ARs')
        return jobj

    #Client Name and NAL Number
    jobj['nal_number'] = client.ClientID
    jobj['client_name'] = client.Name

    #Client Address
    address = client.PhysicalAddress
    address_str = ''+address['address']+', '+address['city']+', '+address['state']+' '+address['zip']
    jobj['client_address'] = address_str

    #List of SDGs
    jobj['sample_delivery_groups'] = []

    #NO LOOP FOR SINGLE BATCH
    bobj = {}

    #SDG ID
    bobj['title'] = batch.title

    #Project Contact
    project_brain = batch.getReferences(relationship="SDGProjectContact")
    if len(project_brain) > 0:
        project_contact = project_brain[0]
        project_contact_name = project_contact.Firstname + " " + project_contact.Surname
        project_contact_email = project_contact.EmailAddress
    elif hasattr(batch,'ProjectContact') and batch.ProjectContact is not None and batch.ProjectContact != '':
        project_contact = api.get_object_by_uid(batch.ProjectContact)
        project_contact_name = project_contact.Firstname + " " + project_contact.Surname
        project_contact_email = project_contact.EmailAddress
    else:
        project_contact_name = ''
    bobj['project_contact'] = project_contact_name
    bobj['project_email'] = project_contact_email

    #Sampler Contact
    sampler_brain = batch.getReferences(relationship="SDGSamplerContact")
    if len(sampler_brain) > 0:
        sampler_contact = sampler_brain[0]
        sampler_contact_name = sampler_contact.Firstname + " " + sampler_contact.Surname
    elif hasattr(batch,'SamplerContact') and batch.SamplerContact is not None and batch.SamplerContact != '':
        sampler_contact = api.get_object_by_uid(batch.SamplerContact)
        sampler_contact_name = sampler_contact.Firstname + " " + sampler_contact.Surname
    else:
        sampler_contact_name = ''
    bobj['sampler_contact'] = sampler_contact_name

    #Grower Contact
    grower_brain = batch.getReferences(relationship="SDGGrowerContact")
    if len(grower_brain) > 0:
        grower_contact = grower_brain[0]
        grower_contact_name = grower_contact.Firstname + " " + grower_contact.Surname
    elif hasattr(batch,'GrowerContact') and batch.GrowerContact is not None and batch.GrowerContact != '':
        grower_contact = api.get_object_by_uid(batch.GrowerContact)
        grower_contact_name = grower_contact.Firstname + " " + grower_contact.Surname
    else:
        grower_contact_name = ''
    bobj['grower_contact'] = grower_contact_name

    #Date and Time Received
    dreceived = batch.SDGDate.strftime('%m-%d-%Y')
    bobj['date_recieved'] = dreceived
    bobj['time_received'] = batch.SDGTime
    bobj['samples'] = []

    clean_ars = [ar for ar in ARs if api.get_workflow_status_of(ar) not in bad_status]

    for ar in clean_ars:
        analyses = map(api.get_object,ar.getAnalyses())
        clean_analyses = [analysis for analysis in analyses if api.get_workflow_status_of(analysis) not in bad_status]
        if len(clean_analyses) == 0:
            continue

        sobj = {}

        #Client Sample ID
        sobj['client_sample_id'] = ar.getClientSampleID()

        #Internal Lab ID
        sobj['internal_lab_id'] = ar.InternalLabID

        #Pair
        pair = ''
        if hasattr(ar,'SubGroup') and ar.getSubGroup() is not None:
            pair = ar.getSubGroup().title
        sobj['pair'] = pair

        #NAL Sample ID
        sobj['nal_client_id'] = ar.id

        #Date Sampled
        sobj['date_sampled'] = ar.DateOfSampling.strftime('%m-%d-%Y')

        #Time Sampled
        sobj['time_sampled'] = ar.TimeOfSampling

        #Sample Type
        sobj['sample_type'] = ar.getSampleType().title

        #Sample Location
        sobj['sample_location'] = '' if ar.getSamplePoint() is None else ar.getSamplePoint().title

        #Plant Type
        sobj['plant_type'] = ar.PlantType

        #Variety
        sobj['variety'] = ar.Variety

        #Growth Stage
        sobj['growth_stage'] = ar.GrowthStage

        #Vigor
        sobj['vigor'] = ar.Vigor

        #New/Old
        new_old = ''
        if ar.getSampleType().title == 'Sap' and ar.getSubGroup() is not None:
            if ar.NewLeaf:
                new_old = 'new'
            if not ar.NewLeaf:
                new_old = 'old'
        sobj['new_old'] = new_old

        #Analyses
        sobj['analyses'] = []

        #GET NCE IF IT SHOULD BE THERE
        if ar.getSampleType().title == 'Sap' and hasattr(ar,'nitrogen_nitrate') and hasattr(ar,'nitrogen_ammonium') and hasattr(ar,'nitrogen'):

            nh4 = None
            no3 = None
            tn = None
            nce = 0

            for analysis in clean_analyses:
                if analysis.Keyword == 'nitrogen_ammonium' and api.get_workflow_status_of(analysis) not in bad_status:
                    nh4 = float(analysis.Result)
                elif analysis.Keyword == 'nitrogen_nitrate' and api.get_workflow_status_of(analysis) not in bad_status:
                    no3 = float(analysis.Result)
                elif analysis.Keyword == 'nitrogen' and api.get_workflow_status_of(analysis) not in bad_status:
                    tn = float(analysis.Result)

            if nh4 is None or nh4 < 0.01:
                nh4 = 0
            if no3 is None or no3 < 0.01:
                no3 = 0
            if tn is None or  tn < 0.01:
                tn = 0

            if tn > 0:
                nce = (1 - ((float(nh4) + float(no3)) / float(tn)))*100
                nce = round(nce, 3-int(floor(log10(abs(nce))))-1)
            else:
                nce = ''
            aobj = {}
            aobj['keyword'] = 'nitrogen_conversion_efficiency'
            aobj['unit'] = '%'
            aobj['result'] = nce
            sobj['analyses'].append(aobj)

        #Loop through all tests (other than NCE)
        for analysis in clean_analyses:

            aobj = {}

            #Keyword
            aobj['keyword'] = analysis.Keyword

            #Unit
            aobj['unit'] = analysis.Unit

            #Result
            result = analysis.Result
            dil = (1 if (analysis.Dilution is None or analysis.Dilution == '') else analysis.Dilution)

            if result.replace('.','',1).replace('-','',1).isdigit() is False:
                pass
            else:
                result = float(result)

                loq = 0.01
                for method in analysis.getAnalysisService().MethodRecords:
                    if hasattr(analysis,'CustomMethod') and method['methodid'] == analysis.CustomMethod:
                        loq = method['loq']
                choices = None
                if loq == 'P|A':
                    choices = analysis.getResultOptions()
                if choices:
                    # Create a dict for easy mapping of result options
                    values_texts = dict(map(lambda c: (str(c["ResultValue"]), c['ResultText']), choices))
                    # Result might contain a single result option
                    match = values_texts.get(str(int(result)))
                    if match:
                        result = match
                    else:
                        result = '-'

                elif result < float(loq):
                    result = '< {}'.format(float(loq) * float(dil))
                else:
                    result = round((result*float(dil)), 3-int(floor(log10(abs(result*float(dil)))))-1)

            aobj['result'] = result
            sobj['analyses'].append(aobj)

        bobj['samples'].append(sobj)

    jobj['sample_delivery_groups'].append(bobj)

    return jobj
