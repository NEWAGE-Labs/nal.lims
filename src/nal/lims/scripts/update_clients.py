from AccessControl import getSecurityManager
from AccessControl.User import UnrestrictedUser
from AccessControl.SecurityManagement import newSecurityManager
from bika.lims import api
import pandas as pd
import csv
import transaction as t
portal = api.get_portal()
me = UnrestrictedUser(getSecurityManager().getUser().getUserName(), '', ['LabManager'], '')
me = me.__of__(portal.acl_users)
newSecurityManager(None, me)

path = '/home/naladmin/NAL/LIMS/src/nal.lims/src/nal/lims/scripts/migration data/'
clients = pd.read_csv(path + 'clients_export.csv', keep_default_na=False, dtype=str)

lims_clients = map(api.get_object,api.search({'portal_type':'Client'}))
this_client = None
for i, row in clients.iterrows():
    lims_clients = map(api.get_object,api.search({'portal_type':'Client'}))
    this_client = None
    for j in lims_clients:
        if row['NAL Number'] == j.ClientID or row['Client ID'] == j.title or row['Client ID'] == j.Name:
            this_client = j
        else:
            pass
    if this_client is not None:
        this_client.EmailAddress = row['Email Address']
        this_client.Phone = row['Phone']
        this_client.MBGGrowerNumber = row['Grower Number']
        this_client.PhysicalAddress['country'] = row['Country']
        this_client.PhysicalAddress['state'] = row['State']
        this_client.PhysicalAddress['district'] = row['District']
        this_client.PhysicalAddress['city'] = row['City']
        this_client.PhysicalAddress['zip'] = row['Zip']
        this_client.PhysicalAddress['address'] = row['Address']
    else:
        address = {'country':row['Country'], 'state':row['State'], 'district':row['District'],'city':row['City'],'zip':row['Zip'],'address':row['Address']}
        this_client = api.create(portal.clients,
                    "Client",
                    ClientID=row['NAL Number'],
                    title=row['Client ID'],
                    Name=row['Client ID'],
                    EmailAddress=row['Email Address'],
                    Phone=row['Phone'],
                    MBGGrowerNumber=row['Grower Number'],
                    PhysicalAddress=address
                    )
    this_client.reindexObject()

t.get().commit()

lims_clients = map(api.get_object,api.search({'portal_type':'Client'}))
this_client = None
contacts = pd.read_csv(path + 'contacts_export.csv', keep_default_na=False, dtype=str)
for i, row in contacts.iterrows():
    this_contact = None
    this_client = None
    for j in lims_clients:
        if row['Client Number'] == j.ClientID or row['Client Name'] == j.title or row['Client Name'] == j.Name:
            this_client = j
        else:
            pass
    if this_client is not None:
        this_contact = api.create(
            this_client,
            'Contact',
            Firstname = row['First Name'],
            Surname = row['Surname'],
            Phone = row['Phone']
            )
    this_contact.reindexObject()

t.get().commit()

locations = pd.read_csv(path + 'samplepoints_export.csv', keep_default_na=False, dtype=str)
lims_clients = map(api.get_object,api.search({'portal_type':'Client'}))
this_client = None
for i, row in locations.iterrows():
    this_location = None
    this_client = None
    for j in lims_clients:
        if row['Client Number'] == j.ClientID or row['Client Name'] == j.title or row['Client Name'] == j.Name:
            this_client = j
        else:
            pass
    if this_client is not None:
        this_location = api.create(
            this_client,
            'SamplePoint',
            title=row['title'].replace('"','')
            )
    this_location.reindexObject()

    # address = {'country':row['Country'], 'state':row['State'], 'district':row['District'],'city':row['City'],'zip':row['Zip'],'address':row['Address']}
    # thisclient = api.create(portal.clients,
    #             "Client",
    #             id='importedclient-'+str(i),
    #             ClientID=row['NAL Number'],
    #             title=row['Client Name'],
    #             Name=row['Client Name'],
    #             # EmailAddress=row['Email Address'],
    #             # Phone=row['Phone'],
    #             # MBGGrowerNumber=row['Grower Number'],
    #             # PhysicalAddress = address,
    #             # PostalAddress = address,
    #             # BillingAddress = address
    #             )
    # thisclient.reindexObject()

t.get().commit()
