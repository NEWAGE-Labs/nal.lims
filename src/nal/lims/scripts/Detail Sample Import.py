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
import transaction as t

#Get Data
file = "/home/naladmin/sdgs/Sap Details 7_15.csv"
data = pd.read_csv(file,keep_default_na=False,dtype=str)
bad = []
new = []
sdgs = data['SDGID'].to_list()
batches = map(api.get_object,api.search({'portal_type':'Batch','title':sdgs}))
pair_objs = map(api.get_object,api.search({'portal_type':'SubGroup',}))
pairs = {}
type_objs = map(api.get_object,api.search({'portal_type':'SampleType',}))
types = {}

for i in pair_objs:
    if api.get_workflow_status_of(i) not in ['invalid','cancelled']:
        pairs[api.get_title(i)] = i

for i in type_objs:
    if api.get_workflow_status_of(i) not in ['invalid','cancelled']:
        types[api.get_title(i)] = i

saptype = types["Sap"]
hptype = types["Water"]
rstype = types["Soil"]

#Show SDGs found
print("Found the following SDGs:")
for i in batches:
    print(api.get_title(i))

#Iterate through each Sample row in spreadsheet
for i, row in data.iterrows():
    print("row {}. Row:\n{}".format(i,row))
    #Get ID to search Batch for
    SDG = row["SDGID"]
    #Clear variabless
    batch = None
    for i in batches:
        if i.title == SDG:
            batch = i
    #If Batch wasnt found, add it to bad list
    if batch is None:
        bad.append(batch)
    #Else Process it
    else:
        #Clear variables
        test = None
        pair = None
        loc = None
        type=None
        contact = None
        newold = False
        ars = map(api.get_object,batch.getAnalysisRequests())
        client = batch.getClient()
        loc_objs = [x for x in client.objectValues("SamplePoint")]
        locations = {}
        for j in loc_objs:
            if api.get_workflow_status_of(j) not in ['invalid','cancelled']:
                locations[api.get_title(j)] = j
        locstr = row["Location"]
        pairstr = "Pair {}".format(row['Pair'].zfill(2))
        if locstr in locations.keys():
            loc = api.get_uid(locations[locstr])
        else:
            loc = api.create(client, "SamplePoint", title=locstr).UID()
        if pairstr in pairs.keys():
            pair = pairs[pairstr]
        else:
            print("NO PAIR")
        if row['New'] not in [None, '', 'old','whole']:
            newold = True
        project = batch.getReferences(relationship="SDGProjectContact")[0]
        if project is not None:
            contact = project
        else:
            print("NO CONTACT FOUND")
        sample = None
        for i in ars:
            if i.InternalLabID == row['LabID'].zfill(3):
                sample = i
        if sample is None:
            print("NO SAMPLE")
        else:
            sample.ClientSampleID = row["SampleID"]
            if pair is not None:
                sample.setSubGroup(pair)
            sample.NewLeaf = newold
            sample.SamplePoint=loc
            sample.PlantType = row['Crop']
            sample.Variety=row['Variety']
            sample.GrowthStage = row['Growth']
            sample.Vigor=row['Vigor']
            for j in sample.getProfiles():
                if "Sap" in j.title:
                    type = api.get_uid(saptype)
                elif "Rapid Soil (RS)" in j.title:
                    type = api.get_uid(rstype)
                elif "HP-01" in j.title:
                    type = api.get_uid(hptype)
            sample.SampleType=type
            sample.reindexObject()
            t.get().commit()

print("Missing Batches:")
for i in bad:
    print(i)
