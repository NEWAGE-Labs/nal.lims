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
file = "/home/naladmin/sdgs/Samples 7_27.csv"
data = pd.read_csv(file,keep_default_na=False,dtype=str)
bad = []
new = []
sdgs = data['SDGID'].to_list()
batches = map(api.get_object,api.search({'portal_type':'Batch','title':sdgs}))
pair_objs = map(api.get_object,api.search({'portal_type':'SubGroup',}))
pairs = {}
type_objs = map(api.get_object,api.search({'portal_type':'SampleType',}))
types = {}
saptest = api.search({'portal_type':'AnalysisProfile','title':'Sap'})
hptest = api.search({'portal_type':'AnalysisProfile','title':'HP-01'})
rstest = api.search({'portal_type':'AnalysisProfile','title':'Rapid Soil (RS)'})
pttest = api.search({'portal_type':'AnalysisProfile','title':'Plant Tissue'})

for i in pair_objs:
    if api.get_workflow_status_of(i) not in ['invalid','cancelled']:
        pairs[api.get_title(i)] = i

for i in type_objs:
    if api.get_workflow_status_of(i) not in ['invalid','cancelled']:
        types[api.get_title(i)] = i

saptype = types["Sap"]
hptype = types["Water"]
rstype = types["Soil"]
pttype = types["Tissue"]

if saptest == [] or hptest == [] or rstest == [] or pttest == []:
    print("TESTS NOT FOUND")
else:
    saptest = api.get_object(saptest[0])
    hptest = api.get_object(hptest[0])
    rstest = api.get_object(rstest[0])
    pttest = api.get_object(pttest[0])

#Show SDGs found
print("Found the following SDGs:")
for i in batches:
    print(api.get_title(i))

#Iterate through each Sample row in spreadsheet
for i, row in data.iterrows():
    print("row {}. Row:\n{}".format(i,row))
    #Get ID to search Batch for
    SDG = row["SDGID"]
    print(SDG)
    #Clear variabless
    batch = None
    for i in batches:
        if i.title == SDG:
            batch = i
    #If Batch wasnt found, add it to bad list
    if batch is None:
        bad.append(row["SDGID"])
    ars = map(api.get_object,batch.getAnalysisRequests())
    ilid = []
    if ars != []:
        for j in ars:
            ilid.append(j.InternalLabID)
    if row['LabID'].zfill(3) in ilid:
        print("NO GO")
        pass
        #Else Process it
    else:
        #Clear variables
        test = None
        pair = None
        loc = None
        type=None
        contact = None
        newold = False
        client = batch.getClient()
        loc_objs = [x for x in client.objectValues("SamplePoint")]
        locations = {}
        for j in loc_objs:
            if api.get_workflow_status_of(j) not in ['invalid','cancelled']:
                locations[api.get_title(j)] = j
        teststr = row["Test"]
        locstr = row["Location"]
        pairstr = "Pair {}".format(row['Pair'].zfill(2))
        if teststr.lower() == "sap":
            test = saptest
            type = api.get_uid(saptype)
        elif teststr.lower() in ["hp","hp-01","hp01"]:
            test = hptest
            type = api.get_uid(hptype)
        elif teststr.lower() in ["rs","rs-01","rapid soil","rapidsoil"]:
            test = rstest
            type = api.get_uid(rstype)
        elif teststr.lower() in ["tissue","dry tissue","plant tissue","pt"]:
            test = pttest
            type = api.get_uid(pttype)
        else:
            print("NO TEST FOUND FOR {}".format(row["SDGID"] + " " + row["LabID"]))
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
        sample = api.create(client, "AnalysisRequest", CCContact=[project],SampleType=type, Batch=batch, InternalLabID=row['LabID'].zfill(3), ClientSampleID=row["SampleID"],SubGroup = pair, NewLeaf=newold, SamplePoint=loc,DateOfSampling=DateTime(row["Date"]), TimeOfSampling=row["Time"], PlantType=row["Crop"], Variety=row["Variety"], GrowthStage=row["Growth"],Vigor=row["Vigor"])
        api.do_transition_for(sample,"no_sampling_workflow")
        sample.setProfiles(test)
        t.get().commit()

print("Missing Batches:")
for i in bad:
    print(i)
