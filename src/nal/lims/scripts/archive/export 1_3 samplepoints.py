from AccessControl import getSecurityManager
from AccessControl.User import UnrestrictedUser
from AccessControl.SecurityManagement import newSecurityManager
from bika.lims import api
import csv
portal = api.get_portal()
me = UnrestrictedUser(getSecurityManager().getUser().getUserName(), '', ['LabManager'], '')
me = me.__of__(portal.acl_users)
newSecurityManager(None, me)

points = map(api.get_object, api.search({'portal_type':'SamplePoint'}))
data = []
cols = ['Client Number','Client Name','title']
for i in points:
    thispoint = {}
    thispoint[cols[0]] = api.get_parent(i).ClientID
    thispoint[cols[1]] = api.get_parent(i).Name
    thispoint[cols[2]] = i.title
    data.append(thispoint)

try:
    with open("samplepoints_export.csv", 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=cols)
        writer.writeheader()
        for apoint in data:
            try:
                writer.writerow(apoint)
            except UnicodeEncodeError:
                print(apoint)
except IOError:
    print("I/O Error")
