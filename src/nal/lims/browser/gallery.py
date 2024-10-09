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
        csv_coded = codecs.decode(data, 'UTF-16').encode('utf-8').decode('utf-8')
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
            if ('fl' in row["Sample/ctrl ID"].lower() or 'test-' in row["Sample/ctrl ID"].lower()) and 'MA' in row['Status']:
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

            imported = False

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
            for j in range(5, 0, -1):
                if found==False:
                    sap_version = 'sugars-'+str(j)
                    if hasattr(i,sap_version) and api.get_workflow_status_of(i[sap_version]) not in ['cancelled','invalid','retracted','rejected']:
                        found = True
                        total_sugar = i[sap_version]
            if found == False and hasattr(i,'sugars') and api.get_workflow_status_of(i['sugars']) not in ['retracted','rejected','cancelled','invalid']:
                total_sugar = i.sugars

            #Frutose
            found = False
            fructose = None
            for j in range(5, 0, -1):
                if found==False:
                    sap_version = 'sugars_fructose-'+str(j)
                    if hasattr(i,sap_version) and api.get_workflow_status_of(i[sap_version]) not in ['cancelled','invalid','retracted','rejected']:
                        found = True
                        fructose = i[sap_version]
            if found == False and hasattr(i,'sugars_fructose') and api.get_workflow_status_of(i['sugars_fructose']) not in ['retracted','rejected','cancelled','invalid']:
                fructose = i.sugars_fructose

            #Glucose
            found = False
            glucose = None
            for j in range(5, 0, -1):
                if found==False:
                    sap_version = 'sugars_glucose-'+str(j)
                    if hasattr(i,sap_version) and api.get_workflow_status_of(i[sap_version]) not in ['cancelled','invalid','retracted','rejected']:
                        found = True
                        glucose = i[sap_version]
            if found == False and hasattr(i,'sugars_glucose') and api.get_workflow_status_of(i['sugars_glucose']) not in ['retracted','rejected','cancelled','invalid']:
                glucose = i.sugars_glucose
            #Sucrose
            found = False
            sucrose = None
            for j in range(5, 0, -1):
                if found==False:
                    sap_version = 'sugars_sucrose-'+str(j)
                    if hasattr(i,sap_version) and api.get_workflow_status_of(i[sap_version]) not in ['cancelled','invalid','retracted','rejected']:
                        found = True
                        sucrose = i[sap_version]
            if found == False and hasattr(i,'sugars_sucrose') and api.get_workflow_status_of(i['sugars_sucrose']) not in ['retracted','rejected','cancelled','invalid']:
                sucrose = i.sugars_sucrose
            if found:
                print("Sucrose is found for {}".format(api.get_id(i)))
            # try:
            #     total_sugar = i.sap_total_sugar
            # except AttributeError:
            #     total_sugar = None

            #Chloride
            found = False
            chloride = None
            for j in range(5, 0, -1):
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
            for j in range(5, 0, -1):
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
            for j in range(5, 0, -1):
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
            for j in range(5, 0, -1):
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
                found = True

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
                found = True

            #Total Sugar
            if total_sugar is not None and api.get_workflow_status_of(total_sugar) in ['unassigned'] and not filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Test'].isin(['GluFruSucG','GEnzytec']))].empty:
                logger.info("Importing Total Sugar for {0}".format(i))
                total_sugar.Result = unicode(filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Test'].isin(['GluFruSucG','GEnzytec']))]['Result'].values[0].strip(), "utf-8")
                total_sugar.AnalysisDateTime = filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Test'].isin(['GluFruSucG','GEnzytec']))]['Analysis Date/Time'].values[0]
                total_sugar.CustomMethod = sugar_method
                total_sugar.reindexObject(idxs=['Result','AnalysisDateTime','CustomMethod'])
                if [j for j in api.get_transitions_for(total_sugar) if 'submit' in j.values()]:
                    try:
                        api.do_transition_for(total_sugar, "submit")
                    except AttributeError:
                        pass
                if 'Analyst' in filtered_df.columns and not filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Test'].isin(['GluFruSucG','GEnzytec']))]['Analyst'].empty:
                    total_sugar.Analyst = filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Test'].isin(['GluFruSucG','GEnzytec']))]['Analyst'].values[0]
                    total_sugar.reindexObject(idxs=['Analyst'])
                found = True

            #Fructose
            if fructose is not None and api.get_workflow_status_of(fructose) in ['unassigned'] and not filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Test']=='D-Fru')].empty:
                logger.info("Importing fructose for {0}".format(i))
                fructose.Result = unicode(filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Test']=='D-Fru')]['Result'].values[0].strip(), "utf-8")
                fructose.AnalysisDateTime = filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Test']=='D-Fru')]['Analysis Date/Time'].values[0]
                fructose.CustomMethod = sugar_method
                fructose.reindexObject(idxs=['Result','AnalysisDateTime','CustomMethod'])
                if [j for j in api.get_transitions_for(fructose) if 'submit' in j.values()]:
                    try:
                        api.do_transition_for(fructose, "submit")
                    except AttributeError:
                        pass
                if 'Analyst' in filtered_df.columns and not filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Test']=='D-Fru')]['Analyst'].empty:
                    fructose.Analyst = filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Test']=='D-Fru')]['Analyst'].values[0]
                    fructose.reindexObject(idxs=['Analyst'])
                found = True

            #Glucose
            if glucose is not None and api.get_workflow_status_of(glucose) in ['unassigned'] and not filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Test']=='D-Glu')].empty:
                logger.info("Importing glucose for {0}".format(i))
                glucose.Result = unicode(filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Test']=='D-Glu')]['Result'].values[0].strip(), "utf-8")
                glucose.AnalysisDateTime = filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Test']=='D-Glu')]['Analysis Date/Time'].values[0]
                glucose.CustomMethod = sugar_method
                glucose.reindexObject(idxs=['Result','AnalysisDateTime','CustomMethod'])
                if [j for j in api.get_transitions_for(glucose) if 'submit' in j.values()]:
                    try:
                        api.do_transition_for(glucose, "submit")
                    except AttributeError:
                        pass
                if 'Analyst' in filtered_df.columns and not filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Test']=='D-Glu')]['Analyst'].empty:
                    glucose.Analyst = filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Test']=='D-Glu')]['Analyst'].values[0]
                    glucose.reindexObject(idxs=['Analyst'])
                found = True

            #Sucrose
            if sucrose is not None and api.get_workflow_status_of(sucrose) in ['unassigned']:
                try:
                    print("Importing Sucrose")
                    logger.info("Importing sucrose for {0}".format(i))
                    glu_f = float(glucose.Result) or float(unicode(filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Test']=='D-Glu')]['Result'].values[0].strip(), "utf-8"))
                    fru_f = float(fructose.Result) or float(unicode(filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Test']=='D-Fru')]['Result'].values[0].strip(), "utf-8"))
                    sugar_f = float(total_sugar.Result) or float(unicode(filtered_df[(filtered_df['Sample Name']==api.get_id(i)) & (filtered_df['Test'].isin(['GluFruSucG','GEnzytec']))]['Result'].values[0].strip(), "utf-8"))
                    sucr_f = float((glu_f+fru_f)-sugar_f)
                    if sucr_f <= 0:
                        sucr_f = 0
                    sucrose.Result = unicode(str(sucr_f), 'utf-8')
                    sucrose.AnalysisDateTime = total_sugar.AnalysisDateTime or glucose.AnalysisDateTime or fructose.AnalysisDateTime
                    sucrose.CustomMethod = sugar_method
                    sucrose.Analyst = total_sugar.Analyst or glucose.Analyst or fructose.Analyst
                    sucrose.reindexObject(idxs=['Result','AnalysisDateTime','CustomMethod', 'Analyst'])
                    if [j for j in api.get_transitions_for(sucrose) if 'submit' in j.values()]:
                        try:
                            api.do_transition_for(sucrose, "submit")
                        except AttributeError:
                            pass
                    found = True
                except Exception as e:
                    print("EXCEPTION FOR SUCROSE IS: {}".format(e))
                    pass

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
                imported = True

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
                imported = True

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
                imported = True
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
                imported = True
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
                imported = True

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
                imported = True

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
