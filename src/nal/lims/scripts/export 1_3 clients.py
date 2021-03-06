from AccessControl import getSecurityManager
from AccessControl.User import UnrestrictedUser
from AccessControl.SecurityManagement import newSecurityManager
from bika.lims import api
import csv
portal = api.get_portal()
me = UnrestrictedUser(getSecurityManager().getUser().getUserName(), '', ['LabManager'], '')
me = me.__of__(portal.acl_users)
newSecurityManager(None, me)

clients = map(api.get_object, api.search({'portal_type':'Client'}))
data = []
cols = ['NAL Number','Client ID','Email Address','Phone','Grower Number','Country','State','District','City','Zip','Address']
for i in clients:
    thisclient = {}
    thisclient[cols[0]] = i.ClientID
    thisclient[cols[1]] = i.Name
    thisclient[cols[2]] = i.EmailAddress
    thisclient[cols[3]] = i.Phone
    thisclient[cols[4]] = i.TaxNumber
    thisclient[cols[5]] = i.PhysicalAddress['country']
    thisclient[cols[6]] = i.PhysicalAddress['state']
    thisclient[cols[7]] = i.PhysicalAddress['district']
    thisclient[cols[8]] = i.PhysicalAddress['city']
    thisclient[cols[9]] = i.PhysicalAddress['zip']
    thisclient[cols[10]] = i.PhysicalAddress['address']
    data.append(thisclient)

try:
    with open("clients_export.csv", 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=cols)
        writer.writeheader()
        for aclient in data:
            try:
                writer.writerow(aclient)
            except UnicodeEncodeError:
                print(aclient)
except IOError:
    print("I/O Error")
