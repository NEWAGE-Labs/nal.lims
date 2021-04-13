# -*- coding: utf-8 -*-
"""Module where all interfaces, events and exceptions live."""

# from zope.publisher.interfaces.browser import IDefaultBrowserLayer
# from plone.theme.interfaces import IDefaultPloneLayer
from senaite.impress.interfaces import ILayer as ISenaiteImpressLayer
from senaite.lims.interfaces import ISenaiteLIMS
# from zope.interface import Interface
from bika.lims.interfaces import IBikaLIMS


class INalLimsLayer(IBikaLIMS, ISenaiteLIMS, ISenaiteImpressLayer):
    """Marker interface that defines a browser layer."""
