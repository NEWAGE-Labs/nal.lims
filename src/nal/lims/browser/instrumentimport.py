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
        df = pd.read_csv(StringIO.StringIO(data))
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
            #Log that we checked the sample
            logger.info("Sample {0} Checked".format(i))
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

        for i in import_samples:

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
            try:
                copper = i.sap_copper
            except AttributeError:
                copper = None
            if copper == None:
                try:
                    copper = i.hydro_copper
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
            try:
                sap_nitrate = i.sap_nitrate
            except AttributeError:
                sap_nitrate = None

        #Aluminum
            if aluminum is not None and not aluminum.Result and not filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Al')].empty:
                aluminum.Result = unicode(filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Al')]['Formatted Result'].values[0].strip(), "utf-8")
                aluminum.AnalysisDateTime = filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Al')]['Test Date/Time'].values[0]
                aluminum.reindexObject(idxs=['Result','AnalysisDateTime'])
                aluminum = api.do_transition_for(aluminum, "submit")
        #Boron
            if boron is not None and not boron.Result and not filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='B')].empty:
                boron.Result = unicode(filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='B')]['Formatted Result'].values[0].strip(), "utf-8")
                boron.AnalysisDateTime = filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='B')]['Test Date/Time'].values[0]
                boron.reindexObject(idxs=['Result','AnalysisDateTime'])
                boron = api.do_transition_for(boron, "submit")
        #Calcium
            if calcium  is not None and not calcium .Result and not filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Ca')].empty:
                calcium .Result = unicode(filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Ca')]['Formatted Result'].values[0].strip(), "utf-8")
                calcium .AnalysisDateTime = filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Ca')]['Test Date/Time'].values[0]
                calcium .reindexObject(idxs=['Result','AnalysisDateTime'])
                calcium  = api.do_transition_for(calcium , "submit")
        #Cobalt
            if cobalt is not None and not cobalt.Result and not filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Co')].empty:
                cobalt.Result = unicode(filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Co')]['Formatted Result'].values[0].strip(), "utf-8")
                cobalt.AnalysisDateTime = filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Co')]['Test Date/Time'].values[0]
                cobalt.reindexObject(idxs=['Result','AnalysisDateTime'])
                cobalt = api.do_transition_for(cobalt, "submit")
        #Copper
            if copper is not None and not copper.Result and not filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Cu')].empty:
                copper.Result = unicode(filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Cu')]['Formatted Result'].values[0].strip(), "utf-8")
                copper.AnalysisDateTime = filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Cu')]['Test Date/Time'].values[0]
                copper.reindexObject(idxs=['Result','AnalysisDateTime'])
                copper = api.do_transition_for(copper, "submit")
        #Iron
            if iron is not None and not iron.Result and not filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Fe')].empty:
                iron.Result = unicode(filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Fe')]['Formatted Result'].values[0].strip(), "utf-8")
                iron.AnalysisDateTime = filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Fe')]['Test Date/Time'].values[0]
                iron.reindexObject(idxs=['Result','AnalysisDateTime'])
                iron = api.do_transition_for(iron, "submit")
        #Magnesium
            if magnesium is not None and not magnesium.Result and not filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Mg')].empty:
                magnesium.Result = unicode(filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Mg')]['Formatted Result'].values[0].strip(), "utf-8")
                magnesium.AnalysisDateTime = filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Mg')]['Test Date/Time'].values[0]
                magnesium.reindexObject(idxs=['Result','AnalysisDateTime'])
                magnesium = api.do_transition_for(magnesium, "submit")
        #Manganese
            if manganese is not None and not manganese.Result and not filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Mn')].empty:
                manganese.Result = unicode(filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Mn')]['Formatted Result'].values[0].strip(), "utf-8")
                manganese.AnalysisDateTime = filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Mn')]['Test Date/Time'].values[0]
                manganese.reindexObject(idxs=['Result','AnalysisDateTime'])
                manganese = api.do_transition_for(manganese, "submit")
        #Molybdenum
            if molybdenum is not None and not molybdenum.Result and not filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Mo')].empty:
                molybdenum.Result = unicode(filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Mo')]['Formatted Result'].values[0].strip(), "utf-8")
                molybdenum.AnalysisDateTime = filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Mo')]['Test Date/Time'].values[0]
                molybdenum.reindexObject(idxs=['Result','AnalysisDateTime'])
                molybdenum = api.do_transition_for(molybdenum, "submit")
        #Nickel
            if nickel is not None and not nickel.Result and not filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Ni')].empty:
                nickel.Result = unicode(filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Ni')]['Formatted Result'].values[0].strip(), "utf-8")
                nickel.AnalysisDateTime = filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Ni')]['Test Date/Time'].values[0]
                nickel.reindexObject(idxs=['Result','AnalysisDateTime'])
                nickel = api.do_transition_for(nickel, "submit")
        #Phosphorus
            if phosphorous is not None and not phosphorous.Result and not filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='P')].empty:
                phosphorous.Result = unicode(filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='P')]['Formatted Result'].values[0].strip(), "utf-8")
                phosphorous.AnalysisDateTime = filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='P')]['Test Date/Time'].values[0]
                phosphorous.reindexObject(idxs=['Result','AnalysisDateTime'])
                phosphorous = api.do_transition_for(phosphorous, "submit")
        #Potassium
            if potassium is not None and not potassium.Result and not filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='K')].empty:
                potassium.Result = unicode(filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='K')]['Formatted Result'].values[0].strip(), "utf-8")
                potassium.AnalysisDateTime = filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='K')]['Test Date/Time'].values[0]
                potassium.reindexObject(idxs=['Result','AnalysisDateTime'])
                potassium = api.do_transition_for(potassium, "submit")
        #Selenium
            if selenium is not None and not selenium.Result and not filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Se')].empty:
                selenium.Result = unicode(filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Se')]['Formatted Result'].values[0].strip(), "utf-8")
                selenium.AnalysisDateTime = filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Se')]['Test Date/Time'].values[0]
                selenium.reindexObject(idxs=['Result','AnalysisDateTime'])
                selenium = api.do_transition_for(selenium, "submit")
        #Silica
            if silica is not None and not silica.Result and not filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Si')].empty:
                silica.Result = unicode(filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Si')]['Formatted Result'].values[0].strip(), "utf-8")
                silica.AnalysisDateTime = filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Si')]['Test Date/Time'].values[0]
                silica.reindexObject(idxs=['Result','AnalysisDateTime'])
                silica = api.do_transition_for(silica, "submit")
        #Sodium
            if sodium is not None and not sodium.Result and not filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Na')].empty:
                sodium.Result = unicode(filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Na')]['Formatted Result'].values[0].strip(), "utf-8")
                sodium.AnalysisDateTime = filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Na')]['Test Date/Time'].values[0]
                sodium.reindexObject(idxs=['Result','AnalysisDateTime'])
                sodium = api.do_transition_for(sodium, "submit")
        #Sulfur
            if sulfur is not None and not sulfur.Result and not filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='S')].empty:
                sulfur.Result = unicode(filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='S')]['Formatted Result'].values[0].strip(), "utf-8")
                sulfur.AnalysisDateTime = filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='S')]['Test Date/Time'].values[0]
                sulfur.reindexObject(idxs=['Result','AnalysisDateTime'])
                sulfur = api.do_transition_for(sulfur, "submit")
        #Zinc
            if zinc is not None and not zinc.Result and not filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Zn')].empty:
                zinc.Result = unicode(filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Zn')]['Formatted Result'].values[0].strip(), "utf-8")
                zinc.AnalysisDateTime = filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Zn')]['Test Date/Time'].values[0]
                zinc.reindexObject(idxs=['Result','AnalysisDateTime'])
                zinc = api.do_transition_for(zinc, "submit")

        #K/Ca Ratio
            if sap_kcaratio is not None and not sap_kcaratio.Result and potassium.Result is not None and calcium.Result is not None:
                try:
                    k_float = float(potassium.Result)
                    ca_float = float(calcium.Result)
                    sap_kcaratio.Result = unicode(k_float/ca_float)
                    sap_kcaratio.AnalysisDateTime = potassium.AnalysisDateTime or calcium.AnalysisDateTime
                    sap_kcaratio.reindexObject(idxs=['Result','AnalysisDateTime'])
                    sap_kcaratio = api.do_transition_for(sap_kcaratio, "submit")
                except:
                    pass

        return ','.join(ids)


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

        IStatusMessage(self.request).addStatusMessage(
                u"Import Successful for Samples: "+str(number)
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
        return ''

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

        IStatusMessage(self.request).addStatusMessage(
                u"Import Successful for Gallery"
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
        return ''

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

        IStatusMessage(self.request).addStatusMessage(
                u"Import Successful for pH"
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
        return ''

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

        IStatusMessage(self.request).addStatusMessage(
                u"Import Successful for EC"
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
        return ''

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

        IStatusMessage(self.request).addStatusMessage(
                u"Import Successful for Total Nitrogen"
            )

        contextURL = self.context.absolute_url()
        self.request.response.redirect(contextURL)
