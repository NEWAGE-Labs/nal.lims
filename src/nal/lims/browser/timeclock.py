import collections

from bika.lims import api
from bika.lims import bikaMessageFactory as _
from Products.Five.browser import BrowserView
from Products.statusmessages.interfaces import IStatusMessage

class TimeclockView(BrowserView):

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):

        portal = api.get_portal()
        timeclockfolder = portal.timeclock
        print("Timeclock Folder is: {0}".format(timeclockfolder))
        current_user = api.get_current_user()
        contact = api.get_user_contact(current_user)
        contact_name = contact.Firstname + ' ' + contact.Surname
        if contact.is_clocked_in:
            api.create(timeclockfolder,'Timeclock', personnel=contact_name, type='Clocked Out')
            contact.is_clocked_in = False
        else:
            api.create(timeclockfolder,'Timeclock', personnel=contact_name, type='Clocked In')
            contact.is_clocked_in = True

        tcf_url = api.get_url(timeclockfolder)
        print("Timeclock Folder URL is: {0}".format(tcf_url))

        IStatusMessage(self.request).addStatusMessage(
                u"Successfully Clocked In/Out"
            )
        self.request.response.redirect(tcf_url)
