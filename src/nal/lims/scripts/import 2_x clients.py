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
#
# clients = map(api.get_object, api.search({'portal_type':'Client'}))
# data = []
# cols = ['Status',
#         'NAL Number',
#         'Client ID',
#         'Email Address',
#         'Phone',
#         'MBG Grower Number',
#         'TrueBlue Grower Number',
#         'Grower List',
#         'Country',
#         'State',
#         'District',
#         'City',
#         'Zip',
#         'Address',
#
# ]
# for i in clients:
#     thisclient = {}
#     thisclient[cols[0]] = api.get_workflow_status_of(i)
#     thisclient[cols[1]] = i.ClientID
#     thisclient[cols[2]] = i.Name
#     thisclient[cols[3]] = i.EmailAddress
#     thisclient[cols[4]] = i.Phone
#     thisclient[cols[5]] = i.MBGGrowerNumber
#     thisclient[cols[6]] = i.TBGrowerNumber
#     distributor_client_numbers = []
#     for j in i.getReferences(relationship="ClientDistributor"):
#         distributor_client_numbers.append(j.ClientID)
#     thisclient[cols[7]] = ";".join(distributor_client_numbers)
#     thisclient[cols[8]] = i.PhysicalAddress['country']
#     thisclient[cols[9]] = i.PhysicalAddress['state']
#     thisclient[cols[10]] = i.PhysicalAddress['district']
#     thisclient[cols[11]] = i.PhysicalAddress['city']
#     thisclient[cols[12]] = i.PhysicalAddress['zip']
#     thisclient[cols[13]] = i.PhysicalAddress['address']
#     data.append(thisclient)
#
# try:
#     with open("clients_export.csv", 'w') as csvfile:
#         writer = csv.DictWriter(csvfile, fieldnames=cols)
#         writer.writeheader()
#         for aclient in data:
#             try:
#                 writer.writerow(aclient)
#             except UnicodeEncodeError:
#                 print(aclient)
# except IOError:
#     print("I/O Error")
