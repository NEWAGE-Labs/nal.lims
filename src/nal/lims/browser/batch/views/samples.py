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
from senaite.core.browser.samples.view import SamplesView
from bika.lims.permissions import AddBatch
from bika.lims import bikaMessageFactory as _

class BatchSamplesView(SamplesView):

    def __init__(self, context, request):
        super(BatchSamplesView, self).__init__(context, request)
        self.contentFilter = {"portal_type": "AnalysisRequest",
                              "getBatchUID": api.get_uid(self.context),
                              "sort_on": "created",
                              "sort_order": "reverse"}

        self.remove_column("BatchID")

    def update(self):
        super(BatchSamplesView, self).update()
        self.context_actions = {
            _("Export SDG as .CSV"): {
                "url": "@@sdgcsvexport/",
                "permission": AddBatch,
                "icon": "++resource++bika.lims.images/control_big.png"
            },
        }

        # always redirect to the /analysisrequets view
        # request_path = self.request.PATH_TRANSLATED
        # if (request_path.endswith(self.context.getId())):
        #     object_url = api.get_url(self.context)
        #     redirect_url = "{}/{}".format(object_url, "analysisrequests")
        #     self.request.response.redirect(redirect_url)
