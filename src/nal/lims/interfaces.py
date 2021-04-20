# -*- coding: utf-8 -*-
"""Module where all interfaces, events and exceptions live."""

# from zope.publisher.interfaces.browser import IDefaultBrowserLayer
# from plone.theme.interfaces import IDefaultPloneLayer
from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from senaite.impress.interfaces import ILayer as ISenaiteImpressLayer
from senaite.lims.interfaces import ISenaiteLIMS
from senaite.core.interfaces import ISenaiteCore
# from zope.interface import Interface
from bika.lims.interfaces import IBikaLIMS


class INalLimsLayer(IDefaultBrowserLayer, IBikaLIMS, ISenaiteLIMS, ISenaiteImpressLayer, ISenaiteCore):
    """Marker interface that defines a browser layer."""
