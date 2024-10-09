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

class pHECImportView(edit.DefaultEditForm):

    def __init__(self, context, request):
          self.context = context
          self.request = request

    def saveCSV(self, context, request):
        return context.absolute_url_path()

    def processCSV(self, data):
        """Process the CSV"""
        #Get logger for output messages
        logger = logging.getLogger("Plone")

        ph_method = map(api.get_object,api.search({'portal_type':'Method','title':'AOAC 973.41'}))[0]
        ec_method = map(api.get_object,api.search({'portal_type':'Method','title':'SM2510B'}))[0]

        #Convert CSV data to a dataframe
        iostr = StringIO.StringIO(data)
        print(iostr.readline())
        print(iostr.readline())
        df = pd.read_csv(iostr,keep_default_na=False, header=None, dtype=str)
        print("Input DF is: {}\Columns are: {}".format(df,df.columns))
        #Get a list of Unique sample names from the imported DataFrame
        sample_names = df[1].str.strip().unique()
        print("Sample Names: {}".format(sample_names))
        print("DF[1] is:\n{}\n\nDF[1].str is:\n{}".format(df[1],df[1].values))
        #Take off the '-001' to get a list of SDG titles to search
        batch_titles = df[1].str[:-4].str.strip().unique().tolist()

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
            i = i.strip()
            xsdg = i[:-4]
            ili = i[-3:]
#           print("SDG: {}\nILI: {}".format(xsdg,ili))
            if xsdg in batch_dict.keys():
                ars = batch_dict[xsdg]
#               print("ARs are: {}".format(ars))
                for j in ars:
                    if (
                        api.get_workflow_status_of(j) not in ['retracted','rejected','invalid','cancelled']
                        and (j.InternalLabID == ili
                        or api.get_id(j) == i)
                    ):
                        print("ADDING {} aka {} - {}".format(i,api.get_id(j),j))
                        import_samples.append(j)
                        print("Updating: {} to {}".format(df.loc[df[1] == i,['1']], api.get_id(j)))

#        print("DF is:\n {}".format(df))
        #Get the list of Senaite Sample IDs that will be imported into.
        ids = map(api.get_id, import_samples)
#        print("IDs: {0}".format(ids))

        #Get a filter dataframe for only the samples that exist
        bool_series = df[1].isin(ids)
        filtered_df = df[bool_series]
        clean_ids = []
        for i in import_samples:
            print('IMPORTING - Sample {0} ID: {1}'.format(i,api.get_id(i)))

            found = False
            ph = None
            ec = None
            tds = None


            for j in map(api.get_object,i.getAnalyses()):
                if api.get_workflow_status_of(j) not in ['retracted','rejected','invalid','cancelled']:
                    if j.Keyword == 'ph':
                        ph = j
                    if j.Keyword == 'ec' or j.Keyword == 'solublesalts':
                        ec = j
                        print("ec analysis acquired")
                    if j.Keyword == 'dissolved_solids':
                        tds = j

            print("filtered df: {}".format(filtered_df))
        #pH
            if ph is not None and api.get_workflow_status_of(ph) in ['unassigned'] and not filtered_df[(filtered_df[1]==api.get_id(i)) & (filtered_df[3].str.contains('pH = '))].empty:
                ph_text = unicode(filtered_df[(filtered_df[1]==api.get_id(i)) & (filtered_df[3].str.contains('pH = '))][3].values[0].strip().replace('pH = ',''), "utf-8")
                if ph_text != '0':
                    ph.AnalysisDateTime = DateTime().Date()
                    ph.CustomMethod = ph_method.UID()
                    ph.reindexObject(idxs=['Result','AnalysisDateTime','CustomMethod'])
                    if [j for j in api.get_transitions_for(ph) if 'submit' in j.values()]:
                        try:
                            api.do_transition_for(ph, "submit")
                        except AttributeError:
                            pass
                    found = True
        #ec
            print("ID:{} Row:{}".format(api.get_id(i),filtered_df[filtered_df[1]==api.get_id(i)]))
            if ec is not None and api.get_workflow_status_of(ec) in ['unassigned'] and not filtered_df[(filtered_df[1]==api.get_id(i)) & (filtered_df[3].str.contains('Cond = '))].empty:
                ec_text = unicode(filtered_df[(filtered_df[1]==api.get_id(i)) & (filtered_df[3].str.contains('Cond = '))][3].values[0].strip().replace('Cond = ',''), "utf-8")
                print("Found ec match")
                if ec_text != '0':
                    print("Uploading EC")
                    ec_float = float(ec_text)/1000
                    ec.Result = unicode(ec_float)
                    ec.AnalysisDateTime = DateTime().Date()
                    ec.CustomMethod = ec_method.UID()
                    ec.reindexObject(idxs=['Result','AnalysisDateTime','CustomMethod'])
                    if [j for j in api.get_transitions_for(ec) if 'submit' in j.values()]:
                        try:
                            api.do_transition_for(ec, "submit")
                        except AttributeError:
                            pass
                    found = True

        #TDS
            if tds is not None and ec is not None and api.get_workflow_status_of(tds)=='unassigned' and ec.Result is not None and not filtered_df[(filtered_df[1]==api.get_id(i))].empty:
                logger.info("Caclulation TDS for {0}".format(i))
                ec_text = unicode(ec.Result)
                ec_float = float(ec_text)
                tds.Result = unicode(ec_float*650)
                tds.AnalysisDateTime = DateTime().Date()
                tds.CustomMethod = ec_method.UID()
                tds.reindexObject(idxs=['Result','AnalysisDateTime','CustomMethod'])
                if [j for j in api.get_transitions_for(tds) if 'submit' in j.values()]:
                    try:
                        api.do_transition_for(tds, "submit")
                    except AttributeError:
                        pass
                found = True

            if found:
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
                        u"pH/Conductivity data successfully imported for Samples: "+str(number)
                    )
        else:
            IStatusMessage(self.request).addStatusMessage(
                    u"No .CSV File for pH/Conductivity data"
                )
        contextURL = self.context.absolute_url()
        self.request.response.redirect(contextURL)
