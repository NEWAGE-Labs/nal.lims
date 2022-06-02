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
import csv
import StringIO
import codecs
import pandas as pd
import logging
import copy

# class ICPImportAddView(add.DefaultAddForm):
#
#     def __init__(self, context, request):
#           self.context = context
#           self.request = request
#
#     # Buttons
#
#     @button.buttonAndHandler(u'Save', name='save')
#     def handleAdd(self, action):
#         data, errors = self.extractData()
#         if errors:
#             self.status = self.formErrorsMessage
#             return
#
#         # obj = self.createAndAdd(data)
#         # if obj is not None:
#         #     # mark only as finished if we get the new object
#         #     self._finishedAdd = True
#         #     IStatusMessage(self.request).addStatusMessage(
#         #         self.success_message, "info"
#         #     )
#
#     @button.buttonAndHandler(u'Cancel', name='cancel')
#     def handleCancel(self, action):
#         IStatusMessage(self.request).addStatusMessage(
#             u"Add New Item operation cancelled", "info"
#         )
#         self.request.response.redirect(self.nextURL())
#         notify(AddCancelledEvent(self.context))

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

        #Convert CSV data to a dataframe
        df = pd.read_csv(StringIO.StringIO(data),keep_default_na=False, dtype=str)
        #Get a list of Unique sample names from the imported DataFrame
        samples_names = df['Sample Name'].unique()
        #Get a brain of all Samples
        sample_brain = api.search({'portal_type':'AnalysisRequest'})
        #Map the brain to a list of sample objects
        sample_objs = map(api.get_object, sample_brain)
        #Instantiate an empty list to fill with Senaite samples that will be imported into
        import_samples = []
        method = map(api.get_object,api.search({'portal_type':'Method','id':'method-47'}))[0]

        #Get the list of Senaite Sample Objects that have IDs in the CSV
        print(samples_names)
        for i in sample_objs:
            print('Sample {0} is {1}'.format(i,api.get_workflow_status_of(i)))
            if api.get_workflow_status_of(i) not in ['cancelled','invalid']:
                print('VALID - Sample {0}. ID: {1}'.format(i,i.getBatch().title + '-' + i.InternalLabID))

                if api.get_id(i) in samples_names:
                    import_samples.append(i)

                try:
                    sdg = i.getBatch().title
                except AttributeError:
                    print('Failed to get an SDG')
                    pass

                try:
                    labID = i.InternalLabID
                except AttributeError:
                    print('Failed to get an Internal Lab ID')
                    pass

                nal_id = sdg + '-' + labID

                if nal_id in samples_names:
                    print('FOUND - Sample {0}. NAL ID: {1}'.format(i, nal_id))
                    import_samples.append(i)
                    print(nal_id in samples_names)
                    print(df[df['Sample Name'].str.match(nal_id)])
                    df.loc[df['Sample Name'] == nal_id,['Sample Name']] = api.get_id(i)

        #Get the list of Senaite Sample IDs that will be imported into.
        ids = map(api.get_id, import_samples)

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
            sap_kcaratio = None
            calcium_percent = None
            potassium_percent = None
            magnesium_percent = None
            sodium_percent = None



            for j in i:
                if api.get_workflow_status_of(i[j]) not in ['retracted','rejected','invalid','cancelled']:
                    if 'aluminum' in j and 'percent' not in j:
                        aluminum = i[j]
                    if 'arsenic' in j and 'percent' not in j:
                        arsenic = i[j]
                    if 'boron' in j and 'percent' not in j:
                        boron = i[j]
                    if 'calcium' in j and 'percent' not in j:
                        calcium = i[j]
                    if 'cadmium' in j and 'percent' not in j:
                        cadmium = i[j]
                    if 'cobalt' in j and 'percent' not in j:
                        cobalt = i[j]
                    if 'chromium' in j and 'percent' not in j:
                        chromium = i[j]
                    if 'copper' in j and 'percent' not in j:
                        copper = i[j]
                    if 'iron' in j and 'percent' not in j:
                        iron = i[j]
                    if 'lead' in j and 'percent' not in j:
                        lead = i[j]
                    if 'magnesium' in j and 'percent' not in j:
                        magnesium = i[j]
                    if 'manganese' in j and 'percent' not in j:
                        manganese = i[j]
                    if 'molybdenum' in j and 'percent' not in j:
                        molybdenum = i[j]
                    if 'nickel' in j and 'percent' not in j:
                        nickel = i[j]
                    if ('phosphorus' in j or 'phosphorous' in j):
                        phosphorus = i[j]
                    if 'potassium' in j and 'percent' not in j:
                        potassium = i[j]
                    if 'selenium' in j and 'percent' not in j:
                        selenium = i[j]
                    if 'silica' in j and 'percent' not in j:
                        silica = i[j]
                    if 'sodium' in j and 'percent' not in j:
                        sodium = i[j]
                    if 'sulfur' in j and 'percent' not in j:
                        sulfur = i[j]
                    if 'zinc' in j and 'percent' not in j:
                        zinc = i[j]
                    if 'sap_kcaratio' in j and 'percent' not in j:
                        sap_kcaratio = i[j]
                    if 'calcium' in j and 'percent' in j:
                        calcium_percent = i[j]
                    if 'potassium' in j and 'percent' in j:
                        potassium_percent = i[j]
                    if 'magnesium' in j and 'percent' in j:
                        magnesium_percent = i[j]
                    if 'esp' in j or ('sodium' in j and 'percent' in j):
                        sodium_percent = i[j]



        #Aluminum
            if aluminum is not None and api.get_workflow_status_of(aluminum) in ['unassigned'] and not filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Al')].empty:
                print("Importing Aluminum")
                print("Obtaining Result")
                aluminum.Result = unicode(filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Al')]['Formatted Result'].values[0].strip(), "utf-8")
                print("Obtaining Date/Time")
                aluminum.AnalysisDateTime = filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Al')]['Test Date/Time'].values[0]
                aluminum.Method = method
                print("Reindexing Result, Method, and AnalysisDateTime")
                aluminum.reindexObject(idxs=['Result','AnalysisDateTime','Method'])
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
                arsenic.Method = method
                arsenic.reindexObject(idxs=['Result','AnalysisDateTime','Method'])
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
                boron.Method = method
                boron.reindexObject(idxs=['Result','AnalysisDateTime','Method'])
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
                calcium.Method = method
                calcium.reindexObject(idxs=['Result','AnalysisDateTime','Method'])
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
                cadmium.Method = method
                cadmium.reindexObject(idxs=['Result','AnalysisDateTime','Method'])
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
                cobalt.Method = method
                cobalt.reindexObject(idxs=['Result','AnalysisDateTime','Method'])
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
                chromium.Method = method
                chromium.reindexObject(idxs=['Result','AnalysisDateTime','Method'])
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
                copper.Method = method
                copper.reindexObject(idxs=['Result','AnalysisDateTime','Method'])
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
                iron.Method = method
                iron.reindexObject(idxs=['Result','AnalysisDateTime','Method'])
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
                lead.Method = method
                lead.reindexObject(idxs=['Result','AnalysisDateTime','Method'])
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
                magnesium.Method = method
                magnesium.reindexObject(idxs=['Result','AnalysisDateTime','Method'])
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
                manganese.Method = method
                manganese.reindexObject(idxs=['Result','AnalysisDateTime','Method'])
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
                molybdenum.Method = method
                molybdenum.reindexObject(idxs=['Result','AnalysisDateTime','Method'])
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
                nickel.Method = method
                nickel.reindexObject(idxs=['Result','AnalysisDateTime','Method'])
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
                phosphorus.Method = method
                phosphorus.reindexObject(idxs=['Result','AnalysisDateTime','Method'])
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
                potassium.Method = method
                potassium.reindexObject(idxs=['Result','AnalysisDateTime','Method'])
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
                selenium.Method = method
                selenium.reindexObject(idxs=['Result','AnalysisDateTime','Method'])
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
                silica.Method = method
                silica.reindexObject(idxs=['Result','AnalysisDateTime','Method'])
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
                sodium.Method = method
                sodium.reindexObject(idxs=['Result','AnalysisDateTime','Method'])
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
                sulfur.Method = method
                sulfur.reindexObject(idxs=['Result','AnalysisDateTime','Method'])
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
                zinc.Method = method
                zinc.reindexObject(idxs=['Result','AnalysisDateTime','Method'])
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
            if sap_kcaratio is not None and api.get_workflow_status_of(sap_kcaratio) in ['unassigned'] and potassium.Result is not None and calcium.Result is not None:
                print("Importing KCA")
                try:
                    k_float = float(potassium.Result)
                    ca_float = float(calcium.Result)
                    sap_kcaratio.Result = unicode(k_float/ca_float)
                    sap_kcaratio.AnalysisDateTime = potassium.AnalysisDateTime or calcium.AnalysisDateTime
                    sap_kcaratio.reindexObject(idxs=['Result','AnalysisDateTime','Method'])
                    if [j for j in api.get_transitions_for(sap_kcaratio) if 'submit' in j.values()]:
                        try:
                            api.do_transition_for(sap_kcaratio, "submit")
                        except AttributeError:
                            pass
                    sap_kcaratio.Analyst = potassium.Analyst or calcium.Analyst
                    sap_kcaratio.reindexObject(idxs=['Analyst'])
                    imported.append(True)
                except ValueError:
                    print("--FLOAT CONVERSION ERROR--")
                    print("Sample is: {0}".format(i))
                    print("Potassium is: {0}".format(potassium.Result))
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
                    potassium_percent.reindexObject(idxs=['Result','AnalysisDateTime','Method'])
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
                    magnesium_percent.reindexObject(idxs=['Result','AnalysisDateTime','Method'])
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
                    sodium_percent.reindexObject(idxs=['Result','AnalysisDateTime','Method'])
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
                    calcium_percent.reindexObject(idxs=['Result','AnalysisDateTime','Method'])
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


        df = pd.DataFrame.from_dict(dict_to_df)

        #Get a list of Unique sample names from the imported DataFrame
        samples_names = df['Sample Name'].unique()
        #Get a brain of all Samples
        sample_brain = api.search({'portal_type':'AnalysisRequest'})
        #Map the brain to a list of sample objects
        sample_objs = map(api.get_object, sample_brain)
        #Instantiate an empty list to fill with Senaite samples that will be imported into
        import_samples = []

        nh4_method = map(api.get_object, api.search({'portal_type':'Method','id':'method-32'}))[0]
        no3_method = map(api.get_object, api.search({'portal_type':'Method','id':'method-33'}))[0]
        cl_method = map(api.get_object, api.search({'portal_type':'Method','id':'method-35'}))[0]

        #Get the list of Senaite Sample Objects that have IDs in the CSV
        for i in sample_objs:

            if api.get_workflow_status_of(i) not in ['cancelled','invalid']:

                if api.get_id(i) in samples_names:
                    import_samples.append(i)

                try:
                    sdg = i.getBatch().title
                except AttributeError:
                    pass

                try:
                    labID = i.InternalLabID
                except AttributeError:
                    pass

                nal_id = sdg + '-' + labID
                if nal_id in samples_names:
                    import_samples.append(i)
                    df.loc[df['Sample Name'] == nal_id,['Sample Name']] = api.get_id(i)

        #Get the list of Senaite Sample IDs that will be imported into.
        ids = map(api.get_id, import_samples)
        logger.info("IDs: {0}".format(ids))

        #Get a filter dataframe for only the samples that exist
        bool_series = df['Sample Name'].isin(ids)
        filtered_df = df[bool_series]

        clean_ids = []

        for i in import_samples:

            imported = []

            #Ammonium
            found = False
            ammonium = None
            for j in range(20, 0, -1):
                if found==False:
                    sap_version = 'sap_nitrogen_as_ammonium-'+str(j)
                    liqfert_version = 'liqfert_ammonia-'+str(j)
                    rs_version = 'rapid_soil_ammonia-'+str(j)
                    if hasattr(i,sap_version):
                        found = True
                        ammonium = i[sap_version]
                    elif hasattr(i,liqfert_version):
                        found = True
                        ammonium = i[liqfert_version]
                    elif hasattr(i,rs_version):
                        found = True
                        ammonium = i[rs_version]
            if found == False and hasattr(i,'sap_nitrogen_as_ammonium') and api.get_workflow_status_of(i.sap_nitrogen_as_ammonium) not in ['retracted','rejected','cancelled','invalid']:
                ammonium = i.sap_nitrogen_as_ammonium
            elif found == False and hasattr(i,'liqfert_ammonia') and api.get_workflow_status_of(i.liqfert_ammonia) not in ['retracted','rejected','cancelled','invalid']:
                ammonium = i.liqfert_ammonia
            elif found == False and hasattr(i,'rapid_soil_ammonia') and api.get_workflow_status_of(i.rapid_soil_ammonia) not in ['retracted','rejected','cancelled','invalid']:
                ammonium = i.rapid_soil_ammonia

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
                    sap_version = 'sap_total_sugar-'+str(j)
                    if hasattr(i,sap_version):
                        found = True
                        total_sugar = i[sap_version]
            if found == False and hasattr(i,'sap_total_sugar') and api.get_workflow_status_of(i.sap_total_sugar) not in ['retracted','rejected','cancelled','invalid']:
                total_sugar = i.sap_total_sugar

            # try:
            #     total_sugar = i.sap_total_sugar
            # except AttributeError:
            #     total_sugar = None

            #Chloride
            found = False
            chloride = None
            for j in range(20, 0, -1):
                if found==False:
                    sap_version = 'sap_chloride-'+str(j)
                    liqfert_version = 'liqfert_chloride-'+str(j)
                    rs_version = 'rapid_soil_chloride-'+str(j)
                    if hasattr(i,sap_version):
                        found = True
                        chloride = i[sap_version]
                    elif hasattr(i,liqfert_version):
                        found = True
                        chloride = i[liqfert_version]
                    elif hasattr(i,rs_version):
                        found = True
                        chloride = i[rs_version]
            if found == False and hasattr(i,'sap_chloride') and api.get_workflow_status_of(i.sap_chloride) not in ['retracted','rejected','cancelled','invalid']:
                chloride = i.sap_chloride
            elif found == False and hasattr(i,'liqfert_chloride') and api.get_workflow_status_of(i.liqfert_chloride) not in ['retracted','rejected','cancelled','invalid']:
                chloride = i.liqfert_chloride
            elif found == False and hasattr(i,'rapid_soil_chloride') and api.get_workflow_status_of(i.rapid_soil_chloride) not in ['retracted','rejected','cancelled','invalid']:
                chloride = i.rapid_soil_chloride

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
                    sap_version = 'sap_nitrate-'+str(j)
                    # liqfert_version = 'liqfert_nitrate-'+str(j)
                    drinking_version = 'drinking_nitrate-'+str(j)
                    if hasattr(i,sap_version):
                        found = True
                        nitrate = i[sap_version]
                    # elif hasattr(i,liqfert_version):
                    #     found = True
                    #     nitrate = i[liqfert_version]
                    elif hasattr(i,drinking_version):
                        found = True
                        nitrate = i[drinking_version]
            if found == False and hasattr(i,'sap_nitrate'):
                nitrate = i.sap_nitrate
            # elif found == False and hasattr(i,'liqfert_nitrate'):
            #     nitrate = i.liqfert_nitrate
            elif found == False and hasattr(i,'drinking_nitrate'):
                nitrate = i.drinking_nitrate

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
                    drinking_version = 'drinking_nitrite-'+str(j)
                    if hasattr(i,drinking_version):
                        found = True
                        nitrite = i[drinking_version]
            if found == False and hasattr(i,'drinking_nitrite'):
                nitrite = i.drinking_nitrite


            # try:
            #     nitrite = i.drinking_nitrite
            # except AttributeError:
            #     nitrite = None

            #Nitrogen as Nitrate
            found = False
            n_as_nitrate = None
            for j in range(20, 0, -1):
                if found==False:
                    sap_version = 'sap_nitrogen_as_nitrate-'+str(j)
                    liqfert_version = 'liqfert_nitrate-'+str(j)
                    drinking_version = 'drinking_nitrogen_as_nitrate-'+str(j)
                    rs_version = 'rapid_soil_nitrate-'+str(j)
                    if hasattr(i,sap_version):
                        found = True
                        n_as_nitrate = i[sap_version]
                    elif hasattr(i,liqfert_version):
                        found = True
                        n_as_nitrate = i[liqfert_version]
                    elif hasattr(i,drinking_version):
                        found = True
                        n_as_nitrate = i[drinking_version]
                    elif hasattr(i,rs_version):
                        found = True
                        n_as_nitrate = i[rs_version]
            if found == False and hasattr(i,'sap_nitrogen_as_nitrate') and api.get_workflow_status_of(i.sap_nitrogen_as_nitrate) not in ['retracted','rejected','cancelled','invalid']:
                n_as_nitrate = i.sap_nitrogen_as_nitrate
            elif found == False and hasattr(i,'liqfert_nitrate') and api.get_workflow_status_of(i.liqfert_nitrate) not in ['retracted','rejected','cancelled','invalid']:
                n_as_nitrate = i.liqfert_nitrate
            elif found == False and hasattr(i,'drinking_nitrogen_as_nitrate') and api.get_workflow_status_of(i.drinking_nitrogen_as_nitrate) not in ['retracted','rejected','cancelled','invalid']:
                n_as_nitrate = i.drinking_nitrogen_as_nitrate
            elif found == False and hasattr(i,'rapid_soil_nitrate') and api.get_workflow_status_of(i.rapid_soil_nitrate) not in ['retracted','rejected','cancelled','invalid']:
                n_as_nitrate = i.rapid_soil_nitrate

            # try:
            #     n_as_nitrate = i.sap_nitrogen_as_nitrate
            # except AttributeError:
            #     n_as_nitrate = None

            # #Total Organic Nitrogen
            # try:
            #     total_n = i.sap_total_nitrogen
            # except AttributeError:
            #     total_n = None
            #
            # #Fructose
            # try:
            #     total_n = i.sap_total_nitrogen
            # except AttributeError:
            #     total_n = None
            #
            # #Glucose
            # try:
            #     total_n = i.sap_total_nitrogen
            # except AttributeError:
            #     total_n = None

            #Ammonium
            if ammonium is not None and api.get_workflow_status_of(ammonium) in ['unassigned'] and not filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Test']=='Ammonium')].empty:
                logger.info("Importing Ammonium for {0}: {1}".format(i, ammonium))
                ammonium.Result = unicode(filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Test']=='Ammonium')]['Result'].values[0].strip(), "utf-8")
                ammonium.AnalysisDateTime = filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Test']=='Ammonium')]['Analysis Date/Time'].values[0]
                ammonium.Method = nh4_method
                ammonium.reindexObject(idxs=['Result','AnalysisDateTime','Method'])
                ammonium = api.do_transition_for(ammonium, "submit")
                if 'Analyst' in filtered_df.columns and not filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Test']=='Ammonium')]['Analyst'].empty:
                    ammonium.Analyst = filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Test']=='Ammonium')]['Analyst'].values[0]
                    ammonium.reindexObject(idxs=['Analyst'])
                imported.append(True)

            if ammonium is not None and api.get_workflow_status_of(ammonium) in ['unassigned'] and not filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Test']=='AMMONIA SP')].empty:
                logger.info("Importing Ammonium for {0}: {1}".format(i, ammonium))
                ammonium.Result = unicode(filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Test']=='AMMONIA SP')]['Result'].values[0].strip(), "utf-8")
                ammonium.AnalysisDateTime = filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Test']=='AMMONIA SP')]['Analysis Date/Time'].values[0]
                ammonium.Method = nh4_method
                ammonium.reindexObject(idxs=['Result','AnalysisDateTime','Method'])
                ammonium = api.do_transition_for(ammonium, "submit")
                if 'Analyst' in filtered_df.columns and not filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Test']=='AMMONIA SP')]['Analyst'].empty:
                    ammonium.Analyst = filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Test']=='AMMONIA SP')]['Analyst'].values[0]
                    ammonium.reindexObject(idxs=['Analyst'])
                imported.append(True)

            #Total Sugar
            if total_sugar is not None and api.get_workflow_status_of(total_sugar) in ['unassigned'] and not filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Test']=='GluFruSucG')].empty:
                logger.info("Importing Total Sugar for {0}".format(i))
                total_sugar.Result = unicode(filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Test']=='GluFruSucG')]['Result'].values[0].strip(), "utf-8")
                total_sugar.AnalysisDateTime = filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Test']=='GluFruSucG')]['Analysis Date/Time'].values[0]
                total_sugar.reindexObject(idxs=['Result','AnalysisDateTime'])
                total_sugar = api.do_transition_for(total_sugar, "submit")
                if 'Analyst' in filtered_df.columns and not filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Test']=='GluFruSucG')]['Analyst'].empty:
                    total_sugar.Analyst = filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Test']=='GluFruSucG')]['Analyst'].values[0]
                    total_sugar.reindexObject(idxs=['Analyst'])
                imported.append(True)

            #Chloride
            if chloride is not None and api.get_workflow_status_of(chloride) in ['unassigned'] and not filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Test']=='Chloride')].empty:
                logger.info("Importing Chloride for {0}".format(i))
                chloride.Result = unicode(filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Test']=='Chloride')]['Result'].values[0].strip(), "utf-8")
                chloride.AnalysisDateTime = filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Test']=='Chloride')]['Analysis Date/Time'].values[0]
                chloride.Method = cl_method
                chloride.reindexObject(idxs=['Result','AnalysisDateTime','Method'])
                chloride = api.do_transition_for(chloride, "submit")
                if 'Analyst' in filtered_df.columns and not filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Test']=='Chloride')]['Analyst'].empty:
                    chloride.Analyst = filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Test']=='Chloride')]['Analyst'].values[0]
                    chloride.reindexObject(idxs=['Analyst'])
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
                n_as_nitrate.Method = no3_method
                n_as_nitrate.reindexObject(idxs=['Result','AnalysisDateTime','Method'])
                n_as_nitrate = api.do_transition_for(n_as_nitrate, "submit")
                if 'Analyst' in filtered_df.columns and not filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Test']=='SAPTON1S')]['Analyst'].empty:
                    n_as_nitrate.Analyst = filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Test']=='SAPTON1S')]['Analyst'].values[0]
                    n_as_nitrate.reindexObject(idxs=['Analyst'])
                imported.append(True)
            elif n_as_nitrate is not None and api.get_workflow_status_of(n_as_nitrate) in ['unassigned'] and not filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Test']=='SAPNO3')].empty:
                logger.info("Importing N from Nitrate for {0}. Result is: {1}".format(i,unicode(filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Test']=='SAPNO3')]['Result'].values[0].strip(), "utf-8")))
                n_as_nitrate.Result = unicode(filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Test']=='SAPNO3')]['Result'].values[0].strip(), "utf-8")
                n_as_nitrate.AnalysisDateTime = filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Test']=='SAPNO3')]['Analysis Date/Time'].values[0]
                n_as_nitrate.Method = no3_method
                n_as_nitrate.reindexObject(idxs=['Result','AnalysisDateTime','Method'])
                n_as_nitrate = api.do_transition_for(n_as_nitrate, "submit")
                if 'Analyst' in filtered_df.columns and not filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Test']=='SAPNO3')]['Analyst'].empty:
                    n_as_nitrate.Analyst = filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Test']=='SAPNO3')]['Analyst'].values[0]
                    n_as_nitrate.reindexObject(idxs=['Analyst'])
                imported.append(True)

            #Nitrite
            if nitrite is not None and api.get_workflow_status_of(nitrite) in ['unassigned'] and not filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Test']=='SAPNO2')].empty:
                logger.info("Importing Nitrite for {0}".format(i))
                nitrite.Result = unicode(filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Test']=='SAPNO2')]['Result'].values[0].strip(), "utf-8")
                nitrite.AnalysisDateTime = filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Test']=='SAPNO2')]['Analysis Date/Time'].values[0]
                nitrite.reindexObject(idxs=['Result','AnalysisDateTime'])
                nitrite = api.do_transition_for(nitrite, "submit")
                if 'Analyst' in filtered_df.columns and not filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Test']=='SAPNO2')]['Analyst'].empty:
                    nitrite.Analyst = filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Test']=='SAPNO2')]['Analyst'].values[0]
                    nitrite.reindexObject(idxs=['Analyst'])
                imported.append(True)

            if imported:
                clean_ids.append(api.get_id(i))

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

        #Convert CSV data to a dataframe
        df = pd.read_csv(StringIO.StringIO(data),keep_default_na=False, dtype=str)
        #Get a list of Unique sample names from the imported DataFrame
        samples_names = df['Sample Name'].unique()
        #Get a brain of all Samples
        sample_brain = api.search({'portal_type':'AnalysisRequest'})
        #Map the brain to a list of sample objects
        sample_objs = map(api.get_object, sample_brain)
        #Instantiate an empty list to fill with Senaite samples that will be imported into
        import_samples = []

        ph_method = map(api.get_object, api.search({'portal_type':'Method','id':'method-22'}))[0]

        #Get the list of Senaite Sample Objects that have IDs in the CSV
        for i in sample_objs:

            if api.get_workflow_status_of(i) not in ['cancelled','invalid']:

                if api.get_id(i) in samples_names:
                    import_samples.append(i)

                try:
                    sdg = i.getBatch().title
                except AttributeError:
                    pass

                try:
                    labID = i.InternalLabID
                except AttributeError:
                    pass

                nal_id = sdg + '-' + labID
                if nal_id in samples_names:
                    import_samples.append(i)
                    df.loc[df['Sample Name'] == nal_id,['Sample Name']] = api.get_id(i)

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
                    sap_version = 'sap_ph-'+str(j)
                    liqfert_version = 'liqfert_ph-'+str(j)
                    rs_version = 'rapid_soil_ph-'+str(j)
                    if hasattr(i,sap_version) and api.get_workflow_status_of(i) not in ['retracted','rejected','cancelled','invalid']:
                        found = True
                        ph = i[sap_version]
                    elif hasattr(i,liqfert_version) and api.get_workflow_status_of(i) not in ['retracted','rejected','cancelled','invalid']:
                        found = True
                        ph = i[liqfert_version]
                    elif hasattr(i,rs_version) and api.get_workflow_status_of(i) not in ['retracted','rejected','cancelled','invalid']:
                        found = True
                        ph = i[rs_version]
            if found == False and hasattr(i,'sap_ph') and api.get_workflow_status_of(i) not in ['retracted','rejected','cancelled','invalid']:
                ph = i.sap_ph
            elif found == False and hasattr(i,'liqfert_ph') and api.get_workflow_status_of(i) not in ['retracted','rejected','cancelled','invalid']:
                ph = i.liqfert_ph
            elif found == False and hasattr(i,'rapid_soil_ph') and api.get_workflow_status_of(i) not in ['retracted','rejected','cancelled','invalid']:
                ph = i.rapid_soil_ph

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
                    ph.Method = ph_method
                    ph.reindexObject(idxs=['Result','AnalysisDateTime','Method'])
                    logger.info("{0}".format(api.get_transitions_for(ph)))
                    ph = api.do_transition_for(ph, "submit")
                    if 'Analyst' in filtered_df.columns and not filtered_df[(filtered_df['Sample Name']==api.get_id(i))]['Analyst'].empty:
                        ph.Analyst = filtered_df[(filtered_df['Sample Name']==api.get_id(i))]['Analyst'].values[0]
                        ph.reindexObject(idxs=['Analyst'])

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
        #Get a list of Unique sample names from the imported DataFrame
        samples_names = df['Sample Name'].unique()
        #Get a brain of all Samples
        sample_brain = api.search({'portal_type':'AnalysisRequest'})
        #Map the brain to a list of sample objects
        sample_objs = map(api.get_object, sample_brain)
        #Instantiate an empty list to fill with Senaite samples that will be imported into
        import_samples = []

        ss_method = map(api.get_object, api.search({'portal_type':'Method','id':'method-28'}))[0]
        tds_method = map(api.get_object, api.search({'portal_type':'Method','id':'method-29'}))[0]

        #Get the list of Senaite Sample Objects that have IDs in the CSV
        for i in sample_objs:

            if api.get_workflow_status_of(i) not in ['cancelled','invalid']:

                if api.get_id(i) in samples_names:
                    import_samples.append(i)

                try:
                    sdg = i.getBatch().title
                except AttributeError:
                    pass

                try:
                    labID = i.InternalLabID
                except AttributeError:
                    pass

                nal_id = sdg + '-' + labID
                if nal_id in samples_names:
                    import_samples.append(i)
                    df.loc[df['Sample Name'] == nal_id,['Sample Name']] = api.get_id(i)


        #Get the list of Senaite Sample IDs that will be imported into.
        ids = map(api.get_id, import_samples)

        #Get a filter dataframe for only the samples that exist
        bool_series = df['Sample Name'].isin(ids)
        filtered_df = df[bool_series]

        clean_ids = []
        for i in import_samples:

            imported = []

            found = False
            ec = None
            tds = None

           # for j in i:
               # if api.get_workflow_status_of(i[j]) not in ['retracted','rejected','invalid','cancelled']:
                   # if 'ec' in j or ('soluable' in j and 'salt' in j):
                   #     ec = i[j]
                  #  if 'tds' in j:
                 #       tds = i[j]

            #EC
            found = False
            ec = None
            for j in range(20, 0, -1):
                if found==False:
                    sap_version = 'sap_ec-'+str(j)
                    liqfert_version = 'liqfert_soluablesalts-'+str(j)
                    rs_version = 'rapid_soil_ec-'+str(j)
                    if hasattr(i,sap_version) and api.get_workflow_status_of(i[sap_version]) not in ['retracted','rejected','cancelled','invalid']:
                        found = True
                        ec = i[sap_version]
                    elif hasattr(i,liqfert_version) and api.get_workflow_status_of(i[liqfert_version]) not in ['retracted','rejected','cancelled','invalid']:
                        found = True
                        ec = i[liqfert_version]
                    elif hasattr(i,rs_version) and api.get_workflow_status_of(i[rs_version]) not in ['retracted','rejected','cancelled','invalid']:
                        found = True
                        ec = i[rs_version]
            if found == False and hasattr(i,'sap_ec') and api.get_workflow_status_of(i) not in ['retracted','rejected','cancelled','invalid']:
                ec = i.sap_ec
            elif found == False and hasattr(i,'liqfert_soluablesalts') and api.get_workflow_status_of(i) not in ['retracted','rejected','cancelled','invalid']:
                ec = i.liqfert_soluablesalts
            elif found == False and hasattr(i,'rapid_soil_ec') and api.get_workflow_status_of(i) not in ['retracted','rejected','cancelled','invalid']:
                ec = i.rapid_soil_ec
           
            # #Calculations
            found = False
            tds = None
            for j in range(20, 0, -1):
                if found==False:
                    liqfert_version = 'liqfert_tds-'+str(j)
                    if hasattr(i,liqfert_version) and api.get_workflow_status_of(i) not in ['retracted','rejected','cancelled','invalid']:
                        found = True
                        tds = i[liqfert_version]
            if found == False and hasattr(i,'liqfert_tds') and api.get_workflow_status_of(i) not in ['retracted','rejected','cancelled','invalid']:
                tds = i.liqfert_tds

            #EC
            if ec is not None and api.get_workflow_status_of(ec)=='unassigned' and not filtered_df[(filtered_df['Sample Name']==api.get_id(i))].empty:
                logger.info("Importing EC for {0}".format(i))
                ec.Result = unicode(filtered_df[(filtered_df['Sample Name']==api.get_id(i))]['Result'].values[0].strip(), "utf-8")
                ec.AnalysisDateTime = filtered_df[(filtered_df['Sample Name']==api.get_id(i))]['Analysis Date/Time'].values[0]
                ec.Method = ss_method
                ec.reindexObject(idxs=['Result','AnalysisDateTime','Method'])
		print("Importing EC For {0}. Result is: {1}".format(i,ec.Result))
		logger.info("{0}".format(api.get_transitions_for(ec)))
                ec = api.do_transition_for(ec, "submit")
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
                tds.Method = ss_method
                tds.reindexObject(idxs=['Result','AnalysisDateTime','Method'])
                tds = api.do_transition_for(tds, "submit")
                if 'Analyst' in filtered_df.columns and not filtered_df[(filtered_df['Sample Name']==api.get_id(i))]['Analyst'].empty:
                    tds.Analyst = filtered_df[(filtered_df['Sample Name']==api.get_id(i))]['Analyst'].values[0]
                    tds.reindexObject(idxs=['Analyst'])
                imported.append(True)

            if imported:
                clean_ids.append(api.get_id(i))

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
            elif "FL" in row["Name"]:
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
        samples_names = df['Sample Name'].unique()
        #Get a brain of all Samples
        sample_brain = api.search({'portal_type':'AnalysisRequest'})
        #Map the brain to a list of sample objects
        sample_objs = map(api.get_object, sample_brain)
        #Instantiate an empty list to fill with Senaite samples that will be imported into
        import_samples = []

        #Get the list of Senaite Sample Objects that have IDs in the CSV
        for i in sample_objs:

            if api.get_workflow_status_of(i) not in ['retracted','rejected','invalid','cancelled']:

                if api.get_id(i) in samples_names:
                    import_samples.append(i)

                try:
                    sdg = i.getBatch().title
                except AttributeError:
                    pass

                try:
                    labID = i.InternalLabID
                except AttributeError:
                    pass

                nal_id = sdg + '-' + labID
                if nal_id in samples_names:
                    import_samples.append(i)
                    df.loc[df['Sample Name'] == nal_id,['Sample Name']] = api.get_id(i)

        #Get the list of Senaite Sample IDs that will be imported into.
        ids = map(api.get_id, import_samples)

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
                    sap_version = 'sap_total_nitrogen-'+str(j)
                    if hasattr(i,sap_version):
                        found = True
                        total_n = i[sap_version]
            if found == False and hasattr(i,'sap_total_nitrogen') and api.get_workflow_status_of(i.sap_total_nitrogen) not in ['retracted','rejected','invalid','cancelled']:
                total_n = i.sap_total_nitrogen

            if total_n is not None and api.get_workflow_status_of(total_n)=='unassigned':
                clean_ids.append(api.get_id(i))
                #Total N
                if 'Analyst' in filtered_df.columns and not filtered_df[(filtered_df['Sample Name']==api.get_id(i))].empty:
                    total_n.Result = unicode(filtered_df[(filtered_df['Sample Name']==api.get_id(i))]['Result'].values[0].strip(), "utf-8")
                    total_n.AnalysisDateTime = filtered_df[(filtered_df['Sample Name']==api.get_id(i))]['Analysis Date/Time'].values[0]
                    total_n.reindexObject(idxs=['Result','AnalysisDateTime'])
                    total_n = api.do_transition_for(total_n, "submit")
                    if 'Analyst' in filtered_df.columns and not filtered_df[(filtered_df['Sample Name']==api.get_id(i))]['Analyst'].empty:
                        total_n.Analyst = filtered_df[(filtered_df['Sample Name']==api.get_id(i))]['Analyst'].values[0]
                        total_n.reindexObject(idxs=['Analyst'])

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

        #Convert CSV data to a dataframe
        df = pd.read_csv(StringIO.StringIO(data),keep_default_na=False, dtype=str)
        #Get a list of Unique sample names from the imported DataFrame
        samples_names = df['Sample Name'].unique()
        #Get a brain of all Samples
        sample_brain = api.search({'portal_type':'AnalysisRequest'})
        #Map the brain to a list of sample objects
        sample_objs = map(api.get_object, sample_brain)
        #Instantiate an empty list to fill with Senaite samples that will be imported into
        import_samples = []

        #Get the list of Senaite Sample Objects that have IDs in the CSV
        for i in sample_objs:

            if api.get_workflow_status_of(i) not in ['cancelled','invalid']:

                if api.get_id(i) in samples_names:
                    import_samples.append(i)

                try:
                    sdg = i.getBatch().title
                except AttributeError:
                    pass

                try:
                    labID = i.InternalLabID
                except AttributeError:
                    pass

                nal_id = sdg + '-' + labID
                if nal_id in samples_names:
                    import_samples.append(i)
                    df.loc[df['Sample Name'] == nal_id,['Sample Name']] = api.get_id(i)

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
                brix = i.sap_brix
            except AttributeError:
                brix = None

            if brix is not None and api.get_workflow_status_of(brix) in ['unassigned']:
                clean_ids.append(api.get_id(i))
                #Brix
                if 'Analyst' in filtered_df.columns and not filtered_df[(filtered_df['Sample Name']==api.get_id(i))].empty:
                    logger.info("Importing Brix for: ".format(i))
                    brix.Result = unicode(filtered_df[(filtered_df['Sample Name']==api.get_id(i))]['Result'].values[0].strip(), "utf-8")
                    brix.AnalysisDateTime = filtered_df[(filtered_df['Sample Name']==api.get_id(i))]['Analysis Date/Time'].values[0]
                    brix.reindexObject(idxs=['Result','AnalysisDateTime'])
                    brix = api.do_transition_for(brix, "submit")
                    if 'Analyst' in filtered_df.columns and not filtered_df[(filtered_df['Sample Name']==api.get_id(i))]['Analyst'].empty:
                        brix.Analyst = filtered_df[(filtered_df['Sample Name']==api.get_id(i))]['Analyst'].values[0]
                        brix.reindexObject(idxs=['Analyst'])

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
