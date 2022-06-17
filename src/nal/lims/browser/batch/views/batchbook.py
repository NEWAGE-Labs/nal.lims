from bika.lims import api
from bika.lims import bikaMessageFactory as _
from bika.lims.permissions import AddBatch
from bika.lims.utils import get_link
from bika.lims.utils import get_link_for
from bika.lims.browser.batch.batchbook import BatchBookView as BikaBatchBookView

class BatchBookView(BikaBatchBookView):

    def __init__(self, context, request):
        super(BatchBookView, self).__init__(context, request)

        #Show Column Toggle
        self.show_column_toggles = True

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
        for i in self.review_states:
            i["columns"] = self.columns.keys()

        #No return

    def folderitems(self):
        items = super(BatchBookView, self).folderitems()

        for item in items:
            ar = item["obj"]
            item["allow_edit"].append('Specification')
            item["PlantType"] = ar.PlantType
            item["Variety"] = ar.Variety
            item["GrowthStage"] = ar.GrowthStage
            item["CurrentSpecification"] = ar.getSpecification().Title() if ar.getSpecification() else ''
            item["Specification"] = ar.getSpecification().Title() if ar.getSpecification() else ''

            if ar.getSampleType().Title() == 'Sap':
                spec_vocab = self.get_spec_vocabulary()
                item['choices']['Specification'] = spec_vocab
                self.columns['CurrentSpecification']['toggle'] = True
                self.columns['Specification']['toggle'] = True
                self.columns['PlantType']['toggle'] = True
                self.columns['Variety']['toggle'] = True
                self.columns['GrowthStage']['toggle'] = True

        return items

    def update(self):
        super(BatchBookView, self).update()
        self.context_actions = {
            _("Apply OL"): {
                "url": "@@optimallevels/",
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
