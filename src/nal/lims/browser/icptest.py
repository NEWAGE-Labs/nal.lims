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
import csv
import StringIO
import codecs
import pandas as pd
import logging


class ICPTestView(edit.DefaultEditForm):

    def __init__(self, context, request):
          self.context = context
          self.request = request

    def saveCSV(self, context, request):
        return context.absolute_url_path()

    def processCSV(self, data):
        """
        """
        #Get list of samples
        samples = api.search({'portal_type':'AnalysisRequest'})
        sample_names = []
        for i in samples:
            sample_names.append(api.get_object(i).getId())

        df = pd.read_csv(StringIO.StringIO(data))
        nump = df.values
        retval = []
        logger = logging.getLogger("Plone")
        for i,j in df.iterrows():
            logger.info("i is "+ str(i))
            logger.info("j[sGorwerName] is "+ str(j['sGrowerName']))
        # updated = 0
        # csvdata = ""
        # for row in reader:
        #     # process the data here as needed for the specific case
        #     for idx, name in enumerate(header):
        #         value = row[idx]
        #     updated += 1
            # csvdata.append(row)

        return nump


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
                u"Import Successful"+str(number)
            )

        contextURL = self.context.absolute_url()
        self.request.response.redirect(contextURL)
