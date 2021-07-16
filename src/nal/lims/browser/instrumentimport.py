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
            #Aluminum
            try:
                aluminum = i.sap_aluminum
            except AttributeError:
                aluminum = None
            if aluminum == None:
                try:
                    aluminum = i.hydro_aluminum
                except AttributeError:
                    aluminum = None
            #Boron
            try:
                boron = i.sap_boron
            except AttributeError:
                boron = None
            if boron == None:
                try:
                    boron = i.hydro_boron
                except AttributeError:
                    boron = None
            #Calcium
            try:
                calcium = i.sap_calcium
            except AttributeError:
                calcium = None
            if calcium == None:
                try:
                    calcium = i.hydro_calcium
                except AttributeError:
                    calcium = None
            #Cobalt
            try:
                cobalt = i.sap_cobalt
            except AttributeError:
                cobalt = None
            if cobalt == None:
                try:
                    cobalt = i.hydro_cobalt
                except AttributeError:
                    cobalt = None
            #Copper
            ##Sap
            try:
                copper = i.sap_copper
            except AttributeError:
                copper = None
            ##Liquid Fertilizer
            if copper == None:
                try:
                    copper = i.hydro_copper
                except AttributeError:
                    copper = None
            ##Drinking Water
            if copper == None:
                try:
                    copper = i.drinking_copper
                except AttributeError:
                    copper = None
            #Iron
            try:
                iron = i.sap_iron
            except AttributeError:
                iron = None
            if iron == None:
                try:
                    iron = i.hydro_iron
                except AttributeError:
                    iron = None
            #Lead
            try:
                lead = i.drinking_lead
            except AttributeError:
                lead = None
            #Magnesium
            try:
                magnesium = i.sap_magnesium
            except AttributeError:
                magnesium = None
            if magnesium == None:
                try:
                    magnesium = i.hydro_magnesium
                except AttributeError:
                    magnesium = None
            #Manganese
            try:
                manganese = i.sap_manganese
            except AttributeError:
                manganese = None
            if manganese == None:
                try:
                    manganese = i.hydro_manganese
                except AttributeError:
                    manganese = None
            #Molybdenum
            try:
                molybdenum = i.sap_molybdenum
            except AttributeError:
                molybdenum = None
            if molybdenum == None:
                try:
                    molybdenum = i.hydro_molybdenum
                except AttributeError:
                    molybdenum = None
            #Nickel
            try:
                nickel = i.sap_nickel
            except AttributeError:
                nickel = None
            if nickel == None:
                try:
                    nickel = i.hydro_nickel
                except AttributeError:
                    nickel = None
            #Phosphorous
            try:
                phosphorous = i.sap_phosphorous
            except AttributeError:
                phosphorous = None
            if phosphorous == None:
                try:
                    phosphorous = i.hydro_phosphorous
                except AttributeError:
                    phosphorous = None
            #Potassium
            try:
                potassium = i.sap_potassium
            except AttributeError:
                potassium = None
            if potassium == None:
                try:
                    potassium = i.hydro_potassium
                except AttributeError:
                    potassium = None
            #Selenium
            try:
                selenium = i.sap_selenium
            except AttributeError:
                selenium = None
            if selenium == None:
                try:
                    selenium = i.hydro_selenium
                except AttributeError:
                    selenium = None
            #Silica
            try:
                silica = i.sap_silica
            except AttributeError:
                silica = None
            if silica == None:
                try:
                    silica = i.hydro_silica
                except AttributeError:
                    silica = None
            #Sodium
            try:
                sodium = i.sap_sodium
            except AttributeError:
                sodium = None
            if sodium == None:
                try:
                    sodium = i.hydro_sodium
                except AttributeError:
                    sodium = None
            #Sulfur
            try:
                sulfur = i.sap_sulfur
            except AttributeError:
                sulfur = None
            if sulfur == None:
                try:
                    sulfur = i.hydro_sulfur
                except AttributeError:
                    sulfur = None
            #Zinc
            try:
                zinc = i.sap_zinc
            except AttributeError:
                zinc = None
            if zinc == None:
                try:
                    zinc = i.hydro_zinc
                except AttributeError:
                    zinc = None

            #Calculations
            try:
                sap_kcaratio = i.sap_kcaratio
            except AttributeError:
                sap_kcaratio = None

        #Aluminum
            if aluminum is not None and api.get_workflow_status_of(aluminum) in ['unassigned','retracted'] and not filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Al')].empty:
                aluminum.Result = unicode(filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Al')]['Formatted Result'].values[0].strip(), "utf-8")
                aluminum.AnalysisDateTime = filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Al')]['Test Date/Time'].values[0]
                aluminum.reindexObject(idxs=['Result','AnalysisDateTime'])
                aluminum = api.do_transition_for(aluminum, "submit")
                if 'Analyst' in filtered_df.columns and not filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Al')]['Analyst'].empty:
                    aluminum.Analyst = filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Al')]['Analyst'].values[0]
                    aluminum.reindexObject(idxs=['Analyst'])
                imported.append(True)
        #Boron
            if boron is not None and api.get_workflow_status_of(boron) in ['unassigned','retracted'] and not filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='B')].empty:
                boron.Result = unicode(filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='B')]['Formatted Result'].values[0].strip(), "utf-8")
                boron.AnalysisDateTime = filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='B')]['Test Date/Time'].values[0]
                boron.reindexObject(idxs=['Result','AnalysisDateTime'])
                boron = api.do_transition_for(boron, "submit")
                if 'Analyst' in filtered_df.columns and not filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='B')]['Analyst'].empty:
                    boron.Analyst = filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='B')]['Analyst'].values[0]
                    boron.reindexObject(idxs=['Analyst'])
                imported.append(True)
        #Calcium
            if calcium  is not None and api.get_workflow_status_of(calcium) in ['unassigned','retracted'] and not filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Ca')].empty:
                calcium .Result = unicode(filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Ca')]['Formatted Result'].values[0].strip(), "utf-8")
                calcium .AnalysisDateTime = filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Ca')]['Test Date/Time'].values[0]
                calcium .reindexObject(idxs=['Result','AnalysisDateTime'])
                calcium  = api.do_transition_for(calcium , "submit")
                if 'Analyst' in filtered_df.columns and not filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Ca')]['Analyst'].empty:
                    calcium.Analyst = filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Ca')]['Analyst'].values[0]
                    calcium.reindexObject(idxs=['Analyst'])
                imported.append(True)
        #Cobalt
            if cobalt is not None and api.get_workflow_status_of(cobalt) in ['unassigned','retracted'] and not filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Co')].empty:
                cobalt.Result = unicode(filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Co')]['Formatted Result'].values[0].strip(), "utf-8")
                cobalt.AnalysisDateTime = filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Co')]['Test Date/Time'].values[0]
                cobalt.reindexObject(idxs=['Result','AnalysisDateTime'])
                cobalt = api.do_transition_for(cobalt, "submit")
                if 'Analyst' in filtered_df.columns and not filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Co')]['Analyst'].empty:
                    cobalt.Analyst = filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Co')]['Analyst'].values[0]
                    cobalt.reindexObject(idxs=['Analyst'])
                imported.append(True)
        #Copper
            if copper is not None and api.get_workflow_status_of(copper) in ['unassigned','retracted'] and not filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Cu')].empty:
                copper.Result = unicode(filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Cu')]['Formatted Result'].values[0].strip(), "utf-8")
                copper.AnalysisDateTime = filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Cu')]['Test Date/Time'].values[0]
                copper.reindexObject(idxs=['Result','AnalysisDateTime'])
                copper = api.do_transition_for(copper, "submit")
                if 'Analyst' in filtered_df.columns and not filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Cu')]['Analyst'].empty:
                    copper.Analyst = filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Cu')]['Analyst'].values[0]
                    copper.reindexObject(idxs=['Analyst'])
                imported.append(True)
        #Iron
            if iron is not None and api.get_workflow_status_of(iron) in ['unassigned','retracted'] and not filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Fe')].empty:
                iron.Result = unicode(filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Fe')]['Formatted Result'].values[0].strip(), "utf-8")
                iron.AnalysisDateTime = filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Fe')]['Test Date/Time'].values[0]
                iron.reindexObject(idxs=['Result','AnalysisDateTime'])
                iron = api.do_transition_for(iron, "submit")
                if 'Analyst' in filtered_df.columns and not filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Fe')]['Analyst'].empty:
                    iron.Analyst = filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Fe')]['Analyst'].values[0]
                    iron.reindexObject(idxs=['Analyst'])
                imported.append(True)
        #Lead
            if lead is not None and api.get_workflow_status_of(lead) in ['unassigned','retracted'] and not filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Pb')].empty:
                lead.Result = unicode(filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Pb')]['Formatted Result'].values[0].strip(), "utf-8")
                lead.AnalysisDateTime = filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Pb')]['Test Date/Time'].values[0]
                lead.reindexObject(idxs=['Result','AnalysisDateTime'])
                lead = api.do_transition_for(lead, "submit")
                if 'Analyst' in filtered_df.columns and not filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Pb')]['Analyst'].empty:
                    lead.Analyst = filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Pb')]['Analyst'].values[0]
                    lead.reindexObject(idxs=['Analyst'])
                imported.append(True)
        #Magnesium
            if magnesium is not None and api.get_workflow_status_of(magnesium) in ['unassigned','retracted'] and not filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Mg')].empty:
                magnesium.Result = unicode(filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Mg')]['Formatted Result'].values[0].strip(), "utf-8")
                magnesium.AnalysisDateTime = filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Mg')]['Test Date/Time'].values[0]
                magnesium.reindexObject(idxs=['Result','AnalysisDateTime'])
                magnesium = api.do_transition_for(magnesium, "submit")
                if 'Analyst' in filtered_df.columns and not filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Mg')]['Analyst'].empty:
                    magnesium.Analyst = filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Mg')]['Analyst'].values[0]
                    magnesium.reindexObject(idxs=['Analyst'])
                imported.append(True)
        #Manganese
            if manganese is not None and api.get_workflow_status_of(manganese) in ['unassigned','retracted'] and not filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Mn')].empty:
                manganese.Result = unicode(filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Mn')]['Formatted Result'].values[0].strip(), "utf-8")
                manganese.AnalysisDateTime = filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Mn')]['Test Date/Time'].values[0]
                manganese.reindexObject(idxs=['Result','AnalysisDateTime'])
                manganese = api.do_transition_for(manganese, "submit")
                if 'Analyst' in filtered_df.columns and not filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Mn')]['Analyst'].empty:
                    manganese.Analyst = filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Mn')]['Analyst'].values[0]
                    manganese.reindexObject(idxs=['Analyst'])
                imported.append(True)
        #Molybdenum
            if molybdenum is not None and api.get_workflow_status_of(molybdenum) in ['unassigned','retracted'] and not filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Mo')].empty:
                molybdenum.Result = unicode(filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Mo')]['Formatted Result'].values[0].strip(), "utf-8")
                molybdenum.AnalysisDateTime = filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Mo')]['Test Date/Time'].values[0]
                molybdenum.reindexObject(idxs=['Result','AnalysisDateTime'])
                molybdenum = api.do_transition_for(molybdenum, "submit")
                if 'Analyst' in filtered_df.columns and not filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Mo')]['Analyst'].empty:
                    molybdenum.Analyst = filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Mo')]['Analyst'].values[0]
                    molybdenum.reindexObject(idxs=['Analyst'])
                imported.append(True)
        #Nickel
            if nickel is not None and api.get_workflow_status_of(nickel) in ['unassigned','retracted'] and not filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Ni')].empty:
                nickel.Result = unicode(filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Ni')]['Formatted Result'].values[0].strip(), "utf-8")
                nickel.AnalysisDateTime = filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Ni')]['Test Date/Time'].values[0]
                nickel.reindexObject(idxs=['Result','AnalysisDateTime'])
                nickel = api.do_transition_for(nickel, "submit")
                if 'Analyst' in filtered_df.columns and not filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Ni')]['Analyst'].empty:
                    nickel.Analyst = filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Ni')]['Analyst'].values[0]
                    nickel.reindexObject(idxs=['Analyst'])
                imported.append(True)
        #Phosphorus
            if phosphorous is not None and api.get_workflow_status_of(phosphorous) in ['unassigned','retracted'] and not filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='P')].empty:
                phosphorous.Result = unicode(filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='P')]['Formatted Result'].values[0].strip(), "utf-8")
                phosphorous.AnalysisDateTime = filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='P')]['Test Date/Time'].values[0]
                phosphorous.reindexObject(idxs=['Result','AnalysisDateTime'])
                phosphorous = api.do_transition_for(phosphorous, "submit")
                if 'Analyst' in filtered_df.columns and not filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='P')]['Analyst'].empty:
                    phosphorous.Analyst = filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='P')]['Analyst'].values[0]
                    phosphorous.reindexObject(idxs=['Analyst'])
                imported.append(True)
        #Potassium
            if potassium is not None and api.get_workflow_status_of(potassium) in ['unassigned','retracted'] and not filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='K')].empty:
                potassium.Result = unicode(filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='K')]['Formatted Result'].values[0].strip(), "utf-8")
                potassium.AnalysisDateTime = filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='K')]['Test Date/Time'].values[0]
                potassium.reindexObject(idxs=['Result','AnalysisDateTime'])
                potassium = api.do_transition_for(potassium, "submit")
                if 'Analyst' in filtered_df.columns and not filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='K')]['Analyst'].empty:
                    potassium.Analyst = filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='K')]['Analyst'].values[0]
                    potassium.reindexObject(idxs=['Analyst'])
                imported.append(True)
        #Selenium
            if selenium is not None and api.get_workflow_status_of(selenium) in ['unassigned','retracted'] and not filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Se')].empty:
                selenium.Result = unicode(filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Se')]['Formatted Result'].values[0].strip(), "utf-8")
                selenium.AnalysisDateTime = filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Se')]['Test Date/Time'].values[0]
                selenium.reindexObject(idxs=['Result','AnalysisDateTime'])
                selenium = api.do_transition_for(selenium, "submit")
                if 'Analyst' in filtered_df.columns and not filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Se')]['Analyst'].empty:
                    selenium.Analyst = filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Se')]['Analyst'].values[0]
                    selenium.reindexObject(idxs=['Analyst'])
                imported.append(True)
        #Silica
            if silica is not None and api.get_workflow_status_of(silica) in ['unassigned','retracted'] and not filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Si')].empty:
                silica.Result = unicode(filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Si')]['Formatted Result'].values[0].strip(), "utf-8")
                silica.AnalysisDateTime = filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Si')]['Test Date/Time'].values[0]
                silica.reindexObject(idxs=['Result','AnalysisDateTime'])
                silica = api.do_transition_for(silica, "submit")
                if 'Analyst' in filtered_df.columns and not filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Si')]['Analyst'].empty:
                    silica.Analyst = filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Si')]['Analyst'].values[0]
                    silica.reindexObject(idxs=['Analyst'])
                imported.append(True)
        #Sodium
            if sodium is not None and api.get_workflow_status_of(sodium) in ['unassigned','retracted'] and not filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Na')].empty:
                sodium.Result = unicode(filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Na')]['Formatted Result'].values[0].strip(), "utf-8")
                sodium.AnalysisDateTime = filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Na')]['Test Date/Time'].values[0]
                sodium.reindexObject(idxs=['Result','AnalysisDateTime'])
                sodium = api.do_transition_for(sodium, "submit")
                if 'Analyst' in filtered_df.columns and not filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Na')]['Analyst'].empty:
                    sodium.Analyst = filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Na')]['Analyst'].values[0]
                    sodium.reindexObject(idxs=['Analyst'])
                imported.append(True)
        #Sulfur
            if sulfur is not None and api.get_workflow_status_of(sulfur) in ['unassigned','retracted'] and not filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='S')].empty:
                sulfur.Result = unicode(filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='S')]['Formatted Result'].values[0].strip(), "utf-8")
                sulfur.AnalysisDateTime = filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='S')]['Test Date/Time'].values[0]
                sulfur.reindexObject(idxs=['Result','AnalysisDateTime'])
                sulfur = api.do_transition_for(sulfur, "submit")
                if 'Analyst' in filtered_df.columns and not filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='S')]['Analyst'].empty:
                    sulfur.Analyst = filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='S')]['Analyst'].values[0]
                    sulfur.reindexObject(idxs=['Analyst'])
                imported.append(True)
        #Zinc
            if zinc is not None and api.get_workflow_status_of(zinc) in ['unassigned','retracted'] and not filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Zn')].empty:
                zinc.Result = unicode(filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Zn')]['Formatted Result'].values[0].strip(), "utf-8")
                zinc.AnalysisDateTime = filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Zn')]['Test Date/Time'].values[0]
                zinc.reindexObject(idxs=['Result','AnalysisDateTime'])
                zinc = api.do_transition_for(zinc, "submit")
                if 'Analyst' in filtered_df.columns and not filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Zn')]['Analyst'].empty:
                    zinc.Analyst = filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Zn')]['Analyst'].values[0]
                    zinc.reindexObject(idxs=['Analyst'])
                imported.append(True)

        #K/Ca Ratio
            if sap_kcaratio is not None and api.get_workflow_status_of(sap_kcaratio) in ['unassigned','retracted'] and potassium.Result is not None and calcium.Result is not None:
                try:
                    k_float = float(potassium.Result)
                    ca_float = float(calcium.Result)
                    sap_kcaratio.Result = unicode(k_float/ca_float)
                    sap_kcaratio.AnalysisDateTime = potassium.AnalysisDateTime or calcium.AnalysisDateTime
                    sap_kcaratio.reindexObject(idxs=['Result','AnalysisDateTime'])
                    sap_kcaratio = api.do_transition_for(sap_kcaratio, "submit")
                    sap_kcaratio.Analyst = potassium.Analyst or calcium.Analyst
                    sap_kcaratio.reindexObject(idxs=['Analyst'])
                    imported.append(True)
                except:
                    pass

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
        dirty_df = pd.read_csv(csv_doc,sep='\t', keep_default_na=False, dtype=str, skiprows=(0,1,2,3,4,5,6,7,8,10))

        #Convert Gallery CSV to Standard Import CSV format
        samples = []
        results = []
        tests = []
        dates = []
        analysts = []
        dict_to_df = {}
        for i, row in dirty_df.iterrows():
            if 'x' not in row["Sample/ctrl ID"].lower():
                pass
            elif 'x' in row["Sample/ctrl ID"].lower():
                dirty_sample = row["Sample/ctrl ID"] # '1234 ppm'
                radix = dirty_sample.lower().find('x')
                dilution = dirty_sample[radix+1:]
                sid = dirty_sample[:radix] # '1234'
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

        logger.info("Printing Datafram")
        logger.info("{0}".format(df[(df['Sample Name']=='0602211538FL-006') & (df['Test']=='Chloride')]))

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

            imported = []

            #Ammonium
            try:
                ammonium = i.sap_nitrogen_as_ammonium
            except AttributeError:
                ammonium = None
            if ammonium == None:
                try:
                    ammonium = i.hydro_ammonia
                except AttributeError:
                    ammonium = None

            #Total Sugar
            try:
                total_sugar = i.sap_total_sugar
            except AttributeError:
                total_sugar = None

            #Chloride
            try:
                chloride = i.sap_chloride
            except AttributeError:
                chloride = None
            if chloride is None:
                try:
                    chloride = i.hydro_chloride
                except AttributeError:
                    chloride = None

            #Nitrate
            try:
                nitrate = i.sap_nitrate
            except AttributeError:
                nitrate = None
            if nitrate is None:
                try:
                    nitrate = i.hydro_nitrate
                except AttributeError:
                    nitrate = None
            if nitrate is None:
                try:
                    nitrate = i.drinking_nitrate
                except AttributeError:
                    nitrate = None

            #Nitrite
            try:
                nitrite = i.drinking_nitrite
            except AttributeError:
                nitrite = None

            #Nitrogen as Nitrate
            try:
                n_as_nitrate = i.sap_nitrogen_as_nitrate
            except AttributeError:
                n_as_nitrate = None

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
            if ammonium is not None and api.get_workflow_status_of(ammonium) in ['unassigned','retracted'] and not filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Test']=='Ammonium')].empty:
                logger.info("Importing Ammonium for {0}".format(i))
                ammonium.Result = unicode(filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Test']=='Ammonium')]['Result'].values[0].strip(), "utf-8")
                ammonium.AnalysisDateTime = filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Test']=='Ammonium')]['Analysis Date/Time'].values[0]
                ammonium.reindexObject(idxs=['Result','AnalysisDateTime'])
                ammonium = api.do_transition_for(ammonium, "submit")
                if 'Analyst' in filtered_df.columns and not filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Test']=='Ammonium')]['Analyst'].empty:
                    ammonium.Analyst = filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Test']=='Ammonium')]['Analyst'].values[0]
                    ammonium.reindexObject(idxs=['Analyst'])
                imported.append(True)

            #Total Sugar
            if total_sugar is not None and api.get_workflow_status_of(total_sugar) in ['unassigned','retracted'] and not filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Test']=='GluFruSucG')].empty:
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
            if chloride is not None and api.get_workflow_status_of(chloride) in ['unassigned','retracted'] and not filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Test']=='Chloride')].empty:
                logger.info("Importing Chloride for {0}".format(i))
                chloride.Result = unicode(filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Test']=='Chloride')]['Result'].values[0].strip(), "utf-8")
                chloride.AnalysisDateTime = filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Test']=='Chloride')]['Analysis Date/Time'].values[0]
                chloride.reindexObject(idxs=['Result','AnalysisDateTime'])
                chloride = api.do_transition_for(chloride, "submit")
                if 'Analyst' in filtered_df.columns and not filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Test']=='Chloride')]['Analyst'].empty:
                    chloride.Analyst = filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Test']=='Chloride')]['Analyst'].values[0]
                    chloride.reindexObject(idxs=['Analyst'])
                imported.append(True)

            #Nitrate
            if nitrate is not None and api.get_workflow_status_of(nitrate) in ['unassigned','retracted'] and not filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Test']=='SAPNO3')].empty:
                logger.info("Importing Nitrate for {0}. Result is: {1}".format(i,unicode(filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Test']=='SAPNO3')]['Result'].values[0].strip(), "utf-8")))
                nitrate.Result = unicode(filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Test']=='SAPNO3')]['Result'].values[0].strip(), "utf-8")
                nitrate.AnalysisDateTime = filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Test']=='SAPNO3')]['Analysis Date/Time'].values[0]
                nitrate.reindexObject(idxs=['Result','AnalysisDateTime'])
                nitrate = api.do_transition_for(nitrate, "submit")
                if 'Analyst' in filtered_df.columns and not filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Test']=='SAPNO3')]['Analyst'].empty:
                    nitrate.Analyst = filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Test']=='SAPNO3')]['Analyst'].values[0]
                    nitrate.reindexObject(idxs=['Analyst'])
                imported.append(True)

            #Nitrite
            if nitrite is not None and api.get_workflow_status_of(nitrite) in ['unassigned','retracted'] and not filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Test']=='SAPNO2')].empty:
                logger.info("Importing Nitrite for {0}".format(i))
                nitrite.Result = unicode(filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Test']=='SAPNO2')]['Result'].values[0].strip(), "utf-8")
                nitrite.AnalysisDateTime = filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Test']=='SAPNO2')]['Analysis Date/Time'].values[0]
                nitrite.reindexObject(idxs=['Result','AnalysisDateTime'])
                nitrite = api.do_transition_for(nitrite, "submit")
                if 'Analyst' in filtered_df.columns and not filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Test']=='SAPNO2')]['Analyst'].empty:
                    nitrite.Analyst = filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Test']=='SAPNO2')]['Analyst'].values[0]
                    nitrite.reindexObject(idxs=['Analyst'])
                imported.append(True)

            #Nitrogen as Nitrate
            logger.info("N_as_Nitrate is {0}, Status is {1}, Nitrate Result is {2}".format(n_as_nitrate,api.get_workflow_status_of(n_as_nitrate),nitrate.Result))
            if n_as_nitrate is not None and api.get_workflow_status_of(n_as_nitrate) in ['unassigned','retracted'] and nitrate.Result is not None:
                logger.info("Calculating Nitrogen as Nitrate for {0}".format(i))
                nitrate_float = float(nitrate.Result)
                n_as_nitrate.Result = unicode(str(nitrate_float*4.43))
                n_as_nitrate.AnalysisDateTime = nitrate.AnalysisDateTime
                n_as_nitrate.reindexObject(idxs=['Result','AnalysisDateTime'])
                n_as_nitrate = api.do_transition_for(n_as_nitrate, "submit")
                n_as_nitrate.Analyst = nitrate.Analyst
                n_as_nitrate.reindexObject(idxs=['Analyst'])
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
            try:
                ph = i.sap_ph
            except AttributeError:
                ph = None
            if ph == None:
                try:
                    ph = i.hydro_ph
                except AttributeError:
                    ph = None
            logger.info("pH for {0} is {1}".format(i, ph))
            if ph is not None and api.get_workflow_status_of(ph) in ['unassigned','retracted']:
                logger.info("pH Clean for {0}".format(i))
                logger.info("Dataframe {0}".format(filtered_df[(filtered_df['Sample Name']==api.get_id(i))]))
                logger.info("Dataframe is: {0}, Sample Name Series is {1}, ID is {2}".format(filtered_df,filtered_df['Sample Name'],api.get_id(i)))
                clean_ids.append(api.get_id(i))
                #pH
                if 'Analyst' in filtered_df.columns and not filtered_df[(filtered_df['Sample Name']==api.get_id(i))].empty:
                    logger.info("Importing pH for: ".format(i))
                    ph.Result = unicode(filtered_df[(filtered_df['Sample Name']==api.get_id(i))]['Result'].values[0].strip(), "utf-8")
                    ph.AnalysisDateTime = filtered_df[(filtered_df['Sample Name']==api.get_id(i))]['Analysis Date/Time'].values[0]
                    ph.reindexObject(idxs=['Result','AnalysisDateTime'])
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

            #EC
            try:
                ec = i.sap_ec
            except AttributeError:
                ec = None
            if ec == None:
                try:
                    ec = i.hydro_soluablesalts
                except AttributeError:
                    ec = None

            #Calculations
            try:
                hydro_tds = i.hydro_tds
            except AttributeError:
                hydro_tds = None
            #EC
            if ec is not None and api.get_workflow_status_of(ec)=='unassigned' and not filtered_df[(filtered_df['Sample Name']==api.get_id(i))].empty:
                ec.Result = unicode(filtered_df[(filtered_df['Sample Name']==api.get_id(i))]['Result'].values[0].strip(), "utf-8")
                ec.AnalysisDateTime = filtered_df[(filtered_df['Sample Name']==api.get_id(i))]['Analysis Date/Time'].values[0]
                ec.reindexObject(idxs=['Result','AnalysisDateTime'])
                ec = api.do_transition_for(ec, "submit")
                if 'Analyst' in filtered_df.columns and not filtered_df[(filtered_df['Sample Name']==api.get_id(i))]['Analyst'].empty:
                    ec.Analyst = filtered_df[(filtered_df['Sample Name']==api.get_id(i))]['Analyst'].values[0]
                    ec.reindexObject(idxs=['Analyst'])
                imported.append(True)

            #TDS
            if hydro_tds is not None and api.get_workflow_status_of(hydro_tds)=='unassigned' and ec.Result is not None:
                try:
                    ec_float = float(ec.Result)
                    hydro_tds.Result = unicode(ec_float*650)
                    hydro_tds.AnalysisDateTime = ec.AnalysisDateTime
                    hydro_tds.reindexObject(idxs=['Result','AnalysisDateTime'])
                    hydro_tds = api.do_transition_for(hydro_tds, "submit")
                    hydro_tds.Analyst = ec.Analyst
                    hydro_tds.reindexObject(idxs=['Analyst'])
                    imported.append(True)
                except:
                    pass

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

            #Total Nitrogen
            try:
                total_n = i.sap_total_nitrogen
            except AttributeError:
                total_n = None

            if total_n is not None and api.get_workflow_status_of(total_n)=='unassigned':
                clean_ids.append(api.get_id(i))
                #pH
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

            if brix is not None and api.get_workflow_status_of(brix) in ['unassigned','retracted']:
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
                        u"pH data successfully imported for Samples: "+str(number)
                    )
        else:
            IStatusMessage(self.request).addStatusMessage(
                    u"No .CSV File for pH data"
                )

        contextURL = self.context.absolute_url()
        self.request.response.redirect(contextURL)
