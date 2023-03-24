from bika.lims import api
from bika.lims.controlpanel.bika_analysisprofiles import AnalysisProfilesView as BikaAnalysisProfilesView
from senaite.core.catalog import SENAITE_CATALOG
from bika.lims import bikaMessageFactory as _

class AnalysisProfilesView(BikaAnalysisProfilesView):

	def __init__(self, context, request, **kwargs):
		super(AnalysisProfilesView, self).__init__(context, request, **kwargs)

		## Analysis Date/Time
        	self.columns['AnalysisProfilePrice'] = {
            	    "title": _("Price"),
            	    "toggle": True,
          	    "sortable": True,
        }

	


	## Update each contentfilter with the added and modified column keys
        	for i in self.review_states:
            	    i["columns"] = self.columns.keys()

	def folderitem(self, obj, item, index):
		super(AnalysisProfilesView, self).folderitem(obj, item, index)

		obj = api.get_object(obj)
		if obj.AnalysisProfilePrice is not None:
		    item['AnalysisProfilePrice'] = obj.getAnalysisProfilePrice()

		return item
