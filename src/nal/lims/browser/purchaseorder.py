import collections

from bika.lims import api
from bika.lims import bikaMessageFactory as _
from Products.Five.browser import BrowserView
from Products.statusmessages.interfaces import IStatusMessage

from DateTime import DateTime
import math

class PurchaseOrderView(BrowserView):

    def __init__(self, context, request):
        self.context = context
        self.request = request
