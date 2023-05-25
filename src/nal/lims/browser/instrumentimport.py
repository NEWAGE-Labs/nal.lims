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

class ICPImportView(edit.DefaultEditForm):

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
        rs_method = map(api.get_object,api.search({'portal_type':'Method','title':'RS Calc'}))[0]
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
            arsenic = None
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
            sodium = None
            sulfur = None
            zinc = None
            kca_ratio = None
	    hardness = None
	    SAR = None
            calcium_percent = None
            potassium_percent = None
            magnesium_percent = None
            sodium_percent = None



            for j in i:
                if api.get_workflow_status_of(i[j]) not in ['retracted','rejected','invalid','cancelled']:
                    if 'aluminum' in j and 'perc' not in j:
                        aluminum = i[j]
                    if 'arsenic' in j and 'perc' not in j:
                        arsenic = i[j]
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
                    if 'sodium' in j and 'perc' not in j and 'ratio' not in j:
                        sodium = i[j]
                    if 'sulfur' in j and 'perc' not in j:
                        sulfur = i[j]
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
                    if 'esp' in j or ('sodium' in j and 'perc' in j):
                        sodium_percent = i[j]



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
                imported.append(True)
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
                imported.append(True)
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
                imported.append(True)
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
                imported.append(True)
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
                imported.append(True)
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
                imported.append(True)
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
                imported.append(True)
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
                imported.append(True)
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
                imported.append(True)
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
                imported.append(True)
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
                imported.append(True)
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
                imported.append(True)
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
                imported.append(True)
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
                imported.append(True)
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
                imported.append(True)
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
                imported.append(True)
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
                imported.append(True)
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
                imported.append(True)
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
                imported.append(True)
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
                imported.append(True)
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
                imported.append(True)

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
                    imported.append(True)
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
                    imported.append(True)
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
                    SAR.Result = unicode((na_float/230)/sqrt(((ca_float/200)+(mg_float/120))/2))
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
                    imported.append(True)
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
                    potassium_percent.AnalysisDateTime = potassium.AnalysisDateTime or calcium.AnalysisDateTime or magnesium.AnalysisDateTime or sodium.AnalysisDateTIme
		    potassium_percent.CustomMethod = rs_method.UID()
                    potassium_percent.reindexObject(idxs=['Result','AnalysisDateTime','CustomMethod'])
                    if [j for j in api.get_transitions_for(potassium_percent) if 'submit' in j.values()]:
                        try:
                            api.do_transition_for(potassium_percent, "submit")
                        except AttributeError:
                            pass
                    potassium_percent.Analyst = potassium.Analyst or calcium.Analyst
                    potassium_percent.reindexObject(idxs=['Analyst'])
                    imported.append(True)
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
                    magnesium_percent.AnalysisDateTime = potassium.AnalysisDateTime or calcium.AnalysisDateTime or magnesium.AnalysisDateTime or sodium.AnalysisDateTIme
		    magnesium_percent.CustomMethod = rs_method.UID()
                    magnesium_percent.reindexObject(idxs=['Result','AnalysisDateTime','CustomMethod'])
                    if [j for j in api.get_transitions_for(magnesium_percent) if 'submit' in j.values()]:
                        try:
                            api.do_transition_for(magnesium_percent, "submit")
                        except AttributeError:
                            pass
                    magnesium_percent.Analyst = potassium.Analyst or calcium.Analyst
                    magnesium_percent.reindexObject(idxs=['Analyst'])
                    imported.append(True)
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
                    sodium_percent.AnalysisDateTime = potassium.AnalysisDateTime or calcium.AnalysisDateTime or magnesium.AnalysisDateTime or sodium.AnalysisDateTIme
		    sodium_percent.CustomMethod = rs_method.UID()
                    sodium_percent.reindexObject(idxs=['Result','AnalysisDateTime','CustomMethod'])
                    if [j for j in api.get_transitions_for(sodium_percent) if 'submit' in j.values()]:
                        try:
                            api.do_transition_for(sodium_percent, "submit")
                        except AttributeError:
                            pass
                    sodium_percent.Analyst = potassium.Analyst or calcium.Analyst
                    sodium_percent.reindexObject(idxs=['Analyst'])
                    imported.append(True)
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
                    calcium_percent.AnalysisDateTime = potassium.AnalysisDateTime or calcium.AnalysisDateTime or magnesium.AnalysisDateTime or sodium.AnalysisDateTIme
		    calcium_percent.CustomMethod = rs_method.UID()
                    calcium_percent.reindexObject(idxs=['Result','AnalysisDateTime','CustomMethod'])
                    if [j for j in api.get_transitions_for(calcium_percent) if 'submit' in j.values()]:
                        try:
                            api.do_transition_for(calcium_percent, "submit")
                        except AttributeError:
                            pass
                    calcium_percent.Analyst = potassium.Analyst or calcium.Analyst
                    calcium_percent.reindexObject(idxs=['Analyst'])
                    imported.append(True)
                except ValueError:
                    print("--FLOAT CONVERSION ERROR--")
                    print("Sample is: {0}".format(i))
                    print("Potassium is: {0}".format(potassium.Result))
                    print("Calcium is: {0}".format(calcium.Result))

            if imported:
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

