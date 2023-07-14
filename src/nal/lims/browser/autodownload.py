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

class AutoDownloadView(BrowserView):

    def __init__(self, context, request):
        alsoProvides(request, IDisableCSRFProtection)
        self.context = context
        self.request = request


    def __call__(self):

	print(self.context)
	arr = self.context
	sdg = api.get_object(arr.getAnalysisRequest().getBatch())
	sdg_title = sdg.title
	rpath = '/Mnt/Data/Pending Email/'

	for r,d,f in os.walk('/Mnt/Data/Data 2023'):
	    if sdg_title == r[-12:]:
		path = r
		files = f

	for i in range(20):
	    v = str(i+1)
	    pdfname = sdg_title +'_FR v{}.pdf'.format(v)
	    csvname = sdg_title +' v{}.csv'.format(v)
	    if pdfname in files or csvname in files:
		pass
	    else:
		napi.getSDGCSV(sdg).to_csv(path+'/'+csvname)
		try:
		    napi.getSDGCSV(sdg).to_csv(rpath+sdg_title+'/'+csvname)
		except IOError as ioe:
		    os.makedirs(rpath+sdg_title)
		    napi.getSDGCSV(sdg).to_csv(rpath+sdg_title+'/'+csvname)
		with arr.getRawPdf().blob.open() as f:
		    print("blob is: {}".format(f))
		    shutil.copyfile(f.name, path+'/'+pdfname)
		    shutil.copyfile(f.name, rpath+sdg_title+'/'+pdfname)
		break

        IStatusMessage(self.request).addStatusMessage(
                u"Download .PDF and .CSV file to: {}".format(path[4:])
            )

        self.request.response.redirect(api.get_url(sdg.getClient())+'/reports_listing')
