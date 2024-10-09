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

        methods = map(api.get_object, api.search({'portal_type':'Method'}))

        #Convert CSV data to a dataframe
        df = pd.read_csv(StringIO.StringIO(data),keep_default_na=False, dtype=str)
        #Get a list of Unique sample names from the imported DataFrame
        sidcol = ''
        for i in df.columns:
                if 'sample' in i.lower():
                        sidcol = i
        if sidcol != '':
                sample_ids = df[sidcol].unique()
        else:
                raise("No Sample ID column. Please include 1 column with the word 'sample' filled with sample IDs.")
        print("Sample IDS: {}".format(sample_ids))
        #Take off the '-001' to get a list of SDG titles to search
        batch_titles = df[sidcol].str[:-4].unique().tolist()
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
                        df.loc[df[sidcol] == i,[sidcol]] = api.get_id(j)

        #Get the list of Senaite Sample IDs that will be imported into.
        ids = map(api.get_id, import_samples)
        print(ids)
        #Get a filter dataframe for only the samples that exist
        bool_series = df[sidcol].isin(ids)
        filtered_df = df[bool_series]
        clean_ids = []
        for i in import_samples:
            sid = api.get_id(i)
            if not filtered_df[(filtered_df[sidcol]==sid)].empty:
                tests = [col for col in filtered_df.columns if col not in [sidcol,'analyst','datetime']]

                test_dict = {}
                for test in tests:
                    test_dict[test] = None

                for analyte in map(api.get_object,i.getAnalyses()):
                    if api.get_workflow_status_of(analyte) not in ['retracted','rejected','invalid','cancelled']:
                        for test in tests:
                            if analyte.Keyword == test:
                                method = [m.UID() for m in map(api.get_object,[api.get_object_by_uid(j['methodid']) for j in analyte.getAnalysisService().MethodRecords])][0]
                                test_dict[test] = (analyte,method)

                for test in tests:
                    if test_dict[test] is not None and api.get_workflow_status_of(test_dict[test][0]) in ['unassigned']:
                        analysis = test_dict[test][0]
                        method = test_dict[test][1]
                        analysis.Result = unicode(filtered_df[(filtered_df[sidcol]==sid)][test].values[0].strip(), "utf-8")
                        analysis.AnalysisDateTime = filtered_df[(filtered_df[sidcol]==sid)]['datetime'].values[0]
                        analysis.CustomMethod = method
                        analysis.reindexObject(idxs=['Result','AnalysisDateTime','CustomMethod'])
                        if [j for j in api.get_transitions_for(analysis) if 'submit' in j.values()]:
                            try:
                                api.do_transition_for(analysis, "submit")
                            except AttributeError:
                                pass
                        if 'analyst' in filtered_df.columns and not filtered_df[(filtered_df[sidcol]==sid)]['analyst'].empty:
                            analysis.Analyst = filtered_df[(filtered_df[sidcol]==sid)]['analyst'].values[0]
                            analysis.reindexObject(idxs=['analyst'])
                        clean_ids.append(sid)

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
