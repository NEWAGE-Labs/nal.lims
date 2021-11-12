from AccessControl import getSecurityManager
from AccessControl.User import UnrestrictedUser
from AccessControl.SecurityManagement import newSecurityManager
from bika.lims import api
portal = api.get_portal()
me = UnrestrictedUser(getSecurityManager().getUser().getUserName(), '', ['LabManager'], '')
me = me.__of__(portal.acl_users)
newSecurityManager(None, me)

sample = map(api.get_object,api.search({'portal_type':'Samplepoint'}))
location = map(api.get_object,api.search({'portal_type':'SamplePoint','id':'samplepoint-483'}))[0]
