import collections

from bika.lims import api
from bika.lims import bikaMessageFactory as _
from Products.Five.browser import BrowserView
from Products.statusmessages.interfaces import IStatusMessage
from zope.interface import alsoProvides
from plone.protect.interfaces import IDisableCSRFProtection

class OptimalLevelView(BrowserView):

    def __init__(self, context, request):
        alsoProvides(request, IDisableCSRFProtection)
        self.context = context
        self.request = request


    def __call__(self):

        ars = self.context.getAnalysisRequests()
        ol = ars[0].getSpecification()

        for i in ars:
            i.setSpecification(ol)
            i.reindexObject(idxs=['Specification'])

        IStatusMessage(self.request).addStatusMessage(
                u"Successfully applied OLs to all samples from sample: {}".format(api.get_id(ars[0]))
            )

        self.request.response.redirect(api.get_url(self.context) + '/batchbook')

class OLResetView(BrowserView):

    def __init__(self, context, request):
        alsoProvides(request, IDisableCSRFProtection)
        self.context = context
        self.request = request


    def __call__(self):

        ars = self.context.getAnalysisRequests()

        for i in ars:
	    ol = i.getSpecification()
	    newbrain = api.search({'portal_type':'AnalysisSpec','title':ol.title})
	    blank = api.get_object(api.search({'portal_type':'AnalysisSpec','title':'-'})[0])
	    if len(newbrain) > 0:
		newobj = api.get_object(newbrain[0])
		i.setSpecification(blank)
            	i.reindexObject(idxs=['Specification'])
		i.setSpecification(newobj)
            	i.reindexObject(idxs=['Specification'])
	    else:
		IStatusMessage(self.request).addStatusMessage(
                    u"No OL found with title: {}".format(ol.title), type="warning"
            	)
	        self.request.response.redirect(api.get_url(self.context) + '/batchbook')

        IStatusMessage(self.request).addStatusMessage(
                u"OLs have been reset"
            )

        self.request.response.redirect(api.get_url(self.context) + '/batchbook')
