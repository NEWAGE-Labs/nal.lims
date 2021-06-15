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
cols = ['Client Number','Client Name','First Name','Surname','Phone']
for i in contacts:
    thiscontact = {}
    thiscontact[cols[0]] = api.get_parent(i).ClientID
    thiscontact[cols[1]] = api.get_parent(i).Name
    thiscontact[cols[2]] = i.Firstname
    thiscontact[cols[3]] = i.Surname
    thiscontact[cols[4]] = i.Phone
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
