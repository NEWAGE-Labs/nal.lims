from bika.lims import api
from bika.lims import bikaMessageFactory as _
from bika.lims import logger
from bika.lims.permissions import AddBatch
from bika.lims.utils import get_link
from bika.lims.utils import get_link_for
from bika.lims.browser.publish.reports_listing import ReportsListingView as BikaReportsListingView
from Products.statusmessages.interfaces import IStatusMessage
from plone import api as papi
from nal.lims import api as napi

class ReportsListingView(BikaReportsListingView):

    def __init__(self, context, request):
        super(ReportsListingView, self).__init__(context, request)

	self.context = context
	self.request = request

        #Add New columns
        ## Current Specification
        self.columns['autodownload'] = {
            "title": _("Auto-Download Files"),
            "toggle": True,
            "sortable": True,
        }

        ## Update each contentfilter with the added and modified column keys
	self.review_states[0]["columns"] = self.columns.keys()

        #No return

    def folderitem(self, obj, item, index):
	item = super(ReportsListingView, self).folderitem(obj, item, index)

	obj = api.get_object(obj)
	ar = obj.getAnalysisRequest()
	sdg = ar.getBatch()
	title = sdg.title

	#CALL DOWNLOAD URL
	autolink = str(api.get_url(obj)+'/@@autodownload/')
	item['autodownload'] = get_link(autolink, "download", target="_blank")
	item['replace']['autodownload'] = get_link(autolink, "download", target="_blank")

	return item
