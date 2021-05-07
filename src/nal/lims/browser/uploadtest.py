from plone.dexterity.browser.view import DefaultView
from bika.lims import api
from z3c.form import button
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.statusmessages.interfaces import IStatusMessage

class ICPTestView(DefaultView):

    def __init__(self, context, request):
          self.context = context
          self.request = request

    def update(self):
        if "import_button" in self.request.form:
            index = ViewPageTemplateFile('instrumentreads.pt')
            return self.index()
