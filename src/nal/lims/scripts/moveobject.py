from AccessControl import getSecurityManager
from AccessControl.User import UnrestrictedUser
from AccessControl.SecurityManagement import newSecurityManager
from bika.lims import api
import pandas as pd
from DateTime import DateTime
portal = api.get_portal()
me = UnrestrictedUser(getSecurityManager().getUser().getUserName(), '', ['LabManager'], '')
me = me.__of__(portal.acl_users)
newSecurityManager(None, me)
from plone import api as papi
import transaction as t

c = api.get_object(api.search({'id':'client-1102'})[0])
b = api.get_object(api.search({'id':'tSDG-1973'})[0])

papi.content.move(source=b,target=c)

for i in b.getAnalysisRequests():
    papi.content.move(source=i,target=c)
