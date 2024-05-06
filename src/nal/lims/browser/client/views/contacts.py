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
from bika.lims.browser.client import ClientContactsView as BikaClientContactsView
from Products.statusmessages.interfaces import IStatusMessage
from bika.lims import bikaMessageFactory as _

class ClientContactsView(BikaClientContactsView):

    def __init__(self, context, request):
        super(ClientContactsView, self).__init__(context, request)

        self.context = context
        self.request = request

        self.columns["Approved"] = {
            "title": _("Approved for Results"),
            "toggle": True,
            "sortable": True
        }

        self.review_states = [
            {'id': 'default',
             'title': _('Active'),
             'contentFilter': {'is_active': True},
             'transitions': [{'id': 'deactivate'}, ],
             'columns': self.columns.keys()},
            {'id': 'inactive',
             'title': _('Inactive'),
             'contentFilter': {'is_active': False},
             'transitions': [{'id': 'activate'}, ],
             'columns': self.columns.keys()},
            {'id': 'all',
             'title': _('All'),
             'contentFilter': {},
             'columns': self.columns.keys()},
        ]

    def folderitem(self, obj, item, index):
        item = super(ClientContactsView, self).folderitem(obj, item, index)
        contact = item["obj"]
        item['Approved'] = False if not hasattr(contact,"Approved") else contact.Approved

        return item
