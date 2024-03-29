from AccessControl import getSecurityManager
from AccessControl.User import UnrestrictedUser
from AccessControl.SecurityManagement import newSecurityManager
from bika.lims import api
import pandas as pd
import csv
portal = api.get_portal()
me = UnrestrictedUser(getSecurityManager().getUser().getUserName(), '', ['LabManager'], '')
me = me.__of__(portal.acl_users)
newSecurityManager(None, me)

sdgs = pd.read_csv('migration data/sdg_export.csv')

# sdgs = map(api.get_object, api.search({'portal_type':'Batch'}))
# data = []
# cols = ['Status',
#         'Batch ID',
#         'ProjectName',
#         'Client Number',
#         'Client Name',
#         'Client Status',
#         'SDG Received Date',
#         'SDG Received Time',
#         'Project Contact',
#         'Sampled By',
#         'Report Contact',
#         'Labels',
#         'Notes',
#
# ]
#
# for i in sdgs:
#     thissdg = {}
#     thissdg[cols[0]] = api.get_workflow_status_of(i)
#     thissdg[cols[1]] = i.id
#     thissdg[cols[2]] = i.title
#     client = i.getClient()
#     if client:
#         try:
#             thissdg[cols[3]] = client.ClientID
#         except AttributeError:
#             thissdg[cols[3]] = ''
#         try:
#             thissdg[cols[4]] = client.Name
#         except AttributeError:
#             thissdg[cols[4]] = ''
#         try:
#             thissdg[cols[5]] = api.get_workflow_status_of(client)
#         except AttributeError:
#             thissdg[cols[5]] = ''
#     thissdg[cols[6]] = i.SDGDate.Date()
#     thissdg[cols[7]] = i.SDGTime
#     thissdg[cols[8]] = i.getReferences(relationship="SDGProjectContact")[0].getFullname()
#     thissdg[cols[9]] = i.getReferences(relationship="SDGSamplerContact")[0].getFullname()
#     thissdg[cols[10]] = i.ReportContact
#     thissdg[cols[11]] = ";".join(i.getLabelNames())
#     thissdg[cols[12]] = i['description']
#     data.append(thissdg)
#
# try:
#     with open("sdg_export.csv", 'w') as csvfile:
#         writer = csv.DictWriter(csvfile, fieldnames=cols)
#         writer.writeheader()
#         for asdg in data:
#             try:
#                 writer.writerow(asdg)
#             except UnicodeEncodeError:
#                 print(asdg)
# except IOError:
#     print("I/O Error")
