from AccessControl import getSecurityManager
from AccessControl.User import UnrestrictedUser
from AccessControl.SecurityManagement import newSecurityManager
from bika.lims import api
import csv
portal = api.get_portal()
me = UnrestrictedUser(getSecurityManager().getUser().getUserName(), '', ['LabManager'], '')
me = me.__of__(portal.acl_users)
newSecurityManager(None, me)

samples = map(api.get_object, api.search({'portal_type':'AnalysisRequest'}))
data = []
cols = ['Sample ID','Client Number','Client Name','Contact First Name', \
        'Contact Last Name','Date/Time Sampled','Batch ID','Batch Title', \
        'Sample Type','Sample Point', 'Internal Lab ID', \
        'Client Sample ID', 'Reported To', 'Collected By']
for i in samples:
    thissample = {}
    thissample[cols[0]] = i.id
    thissample[cols[1]] = i.getClient().ClientID
    thissample[cols[2]] = i.getClient().Name
    thissample[cols[3]] = i.getContact().Firstname
    thissample[cols[4]] = i.getContact().Surname
    thissample[cols[5]] = i.DateSampled
    if thissample[cols[5]]:
        thissample[cols[5]] = thissample[cols[5]].strftime('%m/%d/%Y %H:%M')
    thissample[cols[6]] = i.getBatch()
    if thissample[cols[6]]:
        thissample[cols[6]] = thissample[cols[6]].id
    thissample[cols[7]] = i.getBatch()
    if thissample[cols[7]]:
        thissample[cols[7]] = thissample[cols[7]].title
    thissample[cols[8]] = i.getSampleType()
    if thissample[cols[8]]:
        thissample[cols[8]] = thissample[cols[8]].title
    thissample[cols[9]] = i.getSamplePoint()
    if thissample[cols[9]]:
        thissample[cols[9]] = thissample[cols[9]].title
    thissample[cols[10]] = thissample[cols[7]]
    if thissample[cols[10]]:
        thissample[cols[10]] = thissample[cols[10]] + '-' + i.ClientReference
    thissample[cols[11]] = i.ClientSampleID
    thissample[cols[12]] = i.ReportContact
    thissample[cols[13]] = i.CollectedBy
    data.append(thissample)

try:
    with open("samples_export.csv", 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=cols)
        writer.writeheader()
        for asample in data:
            try:
                writer.writerow(asample)
            except UnicodeEncodeError:
                print(asample)
except IOError:
    print("I/O Error")
