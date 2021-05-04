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
            if i.sap_nickel and not i.sap_nickel.Result and not filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Ni')].empty:
                i.sap_nickel.Result = unicode(filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Ni')]['Formatted Result'].values[0].strip(), "utf-8")
                i.sap_nickel.AnalysisDateTime = filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Element']=='Ni')]['Test Date/Time'].values[0]
                i.sap_nickel.reindexObject(idxs=['Result','AnalysisDateTime'])


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
