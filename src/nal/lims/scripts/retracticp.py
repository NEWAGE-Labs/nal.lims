from AccessControl import getSecurityManager
from AccessControl.User import UnrestrictedUser
from AccessControl.SecurityManagement import newSecurityManager
from bika.lims import api
portal = api.get_portal()
me = UnrestrictedUser(getSecurityManager().getUser().getUserName(), '', ['LabManager'], '')
me = me.__of__(portal.acl_users)
newSecurityManager(None, me)
import transaction as t

bid = 'tSDG-2113'

b = api.get_object(api.search({'id':bid})[0])

an = []

for i in b.getAnalysisRequests():
    for j in i.getAnalyses():
        if any(['retract' in y for y in [x.values() for x in api.get_transitions_for(j)]]):
            an.append(j)

an = map(api.get_object,an) #NEEDED FOR TITLE CHECK

for i in [x for x in an if 'Nitrogen' not in x.title]:
    api.do_transition_for(i,'retract')
    t.get().commit()
