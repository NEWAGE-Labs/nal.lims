from AccessControl import getSecurityManager
from AccessControl.User import UnrestrictedUser
from AccessControl.SecurityManagement import newSecurityManager
from bika.lims import api
import pandas as pd
from DateTime import DateTime
portal = api.get_portal()
me = UnrestrictedUser(getSecurityManager().getUser().getUserName(), '', ['LabManager'], '')
me = me.__of__(portal.acl_users)
newSecurityManager(None, me)

#Get Data
file = "/home/naladmin/Sap Sample Data 7_8_22.csv"
data = pd.read_csv(file,keep_default_na=False,dtype=str)
sdgs = data['SDGID'].to_list()
batches = map(api.get_object,api.search({'portal_type':'Batch','title':sdgs}))
ars = []

pair_objs = map(api.get_object,api.search({'portal_type':'SubGroup',}))
pairs = {}
for i in pair_objs:
    if api.get_workflow_status_of(i) not in ['invalid','cancelled']:
        pairs[api.get_title(i)] = i

for i in batches:
    for j in i.getAnalysisRequests():
        ars.append(j)

for i, row in data.iterrows():
    pair = None
    pairstr = "Pair {}".format(row['Pair'].zfill(2))
    if pairstr in pairs.keys():
        pair = pairs[pairstr]
    else:
        print("NO PAIR")
    for j in ars:
        if j.getBatch().title == row['SDGID'] and j.getClientSampleID() == row['SampleID'] and j.InternalLabID == row['LabID']:
            j.setSubGroup(pair)

for i in ars:
    print("{} {} {}".format(i.getBatch().title+" "+i.InternalLabID, i.ClientSampleID,i.SubGroup.title))
