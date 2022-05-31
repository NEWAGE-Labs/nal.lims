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
# samples = map(api.get_object, api.search({'portal_type':'AnalysisRequest'}))
# data = []
# cols = ['Status',
#         'Sample ID',
#         'Client Sample ID',
#         'Internal Lab ID',
#         'Sample Type',
#         'Date Sampled',
#         'Time Sampled',
#         'Client Number',
#         'Client Name',
#         'Project Contact',
#         'Sampler Contact',
#         'Reported To',
#         'Batch ID',
#         'Batch Title',
#         'Sample Point Title',
#         'Sample Point Address',
#         'Sample Point MBG Type',
#         'Sample Point WSSN',
#         'Plant Type',
#         'Variety',
#         'Growth Stage',
#         'New Leaf',
#
# ]
# for i in samples:
#     thissample = {}
# ##Sample Fields
#     #Status
#     thissample[cols[0]] = api.get_workflow_status_of(i)
#     #Sample ID
#     thissample[cols[1]] = i.id
#     #Internal Lab ID
#     try:
#         thissample[cols[2]] = i.InternalLabID
#     except AttributeError:
#         thissample[cols[2]] = ''
#     #Client Sample ID
#     thissample[cols[3]] = i.ClientSampleID
#     #Sample Type
#     type = i.getSampleType()
#     if type:
#         thissample[cols[4]] = type.title
#     #Date of Sampling
#     thissample[cols[5]] = i.DateOfSampling.Date()
#     #Time Of Sampling
#     thissample[cols[6]] = i.TimeOfSampling
# ##Client Fields
#     #Client Number
#     thissample[cols[7]] = i.getClient().ClientID
#     #Client Name
#     thissample[cols[8]] = i.getClient().Name
# ##Batch Fields
#     batch = i.getBatch()
#     if batch:
#     #Project Contact
#         projectcontact = batch.getReferences(relationship="SDGProjectContact")
#         if projectcontact:
#             thissample[cols[9]] = projectcontact[0].getFullname()
#     #Sampler
#         sampler = batch.getReferences(relationship="SDGSamplerContact")
#         if sampler:
#             thissample[cols[10]] = sampler[0].getFullname()
#     #Reported To
#         thissample[cols[11]] = batch.ReportContact
#     #Batch ID
#         thissample[cols[12]] = batch.id
#     #Batch Title
#         thissample[cols[13]] = batch.title
# ##Sample Point Fields
#     point = i.getSamplePoint()
#     if point:
#     #Sample Point Title
#         thissample[cols[14]] = point.title
#     #Sample Point Address
#         thissample[cols[15]] = point.FormattedAddress
#     #Sample Point MBG Type
#         thissample[cols[16]] = point.WaterSourceType
#     #Sample Point WSSN
#         thissample[cols[17]] = point.WSSN
# ##Sap Fields
#     #Plant Type
#     thissample[cols[18]] = i.PlantType
#     #Variety
#     thissample[cols[19]] = i.Variety
#     #Growth Stage
#     thissample[cols[20]] = i.GrowthStage
#     #New Leaf
#     thissample[cols[21]] = i.NewLeaf
#     data.append(thissample)
#
# try:
#     with open("samples_export.csv", 'w') as csvfile:
#         writer = csv.DictWriter(csvfile, fieldnames=cols)
#         writer.writeheader()
#         for asample in data:
#             try:
#                 writer.writerow(asample)
#             except UnicodeEncodeError:
#                 print(asample)
# except IOError:
#     print("I/O Error")
