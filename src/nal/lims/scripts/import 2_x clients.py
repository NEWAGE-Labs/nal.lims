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

path = '/home/naladmin/NAL/LIMS/src/nal.lims/src/nal/lims/scripts/migration data/'
clients = pd.read_csv(path + 'basic_clients_export.csv', keep_default_na=False, dtype=str)

for i, row in clients.iterrows():
    # address = {'country':row['Country'], 'state':row['State'], 'district':row['District'],'city':row['City'],'zip':row['Zip'],'address':row['Address']}
    thisclient = api.create(portal.clients,
                "Client",
                id='importclient'+str(i),
                ClientID=row['NAL Number'],
                title=row['Client ID'],
                Name=row['Client ID'],
                # EmailAddress=row['Email Address'],
                # Phone=row['Phone'],
                # MBGGrowerNumber=row['Grower Number'],
                # PhysicalAddress = address,
                # PostalAddress = address,
                # BillingAddress = address
                )
    thisclient.reindexObject()
