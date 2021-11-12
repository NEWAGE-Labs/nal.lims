import collections

from bika.lims import api
from bika.lims import bikaMessageFactory as _
from Products.Five.browser import BrowserView
from Products.statusmessages.interfaces import IStatusMessage

class OptimalLevelView(BrowserView):

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):

        ars = self.context.getAnalysisRequests()
        ol = ars[0].getSpecification()

        for i in ars:
            i.Specification = ol
            i.reindexObject(idxs=['Specification'])

        IStatusMessage(self.request).addStatusMessage(
                u"Successfully applied OLs to all samples".format(self.context.title, filepath)
            )

        self.request.response.redirect(api.get_url(self.context))
