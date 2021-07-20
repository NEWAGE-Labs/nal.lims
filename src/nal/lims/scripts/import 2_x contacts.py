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
# contacts = map(api.get_object, api.search({'portal_type':'Contact'}))
# data = []
# cols = ['Status',
#         'Client Number',
#         'Client Name',
#         'Client Status',
#         'First Name',
#         'Middle Name',
#         'Surname',
#         'Initials',
#         'Email Address',
#         'Business Phone',
#         'Home Phone',
#         'Mobile Phone',
#
# ]
# for i in contacts:
#     thiscontact = {}
#     thiscontact[cols[0]] = api.get_workflow_status_of(i)
#     client = api.get_parent(i)
#     if client:
#         try:
#             thiscontact[cols[1]] = client.ClientID
#         except AttributeError:
#             thiscontact[cols[1]] = ''
#         try:
#             thiscontact[cols[2]] = client.Name
#         except AttributeError:
#             thiscontact[cols[2]] = ''
#         try:
#             thiscontact[cols[3]] = api.get_workflow_status_of(client)
#         except AttributeError:
#             thiscontact[cols[3]] = ''
#     thiscontact[cols[4]] = i.Firstname
#     thiscontact[cols[5]] = i.Middlename
#     thiscontact[cols[6]] = i.Surname
#     thiscontact[cols[7]] = i.Initials
#     thiscontact[cols[8]] = i.EmailAddress
#     thiscontact[cols[9]] = i.BusinessPhone
#     thiscontact[cols[10]] = i.HomePhone
#     thiscontact[cols[11]] = i.MobilePhone
#     data.append(thiscontact)
#
# try:
#     with open("contacts_export.csv", 'w') as csvfile:
#         writer = csv.DictWriter(csvfile, fieldnames=cols)
#         writer.writeheader()
#         for acontact in data:
#             try:
#                 writer.writerow(acontact)
#             except UnicodeEncodeError:
#                 print(acontact)
# except IOError:
#     print("I/O Error")
