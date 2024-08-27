import collections

from bika.lims import api
from bika.lims import bikaMessageFactory as _
from Products.Five.browser import BrowserView
from Products.statusmessages.interfaces import IStatusMessage
from zope.interface import alsoProvides
from plone.protect.interfaces import IDisableCSRFProtection
from plone.dexterity.browser.add import DefaultAddForm
from plone.dexterity.utils import createContentInContainer
from DateTime import DateTime
import math

class PurchaseOrderAddForm(DefaultAddForm):
    def __init__(self, context, request):
        alsoProvides(request, IDisableCSRFProtection)
        self.context = context
        self.request = request
	super(PurchaseOrderAddForm, self).__init__()

    def create(self, data):
        obj = createContentInContainer(self.context, self.portal_type, **data)
        return obj

class PurchaseOrderView(BrowserView):

    def __init__(self, context, request):
        alsoProvides(request, IDisableCSRFProtection)
        self.context = context
        self.request = request
