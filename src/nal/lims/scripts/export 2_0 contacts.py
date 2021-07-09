from AccessControl import getSecurityManager
from AccessControl.User import UnrestrictedUser
from AccessControl.SecurityManagement import newSecurityManager
from bika.lims import api
import csv
portal = api.get_portal()
me = UnrestrictedUser(getSecurityManager().getUser().getUserName(), '', ['LabManager'], '')
me = me.__of__(portal.acl_users)
newSecurityManager(None, me)

contacts = map(api.get_object, api.search({'portal_type':'Contact'}))
data = []
cols = ['Client Number','Client Name','First Name','Middle Name','Surname','Initials','Email Address','Business Phone', 'Home Phone', 'Mobile Phone']
for i in contacts:
    thiscontact = {}
    thiscontact[cols[0]] = api.get_parent(i).ClientID
    thiscontact[cols[1]] = api.get_parent(i).Name
    thiscontact[cols[2]] = i.Firstname
    thiscontact[cols[3]] = i.Middlename
    thiscontact[cols[4]] = i.Surname
    thiscontact[cols[5]] = i.Initial
    thiscontact[cols[6]] = i.EmailAddress
    thiscontact[cols[7]] = i.BusinessPhone
    thiscontact[cols[8]] = i.HomePhone
    thiscontact[cols[9]] = i.MobilePhone
    data.append(thiscontact)

try:
    with open("contacts_export.csv", 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=cols)
        writer.writeheader()
        for acontact in data:
            try:
                writer.writerow(acontact)
            except UnicodeEncodeError:
                print(acontact)
except IOError:
    print("I/O Error")
