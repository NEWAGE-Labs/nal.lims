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
file = "/home/naladmin/sdgs/Sap SDG Data 7_27.csv"
data = pd.read_csv(file,keep_default_na=False,dtype=str)
clients = map(api.get_object,api.search({"portal_type":"Client"}))
bad = []
new = []
#Iterate through each SDG row in spreadsheet
for i, row in data.iterrows():
    print("row {}. Row:\n{}".format(i,row))
    #Get ID to search Client for
    NAL = row["NALID"]
    #Clear variabless
    client = None
    #Search through list of clients in memory for an NAL# Match
    for j in clients:
        if j.getClientID() == NAL:
            client = j
            break
        else:
            pass
    #If client wasnt found, add it to bad list
    if client is None and NAL not in bad:
        bad.append(NAL)
    #Else Process it
    elif NAL in bad:
        pass
    else:
        #Clear variables
        contacts = None
        project = None
        sampler = None
        grower = None
        date = None
        time = None
        date = row['SDGID'][0:2]+'/'+row['SDGID'][2:4]+'/'+row['SDGID'][4:6]
        time = row['SDGID'][6:8]+':'+row['SDGID'][8:10]
        pname = row["Project"].split()
        sname = row["Sampler"].split()
        gname = row["Grower"].split()
        #Iterate through contacts
        contacts = client.getContacts()
        for j in contacts:
            if project is None and (pname[0].lower() in j.getFirstname().lower() and pname[1].lower() in j.getSurname().lower()):
                print("PROJECT MATCH")
                project = j
            if sampler is None and (sname[0].lower() in j.getFirstname().lower() and sname[1].lower() in j.getSurname().lower()):
                print("SAMPLER MATCH")
                sampler = j
            if grower is None and (row["Grower"] != '' and (gname[0].lower() in j.getFirstname().lower() and (len(gname) == 1 or gname[1].lower() in j.getSurname().lower()))):
                print("GROWER MATCH")
                grower = j
        #If the contacts didn't exist, create them.
        if project is None:
            new.append(row["Project"])
            project = api.create(client, "Contact",Firstname=sname[0],Surname=' '.join(sname[1:]))
        if sampler is None:
            if row['Sampler'] == row['Project']:
                sampler = project
            else:
                new.append(row["Sampler"])
                sampler = api.create(client, "Contact",Firstname=sname[0],Surname=' '.join(sname[1:]))
        if grower is None and row["Grower"] != '':
            if row["Grower"] == row['Sampler']:
                grower = sampler
            elif row["Grower"] == row['Project']:
                grower = project
            else:
                new.append(row["Grower"])
                grower = api.create(client, "Contact",Firstname=gname[0],Surname=' '.join(gname[1:]))
        #Print Details:
        print(client)
        print("NAL: {}\nProject: {}\nSampler: {}\nGrower: {}".format(NAL,project,sampler,grower))
        #Create Batch
        api.create(client, "Batch", title=row["SDGID"], SDGDate=DateTime(date), SDGTime=time, ProjectContact=project, SamplerContact=sampler, GrowerContact=grower)

print("Missing Clients:")
for i in bad:
    print(i)
