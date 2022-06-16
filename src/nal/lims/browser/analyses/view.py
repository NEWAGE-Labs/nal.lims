# -*- coding: utf-8 -*-
#
# This file is part of SENAITE.CORE.
#
# SENAITE.CORE is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, version 2.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc., 51
# Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
# Copyright 2018-2021 by it's authors.
# Some rights reserved, see README and LICENSE.

from bika.lims import api
from bika.lims import bikaMessageFactory as _
from bika.lims.utils import get_link
from bika.lims.utils import get_link_for
from bika.lims.browser.analyses import AnalysesView as BikaAnalysesView

class AnalysesView(BikaAnalysesView):
    """Displays a list of Analyses in a table.

    Visible InterimFields from all analyses are added to self.columns[].
    Keyword arguments are passed directly to bika_analysis_catalog.
    """

    def __init__(self, context, request, **kwargs):
        super(AnalysesView, self).__init__(context, request, **kwargs)

        #Alter existing Columns
        self.columns['state_title']['toggle'] = False
        self.columns['Specification']['title'] = "Range"
        self.columns['Uncertainty']['toggle'] = False
        self.columns['retested']['toggle'] = False
        self.columns['Attachments']['toggle'] = False
        self.columns['CaptureDate']['toggle'] = False
        self.columns['SubmittedBy']['toggle'] = False
        self.columns['Hidden']['toggle'] = False
        self.columns['DueDate']['toggle'] = False

        #Add New columns
        ## Analysis Date/Time
        self.columns['AnalysisDateTime'] = {
            "title": _("Analysis DateTime"),
            "toggle": True,
            "sortable": False,
            "ajax": True,
            "type": "string"
        }
        ## Inconclusive
        self.columns["Inconclusive"] = {
            "title": _("Inconclusive"),
            "toggle": True,
            "sortable": False,
            "ajax": True,
            "type": "boolean"
        }
        ## Update each contentfilter with the added and modified column keys
        for i in self.review_states:
            i["columns"] = self.columns.keys()

        #No return

    def folderitem(self, obj, item, index):
        super(AnalysesView, self).folderitem(obj, item, index)

        obj = api.get_object(obj)
        item['AnalysisDateTime'] = obj.AnalysisDateTime
        item['Inconclusive'] = obj.Inconclusive

        item['allow_edit'].append('Analyst')
        item['allow_edit'].append('AnalysisDateTime')
        item['allow_edit'].append('Inconclusive')
        return item

    def folderitems(self):
        items = super(AnalysesView, self).folderitems()

        self.columns["Method"]["toggle"] = True
        self.columns["Instrument"]["toggle"] = False
        return items
