import collections

from bika.lims import api
from bika.lims import bikaMessageFactory as _
from Products.Five.browser import BrowserView
from Products.statusmessages.interfaces import IStatusMessage
from zope.interface import alsoProvides
from plone.protect.interfaces import IDisableCSRFProtection
from nal.lims import api as napi
import os
import shutil

class AEAWebhookView(BrowserView):

    def __init__(self, context, request):
        alsoProvides(request, IDisableCSRFProtection)
        self.context = context
        self.request = request


    def __call__(self):

	print(self.context)
	arr = self.context
	sdg = api.get_object(arr.getAnalysisRequest().getBatch())
	sdg_title = sdg.title

	if sdg.aq_parent.ClientID != u'NAL24-001':
		return False, "SDG not for AEA. Cannot send."

	if not hasattr(sdg,'report_sent') or (hasattr(sdg,'report_sent') and not sdg.report_sent):
		return False, "Invalid SDG to send to AEA"

	r = napi.aeawebhook(sdg)
	if r.status_code == 200:
		sdg.report_sent = True
		return True, "SDG {} successfully sent to AEA".format(sdg.title)
	else:
		return False, "Request sent with error {}. Data did not successfully push".format(r.status_code)
