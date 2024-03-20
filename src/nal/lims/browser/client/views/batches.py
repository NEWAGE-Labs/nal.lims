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

from nal.lims.browser.batchfolder import BatchFolderContentsView
from bika.lims import bikaMessageFactory as _
from bika.lims import api
from Products.statusmessages.interfaces import IStatusMessage

class ClientBatchesView(BatchFolderContentsView):

    def before_render(self):
        super(ClientBatchesView, self).before_render()
        self.smessages = IStatusMessage(self.request)
        client = self.context
        if hasattr(client,"Overdue") and client.Overdue:
            self.smessages.addStatusMessage("Account {} is Overdue".format(client.getClientID()), "warning")

    def __init__(self, context, request):
        super(ClientBatchesView, self).__init__(context, request)
        self.view_url = self.context.absolute_url() + "/batches"
        self.contentFilter['getClientUID'] = self.context.UID()
