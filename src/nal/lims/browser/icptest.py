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

class ICPTestAddView(add.DefaultAddForm):

    def __init__(self, context, request):
          self.context = context
          self.request = request

    # Buttons

    @button.buttonAndHandler(u'Save', name='save')
    def handleAdd(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return

        # obj = self.createAndAdd(data)
        # if obj is not None:
        #     # mark only as finished if we get the new object
        #     self._finishedAdd = True
        #     IStatusMessage(self.request).addStatusMessage(
        #         self.success_message, "info"
        #     )

    @button.buttonAndHandler(u'Cancel', name='cancel')
    def handleCancel(self, action):
        IStatusMessage(self.request).addStatusMessage(
            u"Add New Item operation cancelled", "info"
        )
        self.request.response.redirect(self.nextURL())
        notify(AddCancelledEvent(self.context))

class ICPTestView(edit.DefaultEditForm):

    def __init__(self, context, request):
          self.context = context
          self.request = request

    def saveCSV(self, context, request):
        return context.absolute_url_path()

    def processCSV(self, data):
        """Process the CSV"""
        #Get logger for output messages
        logger = logging.getLogger("Plone")

        #Get list of samples in Senaite
        samples = api.search({'portal_type':'AnalysisRequest'})
        sample_names = []
        for i in samples:
            sample_names.append(api.get_object(i).getId())

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

        #Get the list of Senaite Sample IDs that will be imported into.
        ids = map(api.get_id, import_samples)

        #Get a filter dataframe for only the samples that exist
        bool_series = df['Sample Name'].isin(ids)
        filtered_df = df[bool_series]

        for i in import_samples:

            try:
                sap_nickel = i.sap_nickel
            except AttributeError:
                sap_nickel = None
            try:
                sap_aluminum = i.sap_aluminum
            except AttributeError:
                sap_aluminum = None
            try:
                sap_boron = i.sap_boron
            except AttributeError:
                sap_boron = None
            try:
                sap_calcium = i.sap_calcium
            except AttributeError:
                sap_calcium = None
            try:
                sap_cobalt = i.sap_cobalt
            except AttributeError:
                sap_cobalt = None
            try:
                sap_copper = i.sap_copper
            except AttributeError:
                sap_copper = None
            try:
                sap_iron = i.sap_iron
            except AttributeError:
                sap_iron = None
            try:
                sap_magnesium = i.sap_magnesium
            except AttributeError:
                sap_magnesium = None
            try:
                sap_manganese = i.sap_manganese
            except AttributeError:
                sap_manganese = None
            try:
                sap_molybdenum = i.sap_molybdenum
            except AttributeError:
                sap_molybdenum = None
            try:
                sap_phosphorous = i.sap_phosphorous
            except AttributeError:
                sap_phosphorous = None
            try:
                sap_potassium = i.sap_potassium
            except AttributeError:
                sap_potassium = None
            try:
                sap_selenium = i.sap_selenium
            except AttributeError:
                sap_selenium = None
            try:
                sap_silica = i.sap_silica
            except AttributeError:
                sap_silica = None
            try:
                sap_sodium = i.sap_sodium
            except AttributeError:
                sap_sodium = None
            try:
                sap_sulfur = i.sap_sulfur
            except AttributeError:
                sap_sulfur = None
            try:
                sap_zinc = i.sap_zinc
            except AttributeError:
                sap_zinc = None

            try:
                sap_kcaratio = i.sap_kcaratio
            except AttributeError:
                sap_kcaratio = None
            try:
                sap_nitrate = i.sap_nitrate
            except AttributeError:
                sap_nitrate = None

        #Nickel
            if sap_nickel is not None and not sap_nickel.Result and not filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Ni')].empty:
                sap_nickel.Result = unicode(filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Ni')]['Formatted Result'].values[0].strip(), "utf-8")
                sap_nickel.AnalysisDateTime = filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Ni')]['Test Date/Time'].values[0]
                sap_nickel.reindexObject(idxs=['Result','AnalysisDateTime'])
                sap_nickel = api.do_transition_for(sap_nickel, "submit")
        #Aluminum
            if sap_aluminum is not None and not sap_aluminum.Result and not filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Al')].empty:
                sap_aluminum.Result = unicode(filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Al')]['Formatted Result'].values[0].strip(), "utf-8")
                sap_aluminum.AnalysisDateTime = filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Al')]['Test Date/Time'].values[0]
                sap_aluminum.reindexObject(idxs=['Result','AnalysisDateTime'])
                sap_aluminum = api.do_transition_for(sap_aluminum, "submit")
        #Boron
            if sap_boron is not None and not sap_boron.Result and not filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='B')].empty:
                sap_boron.Result = unicode(filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='B')]['Formatted Result'].values[0].strip(), "utf-8")
                sap_boron.AnalysisDateTime = filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='B')]['Test Date/Time'].values[0]
                sap_boron.reindexObject(idxs=['Result','AnalysisDateTime'])
                sap_boron = api.do_transition_for(sap_boron, "submit")
        #Calcium
            if sap_calcium is not None and not sap_calcium.Result and not filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Ca')].empty:
                sap_calcium.Result = unicode(filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Ca')]['Formatted Result'].values[0].strip(), "utf-8")
                sap_calcium.AnalysisDateTime = filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Ca')]['Test Date/Time'].values[0]
                sap_calcium.reindexObject(idxs=['Result','AnalysisDateTime'])
                sap_calcium = api.do_transition_for(sap_calcium, "submit")
        #Cobalt
            if sap_cobalt is not None and not sap_cobalt.Result and not filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Co')].empty:
                sap_cobalt.Result = unicode(filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Co')]['Formatted Result'].values[0].strip(), "utf-8")
                sap_cobalt.AnalysisDateTime = filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Co')]['Test Date/Time'].values[0]
                sap_cobalt.reindexObject(idxs=['Result','AnalysisDateTime'])
                sap_cobalt = api.do_transition_for(sap_cobalt, "submit")
        #Copper
            if sap_copper is not None and not sap_copper.Result and not filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Cu')].empty:
                sap_copper.Result = unicode(filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Cu')]['Formatted Result'].values[0].strip(), "utf-8")
                sap_copper.AnalysisDateTime = filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Cu')]['Test Date/Time'].values[0]
                sap_copper.reindexObject(idxs=['Result','AnalysisDateTime'])
                sap_copper = api.do_transition_for(sap_copper, "submit")
        #Iron
            if sap_iron is not None and not sap_iron.Result and not filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Fe')].empty:
                sap_iron.Result = unicode(filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Fe')]['Formatted Result'].values[0].strip(), "utf-8")
                sap_iron.AnalysisDateTime = filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Fe')]['Test Date/Time'].values[0]
                sap_iron.reindexObject(idxs=['Result','AnalysisDateTime'])
                sap_iron = api.do_transition_for(sap_iron, "submit")
        #Magnesium
            if sap_magnesium is not None and not sap_magnesium.Result and not filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Mg')].empty:
                sap_magnesium.Result = unicode(filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Mg')]['Formatted Result'].values[0].strip(), "utf-8")
                sap_magnesium.AnalysisDateTime = filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Mg')]['Test Date/Time'].values[0]
                sap_magnesium.reindexObject(idxs=['Result','AnalysisDateTime'])
                sap_magnesium = api.do_transition_for(sap_magnesium, "submit")
        #Manganese
            if sap_manganese is not None and not sap_manganese.Result and not filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Mn')].empty:
                sap_manganese.Result = unicode(filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Mn')]['Formatted Result'].values[0].strip(), "utf-8")
                sap_manganese.AnalysisDateTime = filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Mn')]['Test Date/Time'].values[0]
                sap_manganese.reindexObject(idxs=['Result','AnalysisDateTime'])
                sap_manganese = api.do_transition_for(sap_manganese, "submit")
        #Molybdenum
            if sap_molybdenum is not None and not sap_molybdenum.Result and not filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Mo')].empty:
                sap_molybdenum.Result = unicode(filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Mo')]['Formatted Result'].values[0].strip(), "utf-8")
                sap_molybdenum.AnalysisDateTime = filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Mo')]['Test Date/Time'].values[0]
                sap_molybdenum.reindexObject(idxs=['Result','AnalysisDateTime'])
                sap_molybdenum = api.do_transition_for(sap_molybdenum, "submit")
        #Phosphorus
            if sap_phosphorous is not None and not sap_phosphorous.Result and not filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='P')].empty:
                sap_phosphorous.Result = unicode(filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='P')]['Formatted Result'].values[0].strip(), "utf-8")
                sap_phosphorous.AnalysisDateTime = filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='P')]['Test Date/Time'].values[0]
                sap_phosphorous.reindexObject(idxs=['Result','AnalysisDateTime'])
                sap_phosphorous = api.do_transition_for(sap_phosphorous, "submit")
        #Potassium
            if sap_potassium is not None and not sap_potassium.Result and not filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='K')].empty:
                sap_potassium.Result = unicode(filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='K')]['Formatted Result'].values[0].strip(), "utf-8")
                sap_potassium.AnalysisDateTime = filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='K')]['Test Date/Time'].values[0]
                sap_potassium.reindexObject(idxs=['Result','AnalysisDateTime'])
                sap_potassium = api.do_transition_for(sap_potassium, "submit")
        #Selenium
            if sap_selenium is not None and not sap_selenium.Result and not filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Se')].empty:
                sap_selenium.Result = unicode(filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Se')]['Formatted Result'].values[0].strip(), "utf-8")
                sap_selenium.AnalysisDateTime = filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Se')]['Test Date/Time'].values[0]
                sap_selenium.reindexObject(idxs=['Result','AnalysisDateTime'])
                sap_selenium = api.do_transition_for(sap_selenium, "submit")
        #Silica
            if sap_silica is not None and not sap_silica.Result and not filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Si')].empty:
                sap_silica.Result = unicode(filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Si')]['Formatted Result'].values[0].strip(), "utf-8")
                sap_silica.AnalysisDateTime = filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Si')]['Test Date/Time'].values[0]
                sap_silica.reindexObject(idxs=['Result','AnalysisDateTime'])
                sap_silica = api.do_transition_for(sap_silica, "submit")
        #Sodium
            if sap_sodium is not None and not sap_sodium.Result and not filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Na')].empty:
                sap_sodium.Result = unicode(filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Na')]['Formatted Result'].values[0].strip(), "utf-8")
                sap_sodium.AnalysisDateTime = filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Na')]['Test Date/Time'].values[0]
                sap_sodium.reindexObject(idxs=['Result','AnalysisDateTime'])
                sap_sodium = api.do_transition_for(sap_sodium, "submit")
        #Sulfur
            if sap_sulfur is not None and not sap_sulfur.Result and not filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='S')].empty:
                sap_sulfur.Result = unicode(filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='S')]['Formatted Result'].values[0].strip(), "utf-8")
                sap_sulfur.AnalysisDateTime = filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='S')]['Test Date/Time'].values[0]
                sap_sulfur.reindexObject(idxs=['Result','AnalysisDateTime'])
                sap_sulfur = api.do_transition_for(sap_sulfur, "submit")
        #Zinc
            if sap_zinc is not None and not sap_zinc.Result and not filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Zn')].empty:
                sap_zinc.Result = unicode(filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Zn')]['Formatted Result'].values[0].strip(), "utf-8")
                sap_zinc.AnalysisDateTime = filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Zn')]['Test Date/Time'].values[0]
                sap_zinc.reindexObject(idxs=['Result','AnalysisDateTime'])
                sap_zinc = api.do_transition_for(sap_zinc, "submit")

        #K/Ca Ratio
            if sap_kcaratio is not None and not sap_kcaratio.Result and sap_potassium.Result is not None amd sap_calcium.Result is not None:
                try:
                    k_float = float(sap_potassium.Result)
                    ca_float = float(sap_calcium.Result)
                    sap_kcaratio.Result (k_float/ca_float)
                    sap_kcaratio.AnalysisDateTime = sap_potassium.AnalysisDateTime or sap_calcium.AnalysisDateTime
                    sap_kcaratio.reindexObject(idxs=['Result','AnalysisDateTime'])
                    sap_kcaratio = api.do_transition_for(sap_kcaratio, "submit")
                except:
                    pass



        return filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Ni')].values

    @button.buttonAndHandler(u'Import')
    def handleApply(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return
        # Redirect back to the front page with a status message

        # get the actual data
        file = data["IInstrumentReadFolder.sample"].data

        # do the processing
        number = self.processCSV(file)

        IStatusMessage(self.request).addStatusMessage(
                u"Import Successful for Samples: "+str(number)
            )

        contextURL = self.context.absolute_url()
        self.request.response.redirect(contextURL)


# updated = 0
# csvdata = ""
# for row in reader:
#     # process the data here as needed for the specific case
#     for idx, name in enumerate(header):
#         value = row[idx]
#     updated += 1
# csvdata.append(row)
