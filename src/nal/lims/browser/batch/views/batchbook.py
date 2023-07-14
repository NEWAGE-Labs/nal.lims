from bika.lims import api
from bika.lims import bikaMessageFactory as _
from bika.lims import logger
from bika.lims.permissions import AddBatch
from bika.lims.utils import get_link
from bika.lims.utils import get_link_for
from bika.lims.browser.batch.batchbook import BatchBookView as BikaBatchBookView
from Products.statusmessages.interfaces import IStatusMessage
from plone import api as papi

class BatchBookView(BikaBatchBookView):

    def __init__(self, context, request):
        super(BatchBookView, self).__init__(context, request)

	self.smessages = IStatusMessage(self.request)
	self.context = context
	self.request = request

        #Show Column Toggle
        self.show_column_toggles = True
	self.allow_edit = True

        #Alter existing Columns
        self.columns['SampleType']['sortable'] = True

        #Add New columns
        ## Current Specification
        self.columns['CurrentSpecification'] = {
            "title": _("Current Optimal Level"),
            "toggle": False,
            "sortable": True,
        }
        self.columns['Specification'] = {
            "title": _("Replace Optimal Level"),
            "toggle": False,
            "sortable": True,
	    "ajax":True,
        }
        self.columns['PlantType'] = {
            "title": _("Crop"),
            "toggle": False,
            "sortable": True,
        }
        self.columns['Variety'] = {
            "title": _("Variety"),
            "toggle": False,
            "sortable": True,
        }
        self.columns['GrowthStage'] = {
            "title": _("Growth Stage"),
            "toggle": False,
            "sortable": True,
        }

        ## Update each contentfilter with the added and modified column keys
	self.review_states = [
            {
                "id": "default",
                "title": _("Main"),
                "contentFilter": {
			"is_active":True,
			"sort_on":"created",
			"sort_order":"descending",
		},
                "columns": self.columns.keys()
            },
        ]

        #No return

    def folderitems(self):
        items = super(BatchBookView, self).folderitems()

	print("CHECKING NITROGEN")
	self.check_bad_nitrogen(self.context, items)

        for item in items:
            ar = item["obj"]
            item["allow_edit"].append('Specification')
            item["PlantType"] = ar.PlantType
            item["Variety"] = ar.Variety
            item["GrowthStage"] = ar.GrowthStage
            item["CurrentSpecification"] = ar.getSpecification().title if ar.getSpecification() else ''
            item["Specification"] = ar.getSpecification().title if ar.getSpecification() else ''

            if ar.getSampleType().Title() in ['Sap','Root','Fruit','Tissue']:
                spec_vocab = self.get_spec_vocabulary()
                item['choices']['Specification'] = spec_vocab
                self.columns['CurrentSpecification']['toggle'] = True
                self.columns['Specification']['toggle'] = True
                self.columns['PlantType']['toggle'] = True
                self.columns['Variety']['toggle'] = True
                self.columns['GrowthStage']['toggle'] = True

        return items

#    def before_render(self):
#        super(BatchBookView, self).before_render()
#	self.smessages.addStatusMessage("Test Message")
#	self.smessages.show()

    def update(self):
        super(BatchBookView, self).update()
        self.context_actions = {
            _("Apply OL"): {
                "url": "@@optimallevels/",
                "permission": AddBatch,
                "icon": "++resource++bika.lims.images/control_big.png"
            },
            _("Reset OL"): {
                "url": "@@olreset/",
                "permission": AddBatch,
                "icon": "++resource++bika.lims.images/control_big.png"
            },
        }

    def get_spec_vocabulary(self):
        """Returns a vocabulary with all the methods available for the passed in
        analysis, either those assigned to an instrument that are capable to
        perform the test (option "Allow Entry of Results") and those assigned
        manually in the associated Analysis Service.

        The vocabulary is a list of dictionaries. Each dictionary has the
        following structure:

            {'ResultValue': <method_UID>,
             'ResultText': <method_Title>}

        :param analysis_brain: A single Analysis brain
        :type analysis_brain: CatalogBrain
        :returns: A list of dicts
        """
        specs = map(api.get_object,api.search({'portal_type':'AnalysisSpec'}))
        if not specs:
            return [{"ResultValue": "", "ResultText": _("None")}]
        vocab = []
        for spec in specs:
            vocab.append({
                "ResultValue": api.get_uid(spec),
                "ResultText": api.get_title(spec),
            })
        return vocab

    def check_bad_nitrogen(self,context,items):
	bad = []
	for item in items:
	    ar = item["obj"]
	    n = None
	    parts = 0
	    for analysis in map(api.get_object,ar.getAnalyses()):
		if api.get_workflow_status_of(analysis) not in ['cancelled','invalid','retracted','rejected']:
		    keyword = analysis.Keyword
		    if keyword in ['nitrogen_nitrate','nitrogen_ammonium','nitrogen_ammonia','nitrogen_nitrite']:
			try:
			    parts += float(analysis.Result)
			except ValueError:
			    pass
		    if keyword == 'nitrogen':
			try:
			    n = float(analysis.Result)
			except ValueError:
			    pass
	    if n is not None and n < parts:
		bad.append(ar.id)
#	if len(bad) == 1:
#	    self.smessages.addStatusMessage("{} includes Nitrogen Errors".format(bad[0]), "error")
#	elif len(bad) > 1:
#	    self.smessages.addStatusMessage("{} inlcude Nitrogen Errors".format(','.join(bad)), "error")
