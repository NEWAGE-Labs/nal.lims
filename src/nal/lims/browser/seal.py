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

class SealImportView(edit.DefaultEditForm):

    def __init__(self, context, request):
          self.context = context
          self.request = request

    def saveCSV(self, context, request):
        return context.absolute_url_path()

    def processCSV(self, data):
        logger = logging.getLogger('Plone')

        """Process the CSV"""
        nh4_method = map(api.get_object, api.search({'portal_type':'Method','title':'SM4500 NH3-G'}))[0].UID()
        no3_method = map(api.get_object, api.search({'portal_type':'Method','title':'SM4500 NO3-G'}))[0].UID()
        cl_method = map(api.get_object, api.search({'portal_type':'Method','title':'SM4500 Cl-E'}))[0].UID()
        sugar_method = map(api.get_object, api.search({'portal_type':'Method','title':'AOAC 985.09'}))[0].UID()
        so4_method = map(api.get_object, api.search({'portal_type':'Method','title':'SM4500 SO4-E'}))[0].UID()

        #Convert CSV data to a dataframe
        df = pd.read_csv(StringIO.StringIO(data),keep_default_na=False, dtype=str)
        #Get a list of Unique sample names from the imported DataFrame
        sample_names = df['Sample ID'].unique()
        #Take off the '-001' to get a list of SDG titles to search
        batch_titles = df['Sample ID'].str[:-4].unique().tolist()

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
                        df.loc[df['Sample ID'] == i,['Sample ID']] = api.get_id(j)

        #Get the list of Senaite Sample IDs that will be imported into.
        ids = map(api.get_id, import_samples)
        logger.info("IDs: {0}".format(ids))

        #Get a filter dataframe for only the samples that exist
        bool_series = df['Sample ID'].isin(ids)
        filtered_df = df[bool_series]
        clean_ids = []

        for i in import_samples:

            imported = False
            ammonium = None
            nitrate = None
            nitrite = None
            sugars = None
            chloride = None
            fructose = None
            glucose = None
            sucrose = None
            sulfate = None

            for j in i:
                if api.get_workflow_status_of(i[j]) not in ['retracted','rejected','invalid','cancelled']:
                    if 'ammonium' in j or 'ammonia' in j:
                        ammonium = i[j]
                    if 'nitrate' in j:
                        nitrate = i[j]
                    if 'nitrite' in j:
                        nitrite = i[j]
                    if 'chloride' in j:
                        chloride = i[j]
                    if 'sulfate' in j:
                        sulfate = i[j]
                    if 'sugars' in j:
                        sugars = i[j]

            #Ammonium
            if ammonium is not None and api.get_workflow_status_of(ammonium) in ['unassigned'] and not filtered_df[(filtered_df['Sample ID']==api.get_id(i)) & (filtered_df['Test'].str.contains('ammonia',case=False))].empty:
                logger.info("Importing Ammonium for {0}: {1}".format(i, ammonium))

                ammonium.Result = unicode(filtered_df[(filtered_df['Sample ID']==api.get_id(i)) & (filtered_df['Test'].str.contains('ammonia',case=False))]['Results'].values[0].strip(), "utf-8")
                logger.info("Result: ".format(ammonium.Result))
                ammonium.AnalysisDateTime = filtered_df[(filtered_df['Sample ID']==api.get_id(i)) & (filtered_df['Test'].str.contains('ammonia',case=False))]['Date and Time'].values[0]
                ammonium.CustomMethod = nh4_method
                ammonium.reindexObject(idxs=['Results','AnalysisDateTime','CustomMethod'])
                if [j for j in api.get_transitions_for(ammonium) if 'submit' in j.values()]:
                    try:
                        api.do_transition_for(ammonium, "submit")
                    except AttributeError:
                        pass
                if 'Analyst' in filtered_df.columns and not filtered_df[(filtered_df['Sample ID']==api.get_id(i)) & (filtered_df['Test'].str.contains('ammonia',case=False))]['Analyst'].empty:
                    ammonium.Analyst = filtered_df[(filtered_df['Sample ID']==api.get_id(i)) & (filtered_df['Test'].str.contains('ammonia',case=False))]['Analyst'].values[0]
                    ammonium.reindexObject(idxs=['Analyst'])
                imported = True

            #Total Sugar
            if sugars is not None and api.get_workflow_status_of(sugars) in ['unassigned'] and not filtered_df[(filtered_df['Sample ID']==api.get_id(i)) & (filtered_df['Test'].str.contains('gfs',case=False))].empty:
                logger.info("Importing Total Sugar for {0}".format(i))
                sugars.Result = unicode(str(float(filtered_df[(filtered_df['Sample ID']==api.get_id(i)) & (filtered_df['Test'].str.contains('gfs',case=False))]['Results'].values[0].strip())/10000), "utf-8")
                sugars.AnalysisDateTime = filtered_df[(filtered_df['Sample ID']==api.get_id(i)) & (filtered_df['Test'].str.contains('gfs',case=False))]['Date and Time'].values[0]
                sugars.CustomMethod = sugar_method
                sugars.reindexObject(idxs=['Results','AnalysisDateTime','CustomMethod'])
                if [j for j in api.get_transitions_for(sugars) if 'submit' in j.values()]:
                    try:
                        api.do_transition_for(sugars, "submit")
                    except AttributeError:
                        pass
                if 'Analyst' in filtered_df.columns and not filtered_df[(filtered_df['Sample ID']==api.get_id(i)) & (filtered_df['Test'].str.contains('gfs',case=False))]['Analyst'].empty:
                    sugars.Analyst = filtered_df[(filtered_df['Sample ID']==api.get_id(i)) & (filtered_df['Test'].str.contains('gfs',case=False))]['Analyst'].values[0]
                    sugars.reindexObject(idxs=['Analyst'])
                imported = True

            #Chloride
            if chloride is not None and api.get_workflow_status_of(chloride) in ['unassigned'] and not filtered_df[(filtered_df['Sample ID']==api.get_id(i)) & (filtered_df['Test'].str.contains('chloride',case=False))].empty:
                logger.info("Importing Chloride for {0}".format(i))
                chloride.Result = unicode(filtered_df[(filtered_df['Sample ID']==api.get_id(i)) & (filtered_df['Test'].str.contains('chloride',case=False))]['Results'].values[0].strip(), "utf-8")
                chloride.AnalysisDateTime = filtered_df[(filtered_df['Sample ID']==api.get_id(i)) & (filtered_df['Test'].str.contains('chloride',case=False))]['Date and Time'].values[0]
                chloride.CustomMethod = cl_method
                chloride.reindexObject(idxs=['Results','AnalysisDateTime','CustomMethod'])
                if [j for j in api.get_transitions_for(chloride) if 'submit' in j.values()]:
                    try:
                        api.do_transition_for(chloride, "submit")
                    except AttributeError:
                        pass
                if 'Analyst' in filtered_df.columns and not filtered_df[(filtered_df['Sample ID']==api.get_id(i)) & (filtered_df['Test'].str.contains('chloride',case=False))]['Analyst'].empty:
                    chloride.Analyst = filtered_df[(filtered_df['Sample ID']==api.get_id(i)) & (filtered_df['Test'].str.contains('chloride',case=False))]['Analyst'].values[0]
                    chloride.reindexObject(idxs=['Analyst'])
                imported = True

            #Sulfate
            if sulfate is not None and api.get_workflow_status_of(sulfate) in ['unassigned'] and not filtered_df[(filtered_df['Sample ID']==api.get_id(i)) & (filtered_df['Test'].str.contains('sulfate',case=False))].empty:
                logger.info("Importing Sulfate for {0}".format(i))
                sulfate.Result = unicode(filtered_df[(filtered_df['Sample ID']==api.get_id(i)) & (filtered_df['Test'].str.contains('sulfate',case=False))]['Results'].values[0].strip(), "utf-8")
                sulfate.AnalysisDateTime = filtered_df[(filtered_df['Sample ID']==api.get_id(i)) & (filtered_df['Test'].str.contains('sulfate',case=False))]['Date and Time'].values[0]
                sulfate.CustomMethod = so4_method
                sulfate.reindexObject(idxs=['Results','AnalysisDateTime','CustomMethod'])
                if [j for j in api.get_transitions_for(sulfate) if 'submit' in j.values()]:
                    print("Submitting")
                    try:
                        api.do_transition_for(sulfate, "submit")
                    except AttributeError:
                        pass
                if 'Analyst' in filtered_df.columns and not filtered_df[(filtered_df['Sample ID']==api.get_id(i)) & (filtered_df['Test'].str.contains('sulfate',case=False))]['Analyst'].empty:
                    sulfate.Analyst = filtered_df[(filtered_df['Sample ID']==api.get_id(i)) & (filtered_df['Test'].str.contains('sulfate',case=False))]['Analyst'].values[0]
                    sulfate.reindexObject(idxs=['Analyst'])
                imported = True

            #Nitrate
            if nitrate is not None and api.get_workflow_status_of(nitrate) in ['unassigned'] and not filtered_df[(filtered_df['Sample ID']==api.get_id(i)) & (filtered_df['Test'].str.contains('no3',case=False))].empty:
                logger.info("Importing N from Nitrate for {0}. Result is: {1}".format(i,unicode(filtered_df[(filtered_df['Sample ID']==api.get_id(i)) & (filtered_df['Test'].str.contains('no3',case=False))]['Results'].values[0].strip(), "utf-8")))
                nitrate.Result = unicode(filtered_df[(filtered_df['Sample ID']==api.get_id(i)) & (filtered_df['Test'].str.contains('no3',case=False))]['Results'].values[0].strip(), "utf-8")
                nitrate.AnalysisDateTime = filtered_df[(filtered_df['Sample ID']==api.get_id(i)) & (filtered_df['Test'].str.contains('no3',case=False))]['Date and Time'].values[0]
                nitrate.CustomMethod = no3_method
                nitrate.reindexObject(idxs=['Results','AnalysisDateTime','CustomMethod'])
                if [j for j in api.get_transitions_for(nitrate) if 'submit' in j.values()]:
                    try:
                        api.do_transition_for(nitrate, "submit")
                    except AttributeError:
                        pass
                if 'Analyst' in filtered_df.columns and not filtered_df[(filtered_df['Sample ID']==api.get_id(i)) & (filtered_df['Test'].str.contains('no3',case=False))]['Analyst'].empty:
                    nitrate.Analyst = filtered_df[(filtered_df['Sample ID']==api.get_id(i)) & (filtered_df['Test'].str.contains('no3',case=False))]['Analyst'].values[0]
                    nitrate.reindexObject(idxs=['Analyst'])
                imported = True

            #Nitrite
            if nitrite is not None and api.get_workflow_status_of(nitrite) in ['unassigned'] and not filtered_df[(filtered_df['Sample ID']==api.get_id(i)) & (filtered_df['Test'].str.contains('no2',case=False))].empty:
                logger.info("Importing Nitrite for {0}".format(i))
                nitrite.Result = unicode(filtered_df[(filtered_df['Sample ID']==api.get_id(i)) & (filtered_df['Test'].str.contains('no2',case=False))]['Results'].values[0].strip(), "utf-8")
                nitrite.AnalysisDateTime = filtered_df[(filtered_df['Sample ID']==api.get_id(i)) & (filtered_df['Test'].str.contains('no2',case=False))]['Date and Time'].values[0]
                nitrate.CustomMethod = no3_method
                nitrite.reindexObject(idxs=['Results','AnalysisDateTime'])
                if [j for j in api.get_transitions_for(nitrite) if 'submit' in j.values()]:
                    try:
                        api.do_transition_for(nitrite, "submit")
                    except AttributeError:
                        pass
                if 'Analyst' in filtered_df.columns and not filtered_df[(filtered_df['Sample ID']==api.get_id(i)) & (filtered_df['Test'].str.contains('no2',case=False))]['Analyst'].empty:
                    nitrite.Analyst = filtered_df[(filtered_df['Sample ID']==api.get_id(i)) & (filtered_df['Test'].str.contains('no2',case=False))]['Analyst'].values[0]
                    nitrite.reindexObject(idxs=['Analyst'])
                imported = True

            if imported:
                clean_ids.append(api.get_id(i))

            t.get().commit()

        return clean_ids

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
                        u"SEAL data successfully imported for {} Samples: {}".format(len(number),str(','.join(number)))
                    )
        else:
            IStatusMessage(self.request).addStatusMessage(
                    u"No .CSV File for SEAL data"
                )

        contextURL = self.context.absolute_url()
        self.request.response.redirect(contextURL)
