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

path = '/home/naladmin/pregithub/nalims/src/nal.lims/src/nal/lims/scripts/migration data/'
contacts = pd.read_csv(path + 'contacts_export.csv', keep_default_na=False, dtype=str)
client_objs = map(api.get_object, api.search({'portal_type':'Client'}) )

for i, row in contacts.iterrows():
    matchedclients = []
    for i in client_objs:
        if i.ClientID == row['Client Number'] and i.Name == row['Client Name']:
            matchedclients.append(i)
    if len(matchedclients) < 1:
        print('No client found for: {0} {1}'.format(row['Client Number'], row['Client Name']))
        pass
    elif len(matchedclients) > 1:
        print('Multiple Clients found for: {0} {1}'.format(row['Client Number'], row['Client Name']))
        print(matchedclients)
        pass
    else:
        print('creating contact for: {0} {1} {2} {3} {4} {5}'.format(matchedclients[0].ClientID, matchedclients[0].Name, matchedclients[0],row['First Name'],row['Surname'],row['Phone']))
        thiscontact = api.create(
                matchedclients[0], #Location in site
                "Contact", #Content Type
                #Content-Type specific fields:
                Firstname=row['First Name'],
                Surname=row['Surname'],
                Phone=row['Phone']
                )
        thiscontact.reindexObject()
