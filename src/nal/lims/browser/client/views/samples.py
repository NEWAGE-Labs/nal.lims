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
from Products.statusmessages.interfaces import IStatusMessage

class ClientSamplesView(SamplesView):

    def __init__(self, context, request):
        super(ClientSamplesView, self).__init__(context, request)

        self.contentFilter["path"] = {
            "query": api.get_path(context),
            "level": 0}

        self.remove_column("Client")

    def before_render(self):
        super(ClientSamplesView, self).before_render()
        self.smessages = IStatusMessage(self.request)
        client = self.context
        if hasattr(client,"Overdue") and client.Overdue:
            self.smessages.addStatusMessage("Account {} is Overdue".format(client.getClientID()), "warning")

    def update(self):
        super(ClientSamplesView, self).update()

        # always redirect to the /analysisrequets view
        request_path = self.request.PATH_TRANSLATED
        if (request_path.endswith(self.context.getId())):
            object_url = api.get_url(self.context)
            redirect_url = "{}/{}".format(object_url, "analysisrequests")
            self.request.response.redirect(redirect_url)