class GalleryImportView(edit.DefaultEditForm):

    def __init__(self, context, request):
          self.context = context
          self.request = request

    def saveCSV(self, context, request):
        return context.absolute_url_path()

    def processCSV(self, data):
        """Process the CSV"""
        #Get logger for output messages
        logger = logging.getLogger("Plone")

        #Convert CSV data to a dataframe
        csv_coded = codecs.decode(data, 'UTF-16')
        csv_doc = StringIO.StringIO(csv_coded)
        csv_doc_copy = copy.deepcopy(csv_doc)
        dirty_csv = csv.reader(csv_doc_copy, delimiter='\t')
        skiplist = []
        j = 0
        for i in dirty_csv:
            print("i is: {0}".format(i))
            if i == []:
                skiplist.append(j)
                print("skipping blank row: "+str(j))
            elif i[0] == '' or i[0] == 'Time' or i[0] == 'Date':
                skiplist.append(j)
                print("skipping row: "+str(j))
            j += 1
        dirty_df = pd.read_csv(csv_doc, sep='\t', quotechar='"', keep_default_na=False, dtype=str, skiprows=tuple(skiplist)) #tuple() may not be needed
        #Convert Gallery CSV to Standard Import CSV format
        samples = []
        results = []
        tests = []
        dates = []
        analysts = []
        dict_to_df = {}
        for i, row in dirty_df.iterrows():
            if ('fl-0' in row["Sample/ctrl ID"].lower() or 'test-0' in row["Sample/ctrl ID"].lower()) and 'MA' in row['Status']:
                dirty_sample = row["Sample/ctrl ID"] # '1234 ppm'
                if 'x' in row["Sample/ctrl ID"].lower():
                    radix = dirty_sample.lower().find('x')
                    dilution = dirty_sample[radix+1:]
                    sid = dirty_sample[:radix] # '1234'
                else:
                    sid = dirty_sample
                    dilution = 1
                #Result
                try:
                    float_result = float(row['Result'])
                    float_dilution = float(dilution)
                except ValueError:
                    float_result = None
                    float_dilution = None
                if float_dilution is not None and float_result is not None:
                    #Sample
                    samples.append(sid)

                    calculated_result = str(float_dilution * float_result)
                    results.append(calculated_result)

                    #Test
                    if row['Test name'] in ['WWCl', 'Cl Low']:
                        tests.append('Chloride')
                    else:
                        tests.append(row['Test name'])
                    #Analyst
                    if 'Analyst' in row:
                        analysts.append(row['Analyst'])
                    else:
                        analysts.append('')
                    #Date
                    dates.append(row["Result time"])
            else:
                pass

        dict_to_df['Sample Name'] = samples
        dict_to_df['Result'] = results
        dict_to_df['Test'] = tests
        dict_to_df['Analyst'] = analysts
        dict_to_df['Analysis Date/Time'] = dates

        nh4_method = map(api.get_object, api.search({'portal_type':'Method','title':'SM4500 NH3-G'}))[0].UID()
        no3_method = map(api.get_object, api.search({'portal_type':'Method','title':'SM4500 NO3-G'}))[0].UID()
        cl_method = map(api.get_object, api.search({'portal_type':'Method','title':'SM4500 Cl-E'}))[0].UID()
	sugar_method = map(api.get_object, api.search({'portal_type':'Method','title':'AOAC 985.09'}))[0].UID()
	so4_method = map(api.get_object, api.search({'portal_type':'Method','title':'SM4500 SO4-E'}))[0].UID()

        df = pd.DataFrame.from_dict(dict_to_df)

        print(df)

	#Get a list of Unique sample names from the imported DataFrame
        sample_names = df['Sample Name'].unique()
        #Take off the '-001' to get a list of SDG titles to search
        batch_titles = df['Sample Name'].str[:-4].unique().tolist()
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
            if xsdg in batch_dict.keys():
                ars = batch_dict[xsdg]
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

            imported = []

	    sulfate = None
	    for j in i:
		if 'sulfate' in j and api.get_workflow_status_of(i[j]) not in ['cancelled','invalid','retracted','rejected']:
		    sulfate = i[j]

            #Ammonium
            found = False
            ammonium = None
            for j in range(20, 0, -1):
                if found==False:
                    sap_version = 'nitrogen_ammonium-'+str(j)
                    liqfert_version = 'nitrogen_ammonia-'+str(j)
                    if hasattr(i,sap_version) and api.get_workflow_status_of(i[sap_version]) not in ['cancelled','invalid','retracted','rejected']:
                        found = True
                        ammonium = i[sap_version]
                    elif hasattr(i,liqfert_version) and api.get_workflow_status_of(i[liqfert_version]) not in ['cancelled','invalid','retracted','rejected']:
                        found = True
                        ammonium = i[liqfert_version]
            if found == False and hasattr(i,'nitrogen_ammonium') and api.get_workflow_status_of(i['nitrogen_ammonium']) not in ['retracted','rejected','cancelled','invalid']:
                ammonium = i.nitrogen_ammonium
            elif found == False and hasattr(i,'nitrogen_ammonia') and api.get_workflow_status_of(i.nitrogen_ammonia) not in ['retracted','rejected','cancelled','invalid']:
                ammonium = i.nitrogen_ammonia

            # try:
            #     ammonium = i.sap_nitrogen_as_ammonium
            # except AttributeError:
            #     ammonium = None
            # if ammonium == None:
            #     try:
            #         ammonium = i.liqfert_ammonia
            #     except AttributeError:
            #         ammonium = None

            #Total Sugar
            found = False
            total_sugar = None
            for j in range(20, 0, -1):
                if found==False:
                    sap_version = 'sugars-'+str(j)
                    if hasattr(i,sap_version) and api.get_workflow_status_of(i[sap_version]) not in ['cancelled','invalid','retracted','rejected']:
                        found = True
                        total_sugar = i[sap_version]
            if found == False and hasattr(i,'sugars') and api.get_workflow_status_of(i['sugars']) not in ['retracted','rejected','cancelled','invalid']:
                total_sugar = i.sugars

            # try:
            #     total_sugar = i.sap_total_sugar
            # except AttributeError:
            #     total_sugar = None

            #Chloride
            found = False
            chloride = None
            for j in range(20, 0, -1):
                if found==False:
                    sap_version = 'chloride-'+str(j)
                    if hasattr(i,sap_version) and api.get_workflow_status_of(i[sap_version]) not in ['cancelled','invalid','retracted','rejected']:
                        found = True
                        chloride = i[sap_version]
            if found == False and hasattr(i,'chloride') and api.get_workflow_status_of(i['chloride']) not in ['retracted','rejected','cancelled','invalid']:
                chloride = i.chloride

            # try:
            #     chloride = i.sap_chloride
            # except AttributeError:
            #     chloride = None
            # if chloride is None:
            #     try:
            #         chloride = i.liqfert_chloride
            #     except AttributeError:
            #         chloride = None

            #Nitrate
            found = False
            nitrate = None
            for j in range(20, 0, -1):
                if found==False:
                    sap_version = 'nitrate-'+str(j)
                    if hasattr(i,sap_version) and api.get_workflow_status_of(i[sap_version]) not in ['cancelled','invalid','retracted','rejected']:
                        found = True
                        nitrate = i[sap_version]
            if found == False and hasattr(i,'nitrate') and api.get_workflow_status_of(i['nitrate']) not in ['cancelled','invalid','retracted','rejected']:
                nitrate = i.nitrate

            # try:
            #     nitrate = i.sap_nitrate
            # except AttributeError:
            #     nitrate = None
            # if nitrate is None:
            #     try:
            #         nitrate = i.liqfert_nitrate
            #     except AttributeError:
            #         nitrate = None
            # if nitrate is None:
            #     try:
            #         nitrate = i.drinking_nitrate
            #     except AttributeError:
            #         nitrate = None

            #Nitrite
            found = False
            nitrite = None
            for j in range(20, 0, -1):
                if found==False:
                    drinking_version = 'nitrite-'+str(j)
                    if hasattr(i,drinking_version) and api.get_workflow_status_of(i[drinking_version]) not in ['cancelled','invalid','retracted','rejected']:
                        found = True
                        nitrite = i[drinking_version]
            if found == False and hasattr(i,'nitrite') and api.get_workflow_status_of(i.nitrite) not in ['cancelled','invalid','retracted','rejected']:
                nitrite = i.nitrite


            # try:
            #     nitrite = i.drinking_nitrite
            # except AttributeError:
            #     nitrite = None

            #Nitrogen as Nitrate
            found = False
            n_as_nitrate = None
            for j in range(20, 0, -1):
                if found==False:
                    sap_version = 'nitrogen_nitrate-'+str(j)
                    if hasattr(i,sap_version) and api.get_workflow_status_of(i[sap_version]) not in ['cancelled','invalid','retracted','rejected']:
                        found = True
                        n_as_nitrate = i[sap_version]
            if found == False and hasattr(i,'nitrogen_nitrate') and api.get_workflow_status_of(i['nitrogen_nitrate']) not in ['retracted','rejected','cancelled','invalid']:
                n_as_nitrate = i.nitrogen_nitrate

            #Ammonium
            if ammonium is not None and api.get_workflow_status_of(ammonium) in ['unassigned'] and not filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Test']=='Ammonium')].empty:
                logger.info("Importing Ammonium for {0}: {1}".format(i, ammonium))

                ammonium.Result = unicode(filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Test']=='Ammonium')]['Result'].values[0].strip(), "utf-8")
                logger.info("Result: ".format(ammonium.Result))
		ammonium.AnalysisDateTime = filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Test']=='Ammonium')]['Analysis Date/Time'].values[0]
                ammonium.CustomMethod = nh4_method
                ammonium.reindexObject(idxs=['Result','AnalysisDateTime','CustomMethod'])
                if [j for j in api.get_transitions_for(ammonium) if 'submit' in j.values()]:
                    try:
                        api.do_transition_for(ammonium, "submit")
                    except AttributeError:
                        pass
                if 'Analyst' in filtered_df.columns and not filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Test']=='Ammonium')]['Analyst'].empty:
                    ammonium.Analyst = filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Test']=='Ammonium')]['Analyst'].values[0]
                    ammonium.reindexObject(idxs=['Analyst'])
                imported.append(True)

            if ammonium is not None and api.get_workflow_status_of(ammonium) in ['unassigned'] and not filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Test']=='AMMONIA SP')].empty:
                logger.info("Importing Ammonium for {0}: {1}".format(i, ammonium))
                ammonium.Result = unicode(filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Test']=='AMMONIA SP')]['Result'].values[0].strip(), "utf-8")
                logger.info("Result: ".format(ammonium.Result))
		ammonium.AnalysisDateTime = filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Test']=='AMMONIA SP')]['Analysis Date/Time'].values[0]
                ammonium.CustomMethod = nh4_method
                ammonium.reindexObject(idxs=['Result','AnalysisDateTime','CustomMethod'])
                if [j for j in api.get_transitions_for(ammonium) if 'submit' in j.values()]:
                    try:
                        api.do_transition_for(ammonium, "submit")
                    except AttributeError:
                        pass
                if 'Analyst' in filtered_df.columns and not filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Test']=='AMMONIA SP')]['Analyst'].empty:
                    ammonium.Analyst = filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Test']=='AMMONIA SP')]['Analyst'].values[0]
                    ammonium.reindexObject(idxs=['Analyst'])
                imported.append(True)

            #Total Sugar
            if total_sugar is not None and api.get_workflow_status_of(total_sugar) in ['unassigned'] and not filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Test']=='GluFruSucG')].empty:
                logger.info("Importing Total Sugar for {0}".format(i))
                total_sugar.Result = unicode(filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Test']=='GluFruSucG')]['Result'].values[0].strip(), "utf-8")
                total_sugar.AnalysisDateTime = filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Test']=='GluFruSucG')]['Analysis Date/Time'].values[0]
		total_sugar.CustomMethod = sugar_method
                total_sugar.reindexObject(idxs=['Result','AnalysisDateTime','CustomMethod'])
                if [j for j in api.get_transitions_for(total_sugar) if 'submit' in j.values()]:
                    try:
                        api.do_transition_for(total_sugar, "submit")
                    except AttributeError:
                        pass
                if 'Analyst' in filtered_df.columns and not filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Test']=='GluFruSucG')]['Analyst'].empty:
                    total_sugar.Analyst = filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Test']=='GluFruSucG')]['Analyst'].values[0]
                    total_sugar.reindexObject(idxs=['Analyst'])
                imported.append(True)

            #Chloride
            if chloride is not None and api.get_workflow_status_of(chloride) in ['unassigned'] and not filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Test']=='Chloride')].empty:
                logger.info("Importing Chloride for {0}".format(i))
                chloride.Result = unicode(filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Test']=='Chloride')]['Result'].values[0].strip(), "utf-8")
                chloride.AnalysisDateTime = filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Test']=='Chloride')]['Analysis Date/Time'].values[0]
                chloride.CustomMethod = cl_method
                chloride.reindexObject(idxs=['Result','AnalysisDateTime','CustomMethod'])
                if [j for j in api.get_transitions_for(chloride) if 'submit' in j.values()]:
                    try:
                        api.do_transition_for(chloride, "submit")
                    except AttributeError:
                        pass
                if 'Analyst' in filtered_df.columns and not filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Test']=='Chloride')]['Analyst'].empty:
                    chloride.Analyst = filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Test']=='Chloride')]['Analyst'].values[0]
                    chloride.reindexObject(idxs=['Analyst'])
                imported.append(True)

            #Sulfate
            if sulfate is not None and api.get_workflow_status_of(sulfate) in ['unassigned'] and not filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Test']=='SO4 Low')].empty:
                logger.info("Importing Sulfate for {0}".format(i))
                sulfate.Result = unicode(filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Test']=='SO4 Low')]['Result'].values[0].strip(), "utf-8")
                sulfate.AnalysisDateTime = filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Test']=='SO4 Low')]['Analysis Date/Time'].values[0]
		sulfate.CustomMethod = so4_method
                sulfate.reindexObject(idxs=['Result','AnalysisDateTime','CustomMethod'])
                if [j for j in api.get_transitions_for(sulfate) if 'submit' in j.values()]:
                    print("Submitting")
                    try:
                        api.do_transition_for(sulfate, "submit")
                    except AttributeError:
                        pass
                if 'Analyst' in filtered_df.columns and not filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Test']=='SO4 Low')]['Analyst'].empty:
                    sulfate.Analyst = filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Test']=='SO4 Low')]['Analyst'].values[0]
                    sulfate.reindexObject(idxs=['Analyst'])
                imported.append(True)

            #Nitrogen as Nitrate
            #ADD LOGIC TO HANDLE
            # if SAPNO2 > 0:
            #     SAPNO3 = SAPTON1 - SAPNO2
            # else:
            #     SAPNO3 = SAPTON1

            if n_as_nitrate is not None and api.get_workflow_status_of(n_as_nitrate) in ['unassigned'] and not filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Test']=='SAPTON1S')].empty:
                logger.info("Importing N from Nitrate for {0}. Result is: {1}".format(i,unicode(filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Test']=='SAPTON1S')]['Result'].values[0].strip(), "utf-8")))
                n_as_nitrate.Result = unicode(filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Test']=='SAPTON1S')]['Result'].values[0].strip(), "utf-8")
                n_as_nitrate.AnalysisDateTime = filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Test']=='SAPTON1S')]['Analysis Date/Time'].values[0]
                n_as_nitrate.CustomMethod = no3_method
                n_as_nitrate.reindexObject(idxs=['Result','AnalysisDateTime','CustomMethod'])
                if [j for j in api.get_transitions_for(n_as_nitrate) if 'submit' in j.values()]:
                    try:
                        api.do_transition_for(n_as_nitrate, "submit")
                    except AttributeError:
                        pass
                if 'Analyst' in filtered_df.columns and not filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Test']=='SAPTON1S')]['Analyst'].empty:
                    n_as_nitrate.Analyst = filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Test']=='SAPTON1S')]['Analyst'].values[0]
                    n_as_nitrate.reindexObject(idxs=['Analyst'])
                imported.append(True)
            elif n_as_nitrate is not None and api.get_workflow_status_of(n_as_nitrate) in ['unassigned'] and not filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Test']=='SAPNO3')].empty:
                logger.info("Importing N from Nitrate for {0}. Result is: {1}".format(i,unicode(filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Test']=='SAPNO3')]['Result'].values[0].strip(), "utf-8")))
                n_as_nitrate.Result = unicode(filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Test']=='SAPNO3')]['Result'].values[0].strip(), "utf-8")
                n_as_nitrate.AnalysisDateTime = filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Test']=='SAPNO3')]['Analysis Date/Time'].values[0]
                n_as_nitrate.CustomMethod = no3_method
                n_as_nitrate.reindexObject(idxs=['Result','AnalysisDateTime','CustomMethod'])
                if [j for j in api.get_transitions_for(n_as_nitrate) if 'submit' in j.values()]:
                    try:
                        api.do_transition_for(n_as_nitrate, "submit")
                    except AttributeError:
                        pass
                if 'Analyst' in filtered_df.columns and not filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Test']=='SAPNO3')]['Analyst'].empty:
                    n_as_nitrate.Analyst = filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Test']=='SAPNO3')]['Analyst'].values[0]
                    n_as_nitrate.reindexObject(idxs=['Analyst'])
                imported.append(True)
	    elif n_as_nitrate is not None and api.get_workflow_status_of(n_as_nitrate) in ['unassigned'] and not filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Test']=='SAPTON1')].empty:
                logger.info("Importing N from Nitrate for {0}. Result is: {1}".format(i,unicode(filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Test']=='SAPTON1')]['Result'].values[0].strip(), "utf-8")))
                n_as_nitrate.Result = unicode(filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Test']=='SAPTON1')]['Result'].values[0].strip(), "utf-8")
                n_as_nitrate.AnalysisDateTime = filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Test']=='SAPTON1')]['Analysis Date/Time'].values[0]
                n_as_nitrate.CustomMethod = no3_method
                n_as_nitrate.reindexObject(idxs=['Result','AnalysisDateTime','CustomMethod'])
                if [j for j in api.get_transitions_for(n_as_nitrate) if 'submit' in j.values()]:
                    try:
                        api.do_transition_for(n_as_nitrate, "submit")
                    except AttributeError:
                        pass
                if 'Analyst' in filtered_df.columns and not filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Test']=='SAPTON1')]['Analyst'].empty:
                    n_as_nitrate.Analyst = filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Test']=='SAPTON1')]['Analyst'].values[0]
                    n_as_nitrate.reindexObject(idxs=['Analyst'])
                imported.append(True)

            #Nitrite
            if nitrite is not None and api.get_workflow_status_of(nitrite) in ['unassigned'] and not filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Test']=='SAPNO2')].empty:
                logger.info("Importing Nitrite for {0}".format(i))
                nitrite.Result = unicode(filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Test']=='SAPNO2')]['Result'].values[0].strip(), "utf-8")
                nitrite.AnalysisDateTime = filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Test']=='SAPNO2')]['Analysis Date/Time'].values[0]
                nitrite.reindexObject(idxs=['Result','AnalysisDateTime'])
                if [j for j in api.get_transitions_for(nitrite) if 'submit' in j.values()]:
                    try:
                        api.do_transition_for(nitrite, "submit")
                    except AttributeError:
                        pass
                if 'Analyst' in filtered_df.columns and not filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Test']=='SAPNO2')]['Analyst'].empty:
                    nitrite.Analyst = filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Test']=='SAPNO2')]['Analyst'].values[0]
                    nitrite.reindexObject(idxs=['Analyst'])
                imported.append(True)

            if imported:
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
                        u"Gallery data successfully imported for Samples: "+str(number)
                    )
        else:
            IStatusMessage(self.request).addStatusMessage(
                    u"No .CSV File for Gallery data"
                )

        contextURL = self.context.absolute_url()
        self.request.response.redirect(contextURL)

class pHImportView(edit.DefaultEditForm):

    def __init__(self, context, request):
          self.context = context
          self.request = request

    def saveCSV(self, context, request):
        return context.absolute_url_path()

    def processCSV(self, data):
        """Process the CSV"""
        #Get logger for output messages
        logger = logging.getLogger("Plone")

        ph_method = map(api.get_object, api.search({'portal_type':'Method','title':'AOAC 973.41'}))[0].UID()

        #Convert CSV data to a dataframe
        df = pd.read_csv(StringIO.StringIO(data),keep_default_na=False, dtype=str)
        #Get a list of Unique sample names from the imported DataFrame
        sample_names = df['Sample Name'].unique()
        #Take off the '-001' to get a list of SDG titles to search
        batch_titles = df['Sample Name'].str[:-4].unique().tolist()
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
            if xsdg in batch_dict.keys():
                ars = batch_dict[xsdg]
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

            #pH
            found = False
            ph = None
            for j in range(20, 0, -1):
                if found==False:
                    sap_version = 'ph-'+str(j)
                    if hasattr(i,sap_version) and api.get_workflow_status_of(i[sap_version]) not in ['retracted','rejected','cancelled','invalid']:
                        found = True
                        ph = i[sap_version]
            if found == False and hasattr(i,'ph') and api.get_workflow_status_of(i.ph) not in ['retracted','rejected','cancelled','invalid']:
                ph = i.ph

            # try:
            #     ph = i.sap_ph
            # except AttributeError:
            #     ph = None
            # if ph == None:
            #     try:
            #         ph = i.liqfert_ph
            #     except AttributeError:
            #         ph = None
            logger.info("pH for {0} is {1}".format(i, ph))
            if ph is not None and api.get_workflow_status_of(ph) in ['unassigned']:
                logger.info("pH Clean for {0}".format(i))
                logger.info("Dataframe {0}".format(filtered_df[(filtered_df['Sample Name']==api.get_id(i))]))
                logger.info("Dataframe is: {0}, Sample Name Series is {1}, ID is {2}".format(filtered_df,filtered_df['Sample Name'],api.get_id(i)))
                clean_ids.append(api.get_id(i))
                #pH
                if not filtered_df[(filtered_df['Sample Name']==api.get_id(i))].empty:
                    logger.info("Importing pH for: {0}".format(i))
                    ph.Result = unicode(filtered_df[(filtered_df['Sample Name']==api.get_id(i))]['Result'].values[0].strip(), "utf-8")
                    ph.AnalysisDateTime = filtered_df[(filtered_df['Sample Name']==api.get_id(i))]['Analysis Date/Time'].values[0]
                    ph.CustomMethod = ph_method
                    ph.reindexObject(idxs=['Result','AnalysisDateTime','CustomMethod'])
                    logger.info("{0}".format(api.get_transitions_for(ph)))
                if [j for j in api.get_transitions_for(ph) if 'submit' in j.values()]:
                    try:
                        api.do_transition_for(ph, "submit")
                    except AttributeError:
                        pass
                    if 'Analyst' in filtered_df.columns and not filtered_df[(filtered_df['Sample Name']==api.get_id(i))]['Analyst'].empty:
                        ph.Analyst = filtered_df[(filtered_df['Sample Name']==api.get_id(i))]['Analyst'].values[0]
                        ph.reindexObject(idxs=['Analyst'])

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
                        u"pH data successfully imported for Samples: "+str(number)
                    )
        else:
            IStatusMessage(self.request).addStatusMessage(
                    u"No .CSV File for pH data"
                )

        contextURL = self.context.absolute_url()
        self.request.response.redirect(contextURL)

class ManualImportView(edit.DefaultEditForm):

    def __init__(self, context, request):
          self.context = context
          self.request = request

    def saveCSV(self, context, request):
        return context.absolute_url_path()

    def processCSV(self, data):
        """Process the CSV"""
        #Get logger for output messages
        logger = logging.getLogger("Plone")

        ph_method = map(api.get_object, api.search({'portal_type':'Method','title':'AOAC 973.41'}))[0].UID()
        ec_method = map(api.get_object, api.search({'portal_type':'Method','title':'SM2510B'}))[0].UID()
	brix_method = map(api.get_object, api.search({'portal_type':'Method','title':'AOAC 932.14'}))[0].UID()
	alk_method = map(api.get_object, api.search({'portal_type':'Method','title':'SM2320B'}))[0].UID()

        #Convert CSV data to a dataframe
        df = pd.read_csv(StringIO.StringIO(data),keep_default_na=False, dtype=str)
        #Get a list of Unique sample names from the imported DataFrame
        sample_ids = df['Sample ID'].unique()
	#Check for poorly formatted IDs
	bad_ids = []
	for i in sample_ids:
		if len(i) != 12 or i[-2:].upper() != 'FL':
			bad_ids.append(i)
			df = df[df['Sample ID'] != i]
	print("Invalid Samples are: ".format(bad_ids))
        #Take off the '-001' to get a list of SDG titles to search
        batch_titles = df['Sample ID'].str[:-4].unique().tolist()
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

        for i in sample_ids:
            xsdg = i[:-4]
            ili = i[-3:]
            if xsdg in batch_dict.keys():
                ars = batch_dict[xsdg]
                for j in ars:
                    if (
			api.get_workflow_status_of(j) not in ['retracted','rejected','invalid','cancelled']
		        and (j.InternalLabID == ili
                        or api.get_id(j) == i)
		    ):
                        import_samples.append(j)
                        df.loc[df['Sample ID'] == i,['Sample ID']] = api.get_id(j)

        #Get the list of Senaite Sample IDs that will be imported into.
        ids = map(api.get_id, import_samples)
        logger.info("IDs: {0}".format(ids))

        #Get a filter dataframe for only the samples that exist
        bool_series = df['Sample Name'].isin(ids)
        filtered_df = df[bool_series]
        clean_ids = []
        for i in import_samples:
	    if not filtered_df[(filtered_df['Sample ID']==api.get_id(i))].empty:
		#Analytes
		tests = [
		'ph',
		'ec',
		'solublesalts',
		'dissolved_solids',
		'brix',
		'alkalinity',
		'carbonate',
		'bicarbonate'
		]

		col_dict = {
		'ph':('pH',ph_method),
		'ec':('EC',ec_method),
		'solublesalts':('Soluble Salts',ec_method),
		'dissolved_solids':('Dissolved Solids',ec_method),
		'brix':('Brix',brix_method),
		'alkalinity':('Alkalinity',alk_method),
		'carbonate':('Carbonate',alk_method),
		'bicarbonate':('Bicarbonate',alk_method)
	    	}

            	test_dict = {}
	    	for test in tests:
		    test_dict[test] = None

		for analyte in map(api.get_object,i.getAnalyses()):
		    if api.get_workflow_status_of(analyte) not in ['retracted','rejected','invalid','cancelled']:
		        for test in tests:
			    if analyte.Keyword == test:
			        test_dict[test] = analyte

		for test in tests:
		    if test_dict[test] is not None and api.get_workflow_status_of(test_dict[test]) in ['unassigned']:
                        test_dict[test].Result = unicode(filtered_df[(filtered_df['Sample ID']==api.get_id(i))][col_dict[test][0]].values[0].strip(), "utf-8")
                        test_dict[test].AnalysisDateTime = filtered_df[(filtered_df['Sample Name']==api.get_id(i))]['Analysis Date'].values[0]
                        test_dict[test].CustomMethod = col_dict[test][1]
                        test_dict[test].reindexObject(idxs=['Result','AnalysisDateTime','CustomMethod'])
                if [j for j in api.get_transitions_for(test_dict[test]) if 'submit' in j.values()]:
                    try:
                        api.do_transition_for(test_dict[test], "submit")
                    except AttributeError:
                        pass
                if 'Analyst' in filtered_df.columns and not filtered_df[(filtered_df['Sample ID']==api.get_id(i))]['Analyst'].empty:
                    test_dict[test].Analyst = filtered_df[(filtered_df['Sample ID']==api.get_id(i))]['Analyst'].values[0]
                    test_dict[test].reindexObject(idxs=['Analyst'])

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
                        u"Manually imported data successfully imported for Samples: "+str(number)
                    )
        else:
            IStatusMessage(self.request).addStatusMessage(
                    u"No .CSV File for manual data"
                )

        contextURL = self.context.absolute_url()
        self.request.response.redirect(contextURL)

class ECImportView(edit.DefaultEditForm):

    def __init__(self, context, request):
          self.context = context
          self.request = request

    def saveCSV(self, context, request):
        return context.absolute_url_path()

    def processCSV(self, data):
        """Process the CSV"""
        #Get logger for output messages
        logger = logging.getLogger("Plone")

        #Convert CSV data to a dataframe
        df = pd.read_csv(StringIO.StringIO(data),keep_default_na=False, dtype=str)

        ss_method = map(api.get_object, api.search({'portal_type':'Method','title':'SM2510B'}))[0].UID()
        tds_method = map(api.get_object, api.search({'portal_type':'Method','title':'SM2510B'}))[0].UID()

        #Get a list of Unique sample names from the imported DataFrame
        sample_names = df['Sample Name'].unique()
        #Take off the '-001' to get a list of SDG titles to search
        batch_titles = df['Sample Name'].str[:-4].unique().tolist()
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
            if xsdg in batch_dict.keys():
                ars = batch_dict[xsdg]
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

            imported = []

            found = False
            ec = None
            tds = None

            #EC
            found = False
            ec = None
            for j in range(20, 0, -1):
                if found==False:
                    sap_version = 'ec-'+str(j)
                    liqfert_version = 'soluablesalts-'+str(j)
                    if hasattr(i,sap_version) and api.get_workflow_status_of(i[sap_version]) not in ['retracted','rejected','cancelled','invalid']:
                        found = True
                        ec = i[sap_version]
                    elif hasattr(i,liqfert_version) and api.get_workflow_status_of(i[liqfert_version]) not in ['retracted','rejected','cancelled','invalid']:
                        found = True
                        ec = i[liqfert_version]
            if found == False and hasattr(i,'ec') and api.get_workflow_status_of(i.ec) not in ['retracted','rejected','cancelled','invalid']:
                ec = i.ec
            elif found == False and hasattr(i,'solublesalts') and api.get_workflow_status_of(i.solublesalts) not in ['retracted','rejected','cancelled','invalid']:
                ec = i.solublesalts

            # #Calculations
            found = False
            tds = None
            for j in range(20, 0, -1):
                if found==False:
                    liqfert_version = 'dissolved_solids-'+str(j)
                    if hasattr(i,liqfert_version) and api.get_workflow_status_of(i) not in ['retracted','rejected','cancelled','invalid']:
                        found = True
                        tds = i[liqfert_version]
            if found == False and hasattr(i,'dissolved_solids') and api.get_workflow_status_of(i) not in ['retracted','rejected','cancelled','invalid']:
                tds = i.dissolved_solids

            #EC
            if ec is not None and api.get_workflow_status_of(ec)=='unassigned' and not filtered_df[(filtered_df['Sample Name']==api.get_id(i))].empty:
                logger.info("Importing EC for {0}".format(i))
                ec.Result = unicode(filtered_df[(filtered_df['Sample Name']==api.get_id(i))]['Result'].values[0].strip(), "utf-8")
                ec.AnalysisDateTime = filtered_df[(filtered_df['Sample Name']==api.get_id(i))]['Analysis Date/Time'].values[0]
                ec.CustomMethod = ss_method
                ec.reindexObject(idxs=['Result','AnalysisDateTime','CustomMethod'])
		print("Importing EC For {0}. Result is: {1}".format(i,ec.Result))
		logger.info("{0}".format(api.get_transitions_for(ec)))
                if [j for j in api.get_transitions_for(ec) if 'submit' in j.values()]:
                    try:
                        api.do_transition_for(ec, "submit")
                    except AttributeError:
                        pass
                if 'Analyst' in filtered_df.columns and not filtered_df[(filtered_df['Sample Name']==api.get_id(i))]['Analyst'].empty:
                    ec.Analyst = filtered_df[(filtered_df['Sample Name']==api.get_id(i))]['Analyst'].values[0]
                    ec.reindexObject(idxs=['Analyst'])
                imported.append(True)

            #TDS
            if tds is not None and api.get_workflow_status_of(tds)=='unassigned' and not filtered_df[(filtered_df['Sample Name']==api.get_id(i))].empty:
                logger.info("Caclulation TDS for {0}".format(i))
                ec_text = unicode(filtered_df[(filtered_df['Sample Name']==api.get_id(i))]['Result'].values[0].strip(), "utf-8")
                ec_float = float(ec_text)
                tds.Result = unicode(ec_float*650)
                tds.AnalysisDateTime = filtered_df[(filtered_df['Sample Name']==api.get_id(i))]['Analysis Date/Time'].values[0]
                tds.CustomMethod = ss_method
                tds.reindexObject(idxs=['Result','AnalysisDateTime','CustomMethod'])
                tds = api.do_transition_for(tds, "submit")
                if 'Analyst' in filtered_df.columns and not filtered_df[(filtered_df['Sample Name']==api.get_id(i))]['Analyst'].empty:
                    tds.Analyst = filtered_df[(filtered_df['Sample Name']==api.get_id(i))]['Analyst'].values[0]
                    tds.reindexObject(idxs=['Analyst'])
                imported.append(True)

            if imported:
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
                        u"EC data successfully imported for Samples: "+str(number)
                    )
        else:
            IStatusMessage(self.request).addStatusMessage(
                    u"No .CSV File for EC data"
                )

        contextURL = self.context.absolute_url()
        self.request.response.redirect(contextURL)

class TotalNitrogenImportView(edit.DefaultEditForm):

    def __init__(self, context, request):
          self.context = context
          self.request = request

    def saveCSV(self, context, request):
        return context.absolute_url_path()

    def processCSV(self, data):
        """Process the CSV"""
        #Get logger for output messages
        logger = logging.getLogger("Plone")

        #Convert CSV data to a dataframe
        dirty_df = pd.read_csv(StringIO.StringIO(data),keep_default_na=False, dtype=str)

        n_method = map(api.get_object, api.search({'portal_type':'Method','title':'AOAC 972.43'}))[0].UID()

        #Convert Total Nitrogen CSV to Standard Import CSV format
        sdg = '' #Unnecessary?
        sid = '' #Unnecessary?
        date = '' #Unnecessary?
        zfill = '' #Unnecessary?
        samples = []
        results = []
        dates = []
        analysts = []
        dict_to_df = {}
        for i, row in dirty_df.iterrows():
            if "Name" in row["Name"] or "Comments" in row["Name"]:
                pass
            elif "FL" in row["Name"] or "PT" in row["Name"]:
                sdg = row["Name"]
                date = row["Analysis Date"]
            elif row["Name"].isdigit():
                zfill = row["Name"].zfill(3)
                sid = sdg + '-' + zfill
                samples.append(sid)

                dirty_result = row["Nitrogen Average"] # '1234 ppm'
                # unit = dirty_result[-3:] # 'ppm'
                result = dirty_result[:-4] # '1234'
                results.append(result)

                #Analyst
                if 'Analyst' in row:
                    analysts.append(row['Analyst'])
                else:
                    analysts.append('')

                #Date
                dates.append(date)
            elif row["Name"][:-1].isdigit():
                sid = sdg + '-' + row["Name"]
                samples.append(sid)

                dirty_result = row["Nitrogen Average"] # '1234 ppm'
                # unit = dirty_result[-3:] # 'ppm'
                result = dirty_result[:-4] # '1234'
                results.append(result)

                #Analyst
                if 'Analyst' in row:
                    analysts.append(row['Analyst'])
                else:
                    analysts.append('')

                #Date
                dates.append(date)
            else:
                pass

        dict_to_df['Sample Name'] = samples
        dict_to_df['Result'] = results
        dict_to_df['Analyst'] = analysts
        dict_to_df['Analysis Date/Time'] = dates

        df = pd.DataFrame.from_dict(dict_to_df)

        #Get a list of Unique sample names from the imported DataFrame
        sample_names = df['Sample Name'].unique()
        #Take off the '-001' to get a list of SDG titles to search
        batch_titles = df['Sample Name'].str[:-4].unique().tolist()
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
            if xsdg in batch_dict.keys():
                ars = batch_dict[xsdg]
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

            imported = []

            #Total Nitrogen
            found = False
            total_n = None
            for j in range(20, 0, -1):
                if found==False:
                    sap_version = 'nitrogen-'+str(j)
		    tissue_version = 'nitrogen-'+str(j)
		    hp_version = 'nitrogen-'+str(j)
                    if hasattr(i,sap_version) and api.get_workflow_status_of(i[sap_version]) not in ['rejected','retracted','invalid','cancelled']:
                        found = True
                        total_n = i[sap_version]
            if found == False and hasattr(i,'nitrogen') and api.get_workflow_status_of(i.nitrogen) not in ['retracted','rejected','invalid','cancelled']:
                total_n = i.nitrogen

            if total_n is not None and api.get_workflow_status_of(total_n)=='unassigned':
                clean_ids.append(api.get_id(i))
		print(i)
		print(total_n)
                #Total N
                if 'Analyst' in filtered_df.columns and not filtered_df[(filtered_df['Sample Name']==api.get_id(i))].empty:
                    total_n.Result = unicode(filtered_df[(filtered_df['Sample Name']==api.get_id(i))]['Result'].values[0].strip(), "utf-8")
                    total_n.AnalysisDateTime = filtered_df[(filtered_df['Sample Name']==api.get_id(i))]['Analysis Date/Time'].values[0]
		    total_n.CustomMethod = n_method
                    total_n.reindexObject(idxs=['Result','AnalysisDateTime','CustomMethod'])
                if [j for j in api.get_transitions_for(total_n) if 'submit' in j.values()]:
                    try:
                        api.do_transition_for(total_n, "submit")
                    except AttributeError:
                        pass
                    if 'Analyst' in filtered_df.columns and not filtered_df[(filtered_df['Sample Name']==api.get_id(i))]['Analyst'].empty:
                        total_n.Analyst = filtered_df[(filtered_df['Sample Name']==api.get_id(i))]['Analyst'].values[0]
                        total_n.reindexObject(idxs=['Analyst'])

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
                        u"Total Nitrogen data successfully imported for Samples: "+str(number)
                    )
        else:
            IStatusMessage(self.request).addStatusMessage(
                    u"No .CSV File for Total Nitrogen data"
                )

        contextURL = self.context.absolute_url()
        self.request.response.redirect(contextURL)

class BrixImportView(edit.DefaultEditForm):

    def __init__(self, context, request):
          self.context = context
          self.request = request

    def saveCSV(self, context, request):
        return context.absolute_url_path()

    def processCSV(self, data):
        """Process the CSV"""
        #Get logger for output messages
        logger = logging.getLogger("Plone")

	method = map(api.get_object, api.search({'portal_type':'Method','title':'AOAC 932.14'}))[0].UID()

        #Convert CSV data to a dataframe
        df = pd.read_csv(StringIO.StringIO(data),keep_default_na=False, dtype=str)
        #Get a list of Unique sample names from the imported DataFrame
        sample_names = df['Sample Name'].unique()
        #Take off the '-001' to get a list of SDG titles to search
        batch_titles = df['Sample Name'].str[:-4].unique().tolist()
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
            if xsdg in batch_dict.keys():
                ars = batch_dict[xsdg]
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
            #Brix
            try:
                brix = i.brix
            except AttributeError:
                brix = None

            if brix is not None and api.get_workflow_status_of(brix) in ['unassigned']:
                clean_ids.append(api.get_id(i))
                #Brix
                if 'Analyst' in filtered_df.columns and not filtered_df[(filtered_df['Sample Name']==api.get_id(i))].empty:
                    logger.info("Importing Brix for: ".format(i))
                    brix.Result = unicode(filtered_df[(filtered_df['Sample Name']==api.get_id(i))]['Result'].values[0].strip(), "utf-8")
                    brix.AnalysisDateTime = filtered_df[(filtered_df['Sample Name']==api.get_id(i))]['Analysis Date/Time'].values[0]
		    brix.CustomMethod = method
                    brix.reindexObject(idxs=['Result','AnalysisDateTime','CustomMethod'])
                    if [j for j in api.get_transitions_for(brix) if 'submit' in j.values()]:
                        try:
                            api.do_transition_for(brix, "submit")
                        except AttributeError:
                            pass
                    if 'Analyst' in filtered_df.columns and not filtered_df[(filtered_df['Sample Name']==api.get_id(i))]['Analyst'].empty:
                        brix.Analyst = filtered_df[(filtered_df['Sample Name']==api.get_id(i))]['Analyst'].values[0]
                        brix.reindexObject(idxs=['Analyst'])

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
                        u"Brix data successfully imported for Samples: "+str(number)
                    )
        else:
            IStatusMessage(self.request).addStatusMessage(
                    u"No .CSV File for pH data"
                )

        contextURL = self.context.absolute_url()
        self.request.response.redirect(contextURL)
