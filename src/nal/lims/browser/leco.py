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

class LECOImportView(edit.DefaultEditForm):

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
