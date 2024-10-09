from plone.dexterity.browser.view import DefaultView
from bika.lims import api
from z3c.form import button
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.statusmessages.interfaces import IStatusMessage
from plone.autoform.form import AutoExtensibleForm
from zope import interface
from zope import schema
from zope import component
from z3c.form import form
from plone.dexterity.browser import edit
from plone.dexterity.browser import add
import transaction as t
import csv
import StringIO
import codecs
import pandas as pd
import logging
import copy
from DateTime import DateTime

class ICAPImportView(edit.DefaultEditForm):

    def __init__(self, context, request):
          self.context = context
          self.request = request

    def saveCSV(self, context, request):
        return context.absolute_url_path()

    def processCSV(self, data):
        """Process the CSV"""
        #Get logger for output messages
        logger = logging.getLogger("Plone")

        method = map(api.get_object,api.search({'portal_type':'Method','title':'AOAC 993.14'}))[0]
        rs_method = map(api.get_object,api.search({'portal_type':'Method','title':'Calculation'}))[0]
        sar_method = map(api.get_object,api.search({'portal_type':'Method','title':'SAR'}))[0]
        kca_method = map(api.get_object,api.search({'portal_type':'Method','title':'Elemental Ratio'}))[0]
        hardness_method = map(api.get_object,api.search({'portal_type':'Method','title':'SM2340A'}))[0]

        #Convert CSV data to a dataframe
        df = pd.read_csv(StringIO.StringIO(data),keep_default_na=False, dtype=str)
        #Get a list of Unique sample names from the imported DataFrame
        sample_names = df['Sample Name'].unique()
        #Take off the '-001' to get a list of SDG titles to search
        batch_titles = df['Sample Name'].str[:-4].unique().tolist()

        for i in batch_titles:
                print(i)
        #Get a brain of the list of sdgs
        batch_brain = api.search({'portal_type':'Batch','title':batch_titles})
        batch_objs = map(api.get_object,batch_brain)
        batch_dict = {}

        for i in batch_objs:
            if api.get_workflow_status_of(i) == 'open':
                bars = map(api.get_object,i.getAnalysisRequests())
                if bars != []:
                    batch_dict[i.title] = bars

        #Instantiate an empty list to fill with Senaite samples that will be imported into
        import_samples = []

        for i in sample_names:
            xsdg = i[:-4]
            ili = i[-3:]
            print("SDG: {}\nILI: {}".format(xsdg,ili))
            if xsdg in batch_dict.keys():
                ars = batch_dict[xsdg]
                print(ars)
                for j in ars:
                    if (
                        api.get_workflow_status_of(j) not in ['retracted','rejected','invalid','cancelled']
                        and (j.InternalLabID == ili
                        or api.get_id(j) == i)
                    ):
                        import_samples.append(j)
                        df.loc[df['Sample Name'] == i,['Sample Name']] = api.get_id(j)

        #Get the list of Senaite Sample IDs that will be imported into.
        ids = map(api.get_id, import_samples)
        logger.info("IDs: {0}".format(ids))

        #Get a filter dataframe for only the samples that exist
        bool_series = df['Sample Name'].isin(ids)
        filtered_df = df[bool_series]
        clean_ids = []
        for i in import_samples:
            print('IMPORTING - Sample {0} ID: {1}'.format(i,api.get_id(i)))
            imported = []

            found = False
            aluminum = None
            antimony = None
            arsenic = None
            barium = None
            beryllium = None
            boron = None
            calcium = None
            cadmium = None
            cobalt = None
            chromium = None
            copper = None
            iron = None
            lead = None
            magnesium = None
            manganese = None
            molybdenum = None
            nickel = None
            phosphorus = None
            potassium = None
            selenium = None
            silica = None
            silver = None
            sodium = None
            sulfur = None
            thallium = None
            uranium = None
            vanadium = None
            zinc = None
            kca_ratio = None
            hardness = None
            SAR = None
            calcium_percent = None
            potassium_percent = None
            magnesium_percent = None
            sodium_percent = None
            sodium_honee = None
            cec = None
            bec = None
            acidity = None
            weight = None

            for j in i:
                if api.get_workflow_status_of(i[j]) not in ['retracted','rejected','invalid','cancelled']:
                    if 'aluminum' in j and 'perc' not in j:
                        aluminum = i[j]
                    if 'antimony' in j and 'perc' not in j:
                        antimony = i[j]
                    if 'arsenic' in j and 'perc' not in j:
                        arsenic = i[j]
                    if 'barium' in j and 'perc' not in j:
                        barium = i[j]
                    if 'beryllium' in j and 'perc' not in j:
                        beryllium = i[j]
                    if 'boron' in j and 'perc' not in j:
                        boron = i[j]
                    if 'calcium' in j and 'perc' not in j:
                        calcium = i[j]
                    if 'cadmium' in j and 'perc' not in j:
                        cadmium = i[j]
                    if 'cobalt' in j and 'perc' not in j:
                        cobalt = i[j]
                    if 'chromium' in j and 'perc' not in j:
                        chromium = i[j]
                    if 'copper' in j and 'perc' not in j:
                        copper = i[j]
                    if 'iron' in j and 'perc' not in j:
                        iron = i[j]
                    if 'lead' in j and 'perc' not in j:
                        lead = i[j]
                    if 'magnesium' in j and 'perc' not in j:
                        magnesium = i[j]
                    if 'manganese' in j and 'perc' not in j:
                        manganese = i[j]
                    if 'molybdenum' in j and 'perc' not in j:
                        molybdenum = i[j]
                    if 'nickel' in j and 'perc' not in j:
                        nickel = i[j]
                    if ('phosphorus' in j or 'phosphorous' in j):
                        phosphorus = i[j]
                    if 'potassium' in j and 'perc' not in j:
                        potassium = i[j]
                    if 'selenium' in j and 'perc' not in j:
                        selenium = i[j]
                    if 'silica' in j and 'perc' not in j:
                        silica = i[j]
                    if 'silver' in j and 'perc' not in j:
                        silver = i[j]
                    if 'sodium' in j and 'perc' not in j and 'ratio' not in j and 'mg' not in j:
                        sodium = i[j]
                    if 'sulfur' in j and 'perc' not in j:
                        sulfur = i[j]
                    if 'thallium' in j and 'perc' not in j:
                        thallium = i[j]
                    if 'uranium' in j and 'perc' not in j:
                        uranium = i[j]
                    if 'vanadium' in j and 'perc' not in j:
                        vanadium = i[j]
                    if 'zinc' in j and 'perc' not in j:
                        zinc = i[j]
                    if 'kca_ratio' in j:
                        kca_ratio = i[j]
                    if 'hardness' in j:
                        hardness = i[j]
                    if 'sodium_absorption_ratio' in j:
                        SAR = i[j]
                    if 'calcium' in j and 'perc' in j:
                        calcium_percent = i[j]
                    if 'potassium' in j and 'perc' in j:
                        potassium_percent = i[j]
                    if 'magnesium' in j and 'perc' in j:
                        magnesium_percent = i[j]
                    if ('esp' in j or ('sodium' in j and 'perc' in j)) and 'mg' not in j:
                        sodium_percent = i[j]
                    if 'sodium' in j and 'mg' in j:
                        sodium_honee = i[j]
                    if 'cation_exchange_capacity' in j:
                        cec = i[j]
                    if 'base_exchange_capacity' in j:
                        bec = i[j]
                    if 'acidity' in j:
                        acidity = i[j]
                    if 'weight' == j:
                        weight = i[j]


        #Aluminum
            if aluminum is not None and api.get_workflow_status_of(aluminum) in ['unassigned'] and not filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Al')].empty:
                print("Importing Aluminum")
                print("Obtaining Result")
                aluminum.Result = unicode(filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Al')]['Formatted Result'].values[0].strip(), "utf-8")
                print("Obtaining Date/Time")
                aluminum.AnalysisDateTime = filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Al')]['Test Date/Time'].values[0]
                aluminum.CustomMethod = method.UID()
                print("Reindexing Result, Method, and AnalysisDateTime")
                aluminum.reindexObject(idxs=['Result','AnalysisDateTime','CustomMethod'])
                print("Result is {0}".format(aluminum.Result))
                print("AnalysisDateTime is {0}".format(aluminum.AnalysisDateTime))
                print("Checking if Submit is viable")
                if [j for j in api.get_transitions_for(aluminum) if 'submit' in j.values()]:
                    print("Submitting")
                    try:
                        api.do_transition_for(aluminum, "submit")
                    except AttributeError:
                        pass
                print("Checking for Analyst")
                if 'Analyst' in filtered_df.columns and not filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Al')]['Analyst'].empty:
                    print("Obtaining Analyst")
                    aluminum.Analyst = filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Al')]['Analyst'].values[0]
                    print("Reindexing Analyst")
                    aluminum.reindexObject(idxs=['Analyst'])
                print("Setting Imported to True")
                found = True

        #Arsenic
            if arsenic is not None and api.get_workflow_status_of(arsenic) in ['unassigned'] and not filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='As')].empty:
                print("Importing arsenic")
                arsenic.Result = unicode(filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='As')]['Formatted Result'].values[0].strip(), "utf-8")
                arsenic.AnalysisDateTime = filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='As')]['Test Date/Time'].values[0]
                arsenic.CustomMethod = method.UID()
                arsenic.reindexObject(idxs=['Result','AnalysisDateTime','CustomMethod'])
                if [j for j in api.get_transitions_for(arsenic) if 'submit' in j.values()]:
                    try:
                        api.do_transition_for(arsenic, "submit")
                    except AttributeError:
                        pass
                if 'Analyst' in filtered_df.columns and not filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='As')]['Analyst'].empty:
                    arsenic.Analyst = filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='As')]['Analyst'].values[0]
                    arsenic.reindexObject(idxs=['Analyst'])
                found = True
        #Barium
            if barium is not None and api.get_workflow_status_of(barium) in ['unassigned'] and not filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Ba')].empty:
                print("Importing Barium")
                barium.Result = unicode(filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Ba')]['Formatted Result'].values[0].strip(), "utf-8")
                barium.AnalysisDateTime = filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Ba')]['Test Date/Time'].values[0]
                barium.CustomMethod = method.UID()
                barium.reindexObject(idxs=['Result','AnalysisDateTime','CustomMethod'])
                if [j for j in api.get_transitions_for(barium) if 'submit' in j.values()]:
                    try:
                        api.do_transition_for(barium, "submit")
                    except AttributeError:
                        pass
                if 'Analyst' in filtered_df.columns and not filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Ba')]['Analyst'].empty:
                    barium.Analyst = filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Ba')]['Analyst'].values[0]
                    barium.reindexObject(idxs=['Analyst'])
                found = True
        #Beryllium
            if beryllium is not None and api.get_workflow_status_of(beryllium) in ['unassigned'] and not filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Be')].empty:
                print("Importing Beryllium")
                beryllium.Result = unicode(filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Be')]['Formatted Result'].values[0].strip(), "utf-8")
                beryllium.AnalysisDateTime = filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Be')]['Test Date/Time'].values[0]
                beryllium.CustomMethod = method.UID()
                beryllium.reindexObject(idxs=['Result','AnalysisDateTime','CustomMethod'])
                if [j for j in api.get_transitions_for(beryllium) if 'submit' in j.values()]:
                    try:
                        api.do_transition_for(beryllium, "submit")
                    except AttributeError:
                        pass
                if 'Analyst' in filtered_df.columns and not filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Be')]['Analyst'].empty:
                    beryllium.Analyst = filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Be')]['Analyst'].values[0]
                    beryllium.reindexObject(idxs=['Analyst'])
                found = True
        #Boron
            if boron is not None and api.get_workflow_status_of(boron) in ['unassigned'] and not filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='B')].empty:
                print("Importing Boron")
                boron.Result = unicode(filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='B')]['Formatted Result'].values[0].strip(), "utf-8")
                boron.AnalysisDateTime = filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='B')]['Test Date/Time'].values[0]
                boron.CustomMethod = method.UID()
                boron.reindexObject(idxs=['Result','AnalysisDateTime','CustomMethod'])
                if [j for j in api.get_transitions_for(boron) if 'submit' in j.values()]:
                    try:
                        api.do_transition_for(boron, "submit")
                    except AttributeError:
                        pass
                if 'Analyst' in filtered_df.columns and not filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='B')]['Analyst'].empty:
                    boron.Analyst = filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='B')]['Analyst'].values[0]
                    boron.reindexObject(idxs=['Analyst'])
                found = True
        #Calcium:
            if calcium  is not None and api.get_workflow_status_of(calcium) in ['unassigned'] and not filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Ca')].empty:
                print("Importing Calcium")
                calcium.Result = unicode(filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Ca')]['Formatted Result'].values[0].strip(), "utf-8")
                calcium.AnalysisDateTime = filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Ca')]['Test Date/Time'].values[0]
                calcium.CustomMethod = method.UID()
                calcium.reindexObject(idxs=['Result','AnalysisDateTime','CustomMethod'])
                if [j for j in api.get_transitions_for(calcium) if 'submit' in j.values()]:
                    try:
                        api.do_transition_for(calcium, "submit")
                    except AttributeError:
                        pass
                if 'Analyst' in filtered_df.columns and not filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Ca')]['Analyst'].empty:
                    calcium.Analyst = filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Ca')]['Analyst'].values[0]
                    calcium.reindexObject(idxs=['Analyst'])
                found = True
        #Cadmium
            if cadmium is not None and api.get_workflow_status_of(cadmium) in ['unassigned'] and not filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Cd')].empty:
                print("Importing cadmium")
                cadmium.Result = unicode(filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Cd')]['Formatted Result'].values[0].strip(), "utf-8")
                cadmium.AnalysisDateTime = filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Cd')]['Test Date/Time'].values[0]
                cadmium.CustomMethod = method.UID()
                cadmium.reindexObject(idxs=['Result','AnalysisDateTime','CustomMethod'])
                if [j for j in api.get_transitions_for(cadmium) if 'submit' in j.values()]:
                    try:
                        api.do_transition_for(cadmium, "submit")
                    except AttributeError:
                        pass
                if 'Analyst' in filtered_df.columns and not filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Cd')]['Analyst'].empty:
                    cadmium.Analyst = filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Cd')]['Analyst'].values[0]
                    cadmium.reindexObject(idxs=['Analyst'])
                found = True
        #Cobalt
            if cobalt is not None and api.get_workflow_status_of(cobalt) in ['unassigned'] and not filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Co')].empty:
                print("Importing Cobalt")
                cobalt.Result = unicode(filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Co')]['Formatted Result'].values[0].strip(), "utf-8")
                cobalt.AnalysisDateTime = filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Co')]['Test Date/Time'].values[0]
                cobalt.CustomMethod = method.UID()
                cobalt.reindexObject(idxs=['Result','AnalysisDateTime','CustomMethod'])
                if [j for j in api.get_transitions_for(cobalt) if 'submit' in j.values()]:
                    try:
                        api.do_transition_for(cobalt, "submit")
                    except AttributeError:
                        pass
                if 'Analyst' in filtered_df.columns and not filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Co')]['Analyst'].empty:
                    cobalt.Analyst = filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Co')]['Analyst'].values[0]
                    cobalt.reindexObject(idxs=['Analyst'])
                found = True
        #Chromium
            if chromium is not None and api.get_workflow_status_of(chromium) in ['unassigned'] and not filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Cr')].empty:
                print("Importing chromium")
                chromium.Result = unicode(filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Cr')]['Formatted Result'].values[0].strip(), "utf-8")
                chromium.AnalysisDateTime = filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Cr')]['Test Date/Time'].values[0]
                chromium.CustomMethod = method.UID()
                chromium.reindexObject(idxs=['Result','AnalysisDateTime','CustomMethod'])
                if [j for j in api.get_transitions_for(chromium) if 'submit' in j.values()]:
                    try:
                        api.do_transition_for(chromium, "submit")
                    except AttributeError:
                        pass
                if 'Analyst' in filtered_df.columns and not filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Cr')]['Analyst'].empty:
                    chromium.Analyst = filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Cr')]['Analyst'].values[0]
                    chromium.reindexObject(idxs=['Analyst'])
                found = True
        #Copper
            if copper is not None and api.get_workflow_status_of(copper) in ['unassigned'] and not filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Cu')].empty:
                print("Importing Copper")
                copper.Result = unicode(filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Cu')]['Formatted Result'].values[0].strip(), "utf-8")
                copper.AnalysisDateTime = filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Cu')]['Test Date/Time'].values[0]
                copper.CustomMethod = method.UID()
                copper.reindexObject(idxs=['Result','AnalysisDateTime','CustomMethod'])
                if [j for j in api.get_transitions_for(copper) if 'submit' in j.values()]:
                    try:
                        api.do_transition_for(copper, "submit")
                    except AttributeError:
                        pass
                if 'Analyst' in filtered_df.columns and not filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Cu')]['Analyst'].empty:
                    copper.Analyst = filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Cu')]['Analyst'].values[0]
                    copper.reindexObject(idxs=['Analyst'])
                found = True
        #Iron
            if iron is not None and api.get_workflow_status_of(iron) in ['unassigned'] and not filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Fe')].empty:
                print("Importing Iron")
                iron.Result = unicode(filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Fe')]['Formatted Result'].values[0].strip(), "utf-8")
                iron.AnalysisDateTime = filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Fe')]['Test Date/Time'].values[0]
                iron.CustomMethod = method.UID()
                iron.reindexObject(idxs=['Result','AnalysisDateTime','CustomMethod'])
                if [j for j in api.get_transitions_for(iron) if 'submit' in j.values()]:
                    try:
                        api.do_transition_for(iron, "submit")
                    except AttributeError:
                        pass
                if 'Analyst' in filtered_df.columns and not filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Fe')]['Analyst'].empty:
                    iron.Analyst = filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Fe')]['Analyst'].values[0]
                    iron.reindexObject(idxs=['Analyst'])
                found = True
        #Lead
            if lead is not None and api.get_workflow_status_of(lead) in ['unassigned'] and not filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Pb')].empty:
                print("Importing Lead")
                lead.Result = unicode(filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Pb')]['Formatted Result'].values[0].strip(), "utf-8")
                lead.AnalysisDateTime = filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Pb')]['Test Date/Time'].values[0]
                lead.CustomMethod = method.UID()
                lead.reindexObject(idxs=['Result','AnalysisDateTime','CustomMethod'])
                if [j for j in api.get_transitions_for(lead) if 'submit' in j.values()]:
                    try:
                        api.do_transition_for(lead, "submit")
                    except AttributeError:
                        pass
                if 'Analyst' in filtered_df.columns and not filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Pb')]['Analyst'].empty:
                    lead.Analyst = filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Pb')]['Analyst'].values[0]
                    lead.reindexObject(idxs=['Analyst'])
                found = True
        #Magnesium
            if magnesium is not None and api.get_workflow_status_of(magnesium) in ['unassigned'] and not filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Mg')].empty:
                print("Importing Magnesium")
                magnesium.Result = unicode(filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Mg')]['Formatted Result'].values[0].strip(), "utf-8")
                magnesium.AnalysisDateTime = filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Mg')]['Test Date/Time'].values[0]
                magnesium.CustomMethod = method.UID()
                magnesium.reindexObject(idxs=['Result','AnalysisDateTime','CustomMethod'])
                if [j for j in api.get_transitions_for(magnesium) if 'submit' in j.values()]:
                    try:
                        api.do_transition_for(magnesium, "submit")
                    except AttributeError:
                        pass
                if 'Analyst' in filtered_df.columns and not filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Mg')]['Analyst'].empty:
                    magnesium.Analyst = filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Mg')]['Analyst'].values[0]
                    magnesium.reindexObject(idxs=['Analyst'])
                found = True
        #Manganese
            if manganese is not None and api.get_workflow_status_of(manganese) in ['unassigned'] and not filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Mn')].empty:
                print("Importing Manganese")
                manganese.Result = unicode(filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Mn')]['Formatted Result'].values[0].strip(), "utf-8")
                manganese.AnalysisDateTime = filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Mn')]['Test Date/Time'].values[0]
                manganese.CustomMethod = method.UID()
                manganese.reindexObject(idxs=['Result','AnalysisDateTime','CustomMethod'])
                if [j for j in api.get_transitions_for(manganese) if 'submit' in j.values()]:
                    try:
                        api.do_transition_for(manganese, "submit")
                    except AttributeError:
                        pass
                if 'Analyst' in filtered_df.columns and not filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Mn')]['Analyst'].empty:
                    manganese.Analyst = filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Mn')]['Analyst'].values[0]
                    manganese.reindexObject(idxs=['Analyst'])
                found = True
        #Molybdenum
            if molybdenum is not None and api.get_workflow_status_of(molybdenum) in ['unassigned'] and not filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Mo')].empty:
                print("Importing Molybdenum")
                molybdenum.Result = unicode(filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Mo')]['Formatted Result'].values[0].strip(), "utf-8")
                molybdenum.AnalysisDateTime = filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Mo')]['Test Date/Time'].values[0]
                molybdenum.CustomMethod = method.UID()
                molybdenum.reindexObject(idxs=['Result','AnalysisDateTime','CustomMethod'])
                if [j for j in api.get_transitions_for(molybdenum) if 'submit' in j.values()]:
                    try:
                        api.do_transition_for(molybdenum, "submit")
                    except AttributeError:
                        pass
                if 'Analyst' in filtered_df.columns and not filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Mo')]['Analyst'].empty:
                    molybdenum.Analyst = filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Mo')]['Analyst'].values[0]
                    molybdenum.reindexObject(idxs=['Analyst'])
                found = True
        #Nickel
            if nickel is not None and api.get_workflow_status_of(nickel) in ['unassigned'] and not filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Ni')].empty:
                print("Importing Nickel")
                nickel.Result = unicode(filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Ni')]['Formatted Result'].values[0].strip(), "utf-8")
                nickel.AnalysisDateTime = filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Ni')]['Test Date/Time'].values[0]
                nickel.CustomMethod = method.UID()
                nickel.reindexObject(idxs=['Result','AnalysisDateTime','CustomMethod'])
                if [j for j in api.get_transitions_for(nickel) if 'submit' in j.values()]:
                    try:
                        api.do_transition_for(nickel, "submit")
                    except AttributeError:
                        pass
                if 'Analyst' in filtered_df.columns and not filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Ni')]['Analyst'].empty:
                    nickel.Analyst = filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Ni')]['Analyst'].values[0]
                    nickel.reindexObject(idxs=['Analyst'])
                found = True
        #Phosphorus
            if phosphorus is not None and api.get_workflow_status_of(phosphorus) in ['unassigned'] and not filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='P')].empty:
                print("Importing Phosphorus")
                phosphorus.Result = unicode(filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='P')]['Formatted Result'].values[0].strip(), "utf-8")
                phosphorus.AnalysisDateTime = filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='P')]['Test Date/Time'].values[0]
                phosphorus.CustomMethod = method.UID()
                phosphorus.reindexObject(idxs=['Result','AnalysisDateTime','CustomMethod'])
                if [j for j in api.get_transitions_for(phosphorus) if 'submit' in j.values()]:
                    try:
                        api.do_transition_for(phosphorus, "submit")
                    except AttributeError:
                        pass
                if 'Analyst' in filtered_df.columns and not filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='P')]['Analyst'].empty:
                    phosphorus.Analyst = filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='P')]['Analyst'].values[0]
                    phosphorus.reindexObject(idxs=['Analyst'])
                found = True
        #Potassium
            if potassium is not None and api.get_workflow_status_of(potassium) in ['unassigned'] and not filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='K')].empty:
                print("Importing Potassium")
                print("Potassium should be: {0}".format(filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='K')]))
                potassium.Result = unicode(filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='K')]['Formatted Result'].values[0].strip(), "utf-8")
                potassium.AnalysisDateTime = filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='K')]['Test Date/Time'].values[0]
                potassium.CustomMethod = method.UID()
                potassium.reindexObject(idxs=['Result','AnalysisDateTime','CustomMethod'])
                if [j for j in api.get_transitions_for(potassium) if 'submit' in j.values()]:
                    try:
                        api.do_transition_for(potassium, "submit")
                    except AttributeError:
                        pass
                if 'Analyst' in filtered_df.columns and not filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='K')]['Analyst'].empty:
                    potassium.Analyst = filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='K')]['Analyst'].values[0]
                    potassium.reindexObject(idxs=['Analyst'])
                found = True
        #Selenium
            if selenium is not None and api.get_workflow_status_of(selenium) in ['unassigned'] and not filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Se')].empty:
                print("Importing Selenium")
                selenium.Result = unicode(filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Se')]['Formatted Result'].values[0].strip(), "utf-8")
                selenium.AnalysisDateTime = filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Se')]['Test Date/Time'].values[0]
                selenium.CustomMethod = method.UID()
                selenium.reindexObject(idxs=['Result','AnalysisDateTime','CustomMethod'])
                if [j for j in api.get_transitions_for(selenium) if 'submit' in j.values()]:
                    try:
                        api.do_transition_for(selenium, "submit")
                    except AttributeError:
                        pass
                if 'Analyst' in filtered_df.columns and not filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Se')]['Analyst'].empty:
                    selenium.Analyst = filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Se')]['Analyst'].values[0]
                    selenium.reindexObject(idxs=['Analyst'])
                found = True
        #Silica
            if silica is not None and api.get_workflow_status_of(silica) in ['unassigned'] and not filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Si')].empty:
                print("Importing Silica")
                silica.Result = unicode(filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Si')]['Formatted Result'].values[0].strip(), "utf-8")
                silica.AnalysisDateTime = filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Si')]['Test Date/Time'].values[0]
                silica.CustomMethod = method.UID()
                silica.reindexObject(idxs=['Result','AnalysisDateTime','CustomMethod'])
                if [j for j in api.get_transitions_for(silica) if 'submit' in j.values()]:
                    try:
                        api.do_transition_for(silica, "submit")
                    except AttributeError:
                        pass
                if 'Analyst' in filtered_df.columns and not filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Si')]['Analyst'].empty:
                    silica.Analyst = filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Si')]['Analyst'].values[0]
                    silica.reindexObject(idxs=['Analyst'])
                found = True
        #Silver
            if silver is not None and api.get_workflow_status_of(silver) in ['unassigned'] and not filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Ag')].empty:
                print("Importing Silver")
                silver.Result = unicode(filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Ag')]['Formatted Result'].values[0].strip(), "utf-8")
                silver.AnalysisDateTime = filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Ag')]['Test Date/Time'].values[0]
                silver.CustomMethod = method.UID()
                silver.reindexObject(idxs=['Result','AnalysisDateTime','CustomMethod'])
                if [j for j in api.get_transitions_for(silver) if 'submit' in j.values()]:
                    try:
                        api.do_transition_for(silver, "submit")
                    except AttributeError:
                        pass
                if 'Analyst' in filtered_df.columns and not filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Ag')]['Analyst'].empty:
                    silver.Analyst = filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Ag')]['Analyst'].values[0]
                    silver.reindexObject(idxs=['Analyst'])
                found = True
        #Sodium
            if sodium is not None and api.get_workflow_status_of(sodium) in ['unassigned'] and not filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Na')].empty:
                print("Importing Sodium")
                sodium.Result = unicode(filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Na')]['Formatted Result'].values[0].strip(), "utf-8")
                sodium.AnalysisDateTime = filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Na')]['Test Date/Time'].values[0]
                sodium.CustomMethod = method.UID()
                sodium.reindexObject(idxs=['Result','AnalysisDateTime','CustomMethod'])
                if [j for j in api.get_transitions_for(sodium) if 'submit' in j.values()]:
                    try:
                        api.do_transition_for(sodium, "submit")
                    except AttributeError:
                        pass
                if 'Analyst' in filtered_df.columns and not filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Na')]['Analyst'].empty:
                    sodium.Analyst = filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Na')]['Analyst'].values[0]
                    sodium.reindexObject(idxs=['Analyst'])
                found = True
        #Sulfur
            if sulfur is not None and api.get_workflow_status_of(sulfur) in ['unassigned'] and not filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='S')].empty:
                print("Importing Sulfur")
                sulfur.Result = unicode(filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='S')]['Formatted Result'].values[0].strip(), "utf-8")
                sulfur.AnalysisDateTime = filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='S')]['Test Date/Time'].values[0]
                sulfur.CustomMethod = method.UID()
                sulfur.reindexObject(idxs=['Result','AnalysisDateTime','CustomMethod'])
                if [j for j in api.get_transitions_for(sulfur) if 'submit' in j.values()]:
                    try:
                        api.do_transition_for(sulfur, "submit")
                    except AttributeError:
                        pass
                if 'Analyst' in filtered_df.columns and not filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='S')]['Analyst'].empty:
                    sulfur.Analyst = filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='S')]['Analyst'].values[0]
                    sulfur.reindexObject(idxs=['Analyst'])
                found = True
        #Thallium
            if thallium is not None and api.get_workflow_status_of(thallium) in ['unassigned'] and not filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Tl')].empty:
                print("Importing Thallium")
                thallium.Result = unicode(filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Tl')]['Formatted Result'].values[0].strip(), "utf-8")
                thallium.AnalysisDateTime = filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Tl')]['Test Date/Time'].values[0]
                thallium.CustomMethod = method.UID()
                thallium.reindexObject(idxs=['Result','AnalysisDateTime','CustomMethod'])
                if [j for j in api.get_transitions_for(thallium) if 'submit' in j.values()]:
                    try:
                        api.do_transition_for(thallium, "submit")
                    except AttributeError:
                        pass
                if 'Analyst' in filtered_df.columns and not filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Tl')]['Analyst'].empty:
                    thallium.Analyst = filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Tl')]['Analyst'].values[0]
                    thallium.reindexObject(idxs=['Analyst'])
                found = True
        #Uranium
            if uranium is not None and api.get_workflow_status_of(uranium) in ['unassigned'] and not filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='U')].empty:
                print("Importing uranium")
                uranium.Result = unicode(filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='U')]['Formatted Result'].values[0].strip(), "utf-8")
                uranium.AnalysisDateTime = filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='U')]['Test Date/Time'].values[0]
                uranium.CustomMethod = method.UID()
                uranium.reindexObject(idxs=['Result','AnalysisDateTime','CustomMethod'])
                if [j for j in api.get_transitions_for(uranium) if 'submit' in j.values()]:
                    try:
                        api.do_transition_for(uranium, "submit")
                    except AttributeError:
                        pass
                if 'Analyst' in filtered_df.columns and not filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='U')]['Analyst'].empty:
                    uranium.Analyst = filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='U')]['Analyst'].values[0]
                    uranium.reindexObject(idxs=['Analyst'])
                found = True
        #Vanadium
            if vanadium is not None and api.get_workflow_status_of(vanadium) in ['unassigned'] and not filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='V')].empty:
                print("Importing vanadium")
                vanadium.Result = unicode(filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='V')]['Formatted Result'].values[0].strip(), "utf-8")
                vanadium.AnalysisDateTime = filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='V')]['Test Date/Time'].values[0]
                vanadium.CustomMethod = method.UID()
                vanadium.reindexObject(idxs=['Result','AnalysisDateTime','CustomMethod'])
                if [j for j in api.get_transitions_for(vanadium) if 'submit' in j.values()]:
                    try:
                        api.do_transition_for(vanadium, "submit")
                    except AttributeError:
                        pass
                if 'Analyst' in filtered_df.columns and not filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='V')]['Analyst'].empty:
                    vanadium.Analyst = filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='V')]['Analyst'].values[0]
                    vanadium.reindexObject(idxs=['Analyst'])
                found = True
        #Zinc
            if zinc is not None and api.get_workflow_status_of(zinc) in ['unassigned'] and not filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Zn')].empty:
                print("Importing Zinc")
                zinc.Result = unicode(filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Zn')]['Formatted Result'].values[0].strip(), "utf-8")
                zinc.AnalysisDateTime = filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Zn')]['Test Date/Time'].values[0]
                zinc.CustomMethod = method.UID()
                zinc.reindexObject(idxs=['Result','AnalysisDateTime','CustomMethod'])
                if [j for j in api.get_transitions_for(zinc) if 'submit' in j.values()]:
                    try:
                        api.do_transition_for(zinc, "submit")
                    except AttributeError:
                        pass
                if 'Analyst' in filtered_df.columns and not filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Zn')]['Analyst'].empty:
                    zinc.Analyst = filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Zn')]['Analyst'].values[0]
                    zinc.reindexObject(idxs=['Analyst'])
                found = True

        #K/Ca Ratio
            if kca_ratio is not None and api.get_workflow_status_of(kca_ratio) in ['unassigned'] and potassium.Result is not None and calcium.Result is not None:
                print("Importing KCA")
                try:
                    k_float = float(potassium.Result)
                    ca_float = float(calcium.Result)
                    kca_ratio.Result = unicode(k_float/ca_float)
                    kca_ratio.AnalysisDateTime = potassium.AnalysisDateTime or calcium.AnalysisDateTime
                    kca_ratio.CustomMethod = kca_method.UID()
                    kca_ratio.reindexObject(idxs=['Result','AnalysisDateTime','CustomMethod'])
                    if [j for j in api.get_transitions_for(kca_ratio) if 'submit' in j.values()]:
                        try:
                            api.do_transition_for(kca_ratio, "submit")
                        except AttributeError:
                            pass
                    kca_ratio.Analyst = potassium.Analyst or calcium.Analyst
                    kca_ratio.reindexObject(idxs=['Analyst'])
                    found = True
                except ValueError:
                    print("--FLOAT CONVERSION ERROR--")
                    print("Sample is: {0}".format(i))
                    print("Potassium is: {0}".format(potassium.Result))
                    print("Calcium is: {0}".format(calcium.Result))

        #Hardness
            if hardness is not None and api.get_workflow_status_of(hardness) in ['unassigned'] and magnesium.Result is not None and calcium.Result is not None:
                print("Importing Hardness")
                try:
                    mg_float = float(magnesium.Result)
                    ca_float = float(calcium.Result)
                    hardness.Result = unicode((mg_float*4.118)+(ca_float*2.497))
                    hardness.AnalysisDateTime = magnesium.AnalysisDateTime or calcium.AnalysisDateTime
                    hardness.CustomMethod = hardness_method.UID()
                    hardness.reindexObject(idxs=['Result','AnalysisDateTime','CustomMethod'])
                    if [j for j in api.get_transitions_for(hardness) if 'submit' in j.values()]:
                        try:
                            api.do_transition_for(hardness, "submit")
                        except AttributeError:
                            pass
                    hardness.Analyst = magnesium.Analyst or calcium.Analyst
                    hardness.reindexObject(idxs=['Analyst'])
                    found = True
                except ValueError:
                    print("--FLOAT CONVERSION ERROR--")
                    print("Sample is: {0}".format(i))
                    print("Magnesium is: {0}".format(magnesium.Result))
                    print("Calcium is: {0}".format(calcium.Result))

        #Sodium Absorption Ratio
            if SAR is not None and api.get_workflow_status_of(SAR) in ['unassigned'] and calcium.Result is not None and magnesium.Result is not None and sodium.Result is not None:
                print("Importing KCA")
                try:
                    from math import sqrt
                    mg_float = float(magnesium.Result)
                    na_float = float(sodium.Result)
                    ca_float = float(calcium.Result)
                    SAR.Result = unicode((na_float)/sqrt(((ca_float)+(mg_float))/2))
                    SAR.AnalysisDateTime = sodium.AnalysisDateTime or calcium.AnalysisDateTime or magnesium.AnalysisDateTime
                    SAR.CustomMethod = sar_method.UID()
                    SAR.reindexObject(idxs=['Result','AnalysisDateTime','CustomMethod'])
                    if [j for j in api.get_transitions_for(SAR) if 'submit' in j.values()]:
                        try:
                            api.do_transition_for(SAR, "submit")
                        except AttributeError:
                            pass
                    SAR.Analyst = magnesium.Analyst or calcium.Analyst or sodium.Analyst
                    SAR.reindexObject(idxs=['Analyst'])
                    found = True
                except ValueError:
                    print("--FLOAT CONVERSION ERROR--")
                    print("Sample is: {0}".format(i))
                    print("Magnesium is: {0}".format(magnesium.Result))
                    print("Sodium is: {0}".format(sodium.Result))
                    print("Calcium is: {0}".format(calcium.Result))

        #Potassium Percent
            if potassium_percent is not None and api.get_workflow_status_of(potassium_percent) in ['unassigned'] and potassium.Result is not None and calcium.Result is not None and magnesium.Result is not None and sodium.Result is not None:
                print("Importing Potassium Percent")
                try:
                    ca_float = float(calcium.Result)/200
                    k_float = float(potassium.Result)/390
                    mg_float = float(magnesium.Result)/120
                    na_float = float(sodium.Result)/230
                    potassium_percent.Result = unicode(100*((k_float)/(ca_float+k_float+mg_float+na_float)))
                    potassium_percent.AnalysisDateTime = potassium.AnalysisDateTime or calcium.AnalysisDateTime or magnesium.AnalysisDateTime or sodium.AnalysisDateTime
                    potassium_percent.CustomMethod = rs_method.UID()
                    potassium_percent.reindexObject(idxs=['Result','AnalysisDateTime','CustomMethod'])
                    if [j for j in api.get_transitions_for(potassium_percent) if 'submit' in j.values()]:
                        try:
                            api.do_transition_for(potassium_percent, "submit")
                        except AttributeError:
                            pass
                    potassium_percent.Analyst = potassium.Analyst or calcium.Analyst
                    potassium_percent.reindexObject(idxs=['Analyst'])
                    found = True
                except ValueError:
                    print("--FLOAT CONVERSION ERROR--")
                    print("Sample is: {0}".format(i))
                    print("Potassium is: {0}".format(potassium.Result))
                    print("Calcium is: {0}".format(calcium.Result))

        #Magnesium Percent
            if magnesium_percent is not None and api.get_workflow_status_of(magnesium_percent) in ['unassigned'] and potassium.Result is not None and calcium.Result is not None and magnesium.Result is not None and sodium.Result is not None:
                print("Importing Magnesium Percent")
                try:
                    ca_float = float(calcium.Result)/200
                    k_float = float(potassium.Result)/390
                    mg_float = float(magnesium.Result)/120
                    na_float = float(sodium.Result)/230
                    magnesium_percent.Result = unicode(100*((mg_float)/(ca_float+k_float+mg_float+na_float)))
                    magnesium_percent.AnalysisDateTime = potassium.AnalysisDateTime or calcium.AnalysisDateTime or magnesium.AnalysisDateTime or sodium.AnalysisDateTime
                    magnesium_percent.CustomMethod = rs_method.UID()
                    magnesium_percent.reindexObject(idxs=['Result','AnalysisDateTime','CustomMethod'])
                    if [j for j in api.get_transitions_for(magnesium_percent) if 'submit' in j.values()]:
                        try:
                            api.do_transition_for(magnesium_percent, "submit")
                        except AttributeError:
                            pass
                    magnesium_percent.Analyst = potassium.Analyst or calcium.Analyst
                    magnesium_percent.reindexObject(idxs=['Analyst'])
                    found = True
                except ValueError:
                    print("--FLOAT CONVERSION ERROR--")
                    print("Sample is: {0}".format(i))
                    print("Potassium is: {0}".format(potassium.Result))
                    print("Calcium is: {0}".format(calcium.Result))
        #Sodium Percent
            if sodium_percent is not None and api.get_workflow_status_of(sodium_percent) in ['unassigned'] and potassium.Result is not None and calcium.Result is not None and magnesium.Result is not None and sodium.Result is not None:
                print("Importing Sodium Percent")
                try:
                    ca_float = float(calcium.Result)/200
                    k_float = float(potassium.Result)/390
                    mg_float = float(magnesium.Result)/120
                    na_float = float(sodium.Result)/230
                    sodium_percent.Result = unicode(100*((na_float)/(ca_float+k_float+mg_float+na_float)))
                    sodium_percent.AnalysisDateTime = potassium.AnalysisDateTime or calcium.AnalysisDateTime or magnesium.AnalysisDateTime or sodium.AnalysisDateTime
                    sodium_percent.CustomMethod = rs_method.UID()
                    sodium_percent.reindexObject(idxs=['Result','AnalysisDateTime','CustomMethod'])
                    if [j for j in api.get_transitions_for(sodium_percent) if 'submit' in j.values()]:
                        try:
                            api.do_transition_for(sodium_percent, "submit")
                        except AttributeError:
                            pass
                    sodium_percent.Analyst = potassium.Analyst or calcium.Analyst
                    sodium_percent.reindexObject(idxs=['Analyst'])
                    found = True
                except ValueError:
                    print("--FLOAT CONVERSION ERROR--")
                    print("Sample is: {0}".format(i))
                    print("Potassium is: {0}".format(potassium.Result))
                    print("Calcium is: {0}".format(calcium.Result))


        #Calcium Percent
            if calcium_percent is not None and api.get_workflow_status_of(calcium_percent) in ['unassigned'] and potassium.Result is not None and calcium.Result is not None and magnesium.Result is not None and sodium.Result is not None:
                print("Importing Calcium Percent")
                try:
                    ca_float = float(calcium.Result)/200
                    k_float = float(potassium.Result)/390
                    mg_float = float(magnesium.Result)/120
                    na_float = float(sodium.Result)/230
                    calcium_percent.Result = unicode(100*((ca_float)/(ca_float+k_float+mg_float+na_float)))
                    calcium_percent.AnalysisDateTime = potassium.AnalysisDateTime or calcium.AnalysisDateTime or magnesium.AnalysisDateTime or sodium.AnalysisDateTime
                    calcium_percent.CustomMethod = rs_method.UID()
                    calcium_percent.reindexObject(idxs=['Result','AnalysisDateTime','CustomMethod'])
                    if [j for j in api.get_transitions_for(calcium_percent) if 'submit' in j.values()]:
                        try:
                            api.do_transition_for(calcium_percent, "submit")
                        except AttributeError:
                            pass
                    calcium_percent.Analyst = potassium.Analyst or calcium.Analyst
                    calcium_percent.reindexObject(idxs=['Analyst'])
                    found = True
                except ValueError:
                    print("--FLOAT CONVERSION ERROR--")
                    print("Sample is: {0}".format(i))
                    print("Potassium is: {0}".format(potassium.Result))
                    print("Calcium is: {0}".format(calcium.Result))


        #Cation Exchange Capacity
            if cec is not None and api.get_workflow_status_of(cec) in ['unassigned'] and potassium.Result is not None and calcium.Result is not None and magnesium.Result is not None and sodium.Result is not None and aluminum.Result is not None:
                print("Importing Calcium Percent")
                try:
                    ca_float = float(calcium.Result)/200
                    k_float = float(potassium.Result)/390
                    mg_float = float(magnesium.Result)/120
                    na_float = float(sodium.Result)/230
                    al_float = float(aluminum.Result)/90
                    cec.Result = unicode(ca_float+k_float+mg_float+na_float+al_float)
                    cec.AnalysisDateTime = potassium.AnalysisDateTime or calcium.AnalysisDateTime or magnesium.AnalysisDateTime or sodium.AnalysisDateTime
                    cec.CustomMethod = rs_method.UID()
                    cec.reindexObject(idxs=['Result','AnalysisDateTime','CustomMethod'])
                    if [j for j in api.get_transitions_for(cec) if 'submit' in j.values()]:
                        try:
                            api.do_transition_for(cec, "submit")
                        except AttributeError:
                            pass
                    cec.Analyst = potassium.Analyst or calcium.Analyst
                    cec.reindexObject(idxs=['Analyst'])
                    found = True
                except ValueError:
                    pass


        #Base Exchange Capacity
            if bec is not None and api.get_workflow_status_of(bec) in ['unassigned'] and potassium.Result is not None and calcium.Result is not None and magnesium.Result is not None and sodium.Result is not None:
                print("Importing Calcium Percent")
                try:
                    ca_float = float(calcium.Result)/200
                    k_float = float(potassium.Result)/390
                    mg_float = float(magnesium.Result)/120
                    na_float = float(sodium.Result)/230
                    bec.Result = unicode(ca_float+k_float+mg_float+na_float)
                    bec.AnalysisDateTime = potassium.AnalysisDateTime or calcium.AnalysisDateTime or magnesium.AnalysisDateTime or sodium.AnalysisDateTime
                    bec.CustomMethod = rs_method.UID()
                    bec.reindexObject(idxs=['Result','AnalysisDateTime','CustomMethod'])
                    if [j for j in api.get_transitions_for(bec) if 'submit' in j.values()]:
                        try:
                            api.do_transition_for(bec, "submit")
                        except AttributeError:
                            pass
                    bec.Analyst = potassium.Analyst or calcium.Analyst
                    bec.reindexObject(idxs=['Analyst'])
                    found = True
                except ValueError:
                    pass
        #Acidity
            if acidity is not None and api.get_workflow_status_of(acidity) in ['unassigned'] and aluminum.Result is not None:
                print("Importing Calcium Percent")
                try:
                    acid_float = float(aluminum.Result)/90
                    acidity.Result = unicode(acid_float)
                    acidity.AnalysisDateTime = aluminum.AnalysisDateTime
                    acidity.CustomMethod = rs_method.UID()
                    acidity.reindexObject(idxs=['Result','AnalysisDateTime','CustomMethod'])
                    if [j for j in api.get_transitions_for(acidity) if 'submit' in j.values()]:
                        try:
                            api.do_transition_for(acidity, "submit")
                        except AttributeError:
                            pass
                    acidity.Analyst = aluminum.Analyst
                    acidity.reindexObject(idxs=['Analyst'])
                    found = True
                except ValueError:
                    pass


        #Honee Sodium
            if sodium_honee is not None and api.get_workflow_status_of(sodium_honee) in ['unassigned'] and sodium is not None and weight is not None and sodium.Result is not None and weight.Result is not None:
                print("Importing Calcium Percent")
                try:
                    sodium_float = float(sodium.Result)/1000
                    weight_float = float(weight.Result)
                    sodium_honee.Result = unicode(sodium_float * weight_float)
                    sodium_honee.AnalysisDateTime = sodium.AnalysisDateTime
                    sodium_honee.CustomMethod = method.UID()
                    sodium_honee.reindexObject(idxs=['Result','AnalysisDateTime','CustomMethod'])
                    if [j for j in api.get_transitions_for(sodium_honee) if 'submit' in j.values()]:
                        try:
                            api.do_transition_for(sodium_honee, "submit")
                        except AttributeError:
                            pass
                    sodium_honee.Analyst = sodium.Analyst
                    sodium_honee.reindexObject(idxs=['Analyst'])
                    found = True
                except ValueError:
                    pass

            if found:
                clean_ids.append(api.get_id(i))
            t.get().commit()

        return ','.join(clean_ids)


    @button.buttonAndHandler(u'Import')
    def handleApply(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return
        # Redirect back to the front page with a status message

        # get the actual data
        if data["IInstrumentReadFolder.sample"] is not None:
            file = data["IInstrumentReadFolder.sample"].data
            # do the processing
            number = self.processCSV(file)

            if not number:
                IStatusMessage(self.request).addStatusMessage(
                        u"The .CSV file was successfully read, but there were no new samples to import."
                    )
            else:
                IStatusMessage(self.request).addStatusMessage(
                        u"ICP data successfully imported for Samples: "+str(number)
                    )
        else:
            IStatusMessage(self.request).addStatusMessage(
                    u"No .CSV File for ICP data"
                )
        contextURL = self.context.absolute_url()
        self.request.response.redirect(contextURL)
