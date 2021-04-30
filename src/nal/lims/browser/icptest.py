from Products.Five.browser import BrowserView
from bika.lims import api


class ICPTestView(BrowserView):

    def saveCSV(self):
        return "I Saved the thing!"
