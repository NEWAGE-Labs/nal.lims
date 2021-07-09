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
cols = ['Batch ID', 'ProjectName', 'Client Number', 'Client Name', 'SDG Received Date', 'SDG Received Time', 'Project Contact', 'Sampled By', 'Report Contact', 'Labels', 'Notes']
for i in sdgs:
    thissdg = {}
    thissdg[cols[0]] = i.id
    thissdg[cols[1]] = i.title
    thissdg[cols[2]] = i.getClient().ClientID
    thissdg[cols[3]] = i.getClient().Name
    thissdg[cols[4]] = i.SDGDate.Date()
    thissdg[cols[5]] = i.SDGTime
    thissdg[cols[6]] = i.getReferences(relationship="SDGProjectContact")[0].getFullname()
    thissdg[cols[7]] = i.getReferences(relationship="SDGSamplerContact")[0].getFullname()
    thissdg[cols[8]] = i.ReportContact
    thissdg[cols[9]] = ";".join(i.getLabelNames())
    thissdg[cols[10]] = i['description']
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
