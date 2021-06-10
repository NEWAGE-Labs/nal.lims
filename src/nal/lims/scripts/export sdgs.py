from AccessControl import getSecurityManager
from AccessControl.User import UnrestrictedUser
from AccessControl.SecurityManagement import newSecurityManager
from bika.lims import api
import csv
portal = api.get_portal()
me = UnrestrictedUser(getSecurityManager().getUser().getUserName(), '', ['LabManager'], '')
me = me.__of__(portal.acl_users)
newSecurityManager(None, me)

sdgs = map(api.get_object, api.search({'portal_type':'Batch'}))
data = []
cols = ['Batch ID','Title','Client Batch ID', 'Client Number', 'Client Name', 'SDG Received Date/Time', 'Incubation Date/Time']
for i in sdgs:
    thissdg = {}
    thissdg[cols[0]] = i.id
    thissdg[cols[1]] = i.title
    thissdg[cols[2]] = i.ClientBatchID
    thissdg[cols[3]] = i.getClient().ClientID
    thissdg[cols[4]] = i.getClient().Name
    thissdg[cols[5]] = i.BatchDate
    thissdg[cols[6]] = i.DateTimeIn
    if thissdg[cols[5]]:
        thissdg[cols[5]] = thissdg[cols[5]].strftime('%m/%d/%Y %H:%M')
    if thissdg[cols[6]]:
        thissdg[cols[6]] = thissdg[cols[6]].strftime('%m/%d/%Y %H:%M')
    data.append(thissdg)

try:
    with open("sdg_export.csv", 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=cols)
        writer.writeheader()
        for asdg in data:
            try:
                writer.writerow(asdg)
            except UnicodeEncodeError:
                print(asdg)
except IOError:
    print("I/O Error")
