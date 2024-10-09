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

import collections

from Products.CMFCore.permissions import ModifyPortalContent
from plone.app.content.browser.interfaces import IFolderContentsView
from zope.interface import implements

from bika.lims import api
from bika.lims import bikaMessageFactory as _
from bika.lims.browser.bika_listing import BikaListingView
from bika.lims.permissions import AddClient
from bika.lims.permissions import ManageAnalysisRequests
from bika.lims.utils import check_permission
from bika.lims.utils import get_email_link
from bika.lims.utils import get_link
from bika.lims.utils import get_registry_value
from bika.lims.browser.clientfolder import ClientFolderContentsView as BikaClientFolderContentsView


class ClientFolderContentsView(BikaClientFolderContentsView):
    """Listing view for all Clients
    """
    implements(IFolderContentsView)

    _LANDING_PAGE_REGISTRY_KEY = "bika.lims.client.default_landing_page"
    _DEFAULT_LANDING_PAGE = "analysisrequests"

    def __init__(self, context, request):
        super(ClientFolderContentsView, self).__init__(context, request)

	self.context = context
	self.request = request

	self.show_column_toggles = True
	self.allow_edit = True

        self.show_select_row = True
        self.show_select_all_checkbox = True
        self.show_select_column = True

	#Add New Columns
	#self.columns['MBGGrowerNumber'] = {"title": _("MBG Grower #"), "toggle": False}
	#self.columns['TBGrowerNumber'] = {"title": _("True Blue Grower #"), "toggle": False}
	#self.columns['Recent SDG'] = {"title": _("Most Recent SDG")}

	#for i in self.review_states:
	#	i["columns"] = self.columns.keys()

    def folderitem(self, obj, item, index):
        """Applies new properties to the item (Client) that is currently being
        rendered as a row in the list

        :param obj: client to be rendered as a row in the list
        :param item: dict representation of the client, suitable for the list
        :param index: current position of the item within the list
        :type obj: CatalogBrain
        :type item: dict
        :type index: int
        :return: the dict representation of the item
        :rtype: dict
        """
	super(ClientFolderContentsView, self).folderitem(obj, item, index)
	#obj = api.get_object(obj)
	#if hasattr(obj,'MBGGrowerNumber') and obj.MBGGrowerNumber is not None:
	#	item['MBGGrowerNumber'] = obj.MBGGrowerNumber
	#if hasattr(obj,'TBGrowerNumber') and obj.TBGrowerNumber is not None:
	#	item['TBGrowerNumber'] = obj.TBGrowerNumber
	url = api.get_url(obj)
	item["replace"]["title"] = get_link(url+"/batches", item["title"])
	item["replace"]["ClientID"] = get_link(url+"/batches", item["ClientID"])

        return item
