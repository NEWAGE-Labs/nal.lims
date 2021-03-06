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
cols = ['Status',
        'Client Number',
        'Client Name',
        'Client Status',
        'Title',
        'Description',
        'Formatted Address',
        'MBG Location Type',
        'WSSN',
        'Attachment Type',
        'Attachment Name'

]
for i in points:
    thispoint = {}
    thispoint[cols[0]] = api.get_workflow_status_of(i)
    client = api.get_parent(i)
    if client:
        try:
            thispoint[cols[1]] = client.ClientID
        except AttributeError:
            thispoint[cols[1]] = ''
        try:
            thispoint[cols[2]] = client.Name
        except AttributeError:
            thispoint[cols[2]] = ''
        try:
            thispoint[cols[3]] = api.get_workflow_status_of(client)
        except AttributeError:
            thispoint[cols[3]] = ''
    thispoint[cols[4]] = i.title
    thispoint[cols[5]] = i['description']
    thispoint[cols[6]] = i.FormattedAddress
    thispoint[cols[7]] = i.MBGType
    thispoint[cols[8]] = i.WSSN
    thispoint[cols[9]] = i.AttachmentFile.content_type
    thispoint[cols[10]] = i.AttachmentFile.filename
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
