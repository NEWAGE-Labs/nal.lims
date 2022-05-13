from AccessControl import getSecurityManager
from AccessControl.User import UnrestrictedUser
from AccessControl.SecurityManagement import newSecurityManager
from bika.lims import api
import csv
import HTMLParser as html
portal = api.get_portal()
me = UnrestrictedUser(getSecurityManager().getUser().getUserName(), '', ['LabManager'], '')
me = me.__of__(portal.acl_users)
newSecurityManager(None, me)

sdgs = map(api.get_object, api.search({'portal_type':'Batch'}))
this_batch = []
for i in sdgs:
    if 'Send to MBG' in i.getLabelNames() and api.get_workflow_status_of(i) == 'open':
        this_batch.append(i)

analyses = []
for i in this_batch:
    for j in i.getAnalysisService():
        analyses.append(j)
print("Starting Analysis List")
for i in analyses:
    print(i.id)
print("Ending Analysis List")

data = []
cols = ['Sample Type',
        'Supplier Type',
        'Supplier ID',
        'Sample Location Address',
        'Sample Location City',
        'Sample Location State',
        'Source Type',
        'Source ID',
        'Retest of Sample',
        'Collection Date',
        'Collection Time',
        'Collected By',
        'Lab Name',
        'Received Date',
        'Received Time',
        'Sample ID',
        'Test Date',
        'Test Time',
        'Coliforms',
        'Ecoli',
        'Salmonella',
        'Listeria',
        'Nitrate',
        'Nitrite',
        'Mold',
        'Yeast',
        'Enterobactereacea',
        'Aerobic/Total Plate Count',
        'Geomen',
        'STV',
]
# for i in analyses:
#     thisanalysis = {}
#     thisanalysis[cols[0]] = api.get_workflow_status_of(i)
#     sample = api.get_parent(i)
#     if sample:
#         thisanalysis[cols[1]] = sample.id
#         thisanalysis[cols[2]] = api.get_workflow_status_of(sample)
#     thisanalysis[cols[3]] = i.title
#     thisanalysis[cols[4]] = i.id
#     method = i.getMethod()
#     if method:
#         thisanalysis[cols[5]] = method.title
#     thisanalysis[cols[6]] = i.getAnalyst()
#     thisanalysis[cols[7]] = html.HTMLParser().unescape(i.getFormattedResult())
#     thisanalysis[cols[8]] = i.getUnit()
#     try:
#         thisanalysis[cols[9]] = i.Inconclusive
#     except AttributeError:
#         thisanalysis[cols[9]] = False
#     data.append(thisanalysis)
#
# try:
#     with open("analyses_export.csv", 'w') as csvfile:
#         writer = csv.DictWriter(csvfile, fieldnames=cols)
#         writer.writeheader()
#         for ananalysis in data:
#             try:
#                 writer.writerow(ananalysis)
#             except UnicodeEncodeError:
#                 print(ananalysis)
# except IOError:
#     print("I/O Error")
