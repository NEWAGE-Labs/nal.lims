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

clients = pd.read_csv('migration data/clients_export.csv')

#Needs Status added in
# raw_cols = ['NAL Number',
#             'Client Name',
#             'Email Address',
#             'Phone',
#             'Grower Number',
#             'Country',
#             'State',
#             'District',
#             'City',
#             'Zip',
#             'Address',
#
# ]
#
# clean_cols = [  'Status',
#                 'NAL Number',
#                 'Client ID',
#                 'Email Address',
#                 'Phone',
#                 'MBG Grower Number',
#                 'TrueBlue Grower Number',
#                 'Grower List',
#                 'Country',
#                 'State',
#                 'District',
#                 'City',
#                 'Zip',
#                 'Address',
#
# ]
for i, row in clients.itterrows():
    thisclient = api.create( portal.clients,
                "Client",
                ClientID=row['NAL Number'],
                EmailAddress=row['Email Address'],
                Phone=row['Phone'],
                MBGGrowerNumber=row['Grower Number'],
                PhysicalAddress['country']=row['Country'],
                PostalAddress['country']=row['Country'],
                BillingAddress['country']=row['Country'],
                PhysicalAddress['state']=row['State'],
                PostalAddress['state']=row['State'],
                BillingAddress['state']=row['State'],
                PhysicalAddress['district']=row['District'],
                PostalAddress['district']=row['District'],
                BillingAddress['district']=row['District'],
                PhysicalAddress['city']=row['City'],
                PostalAddress['city']=row['City'],
                BillingAddress['city']=row['City'],
                PhysicalAddress['zip']=row['Zip'],
                PostalAddress['zip']=row['Zip'],
                BillingAddress['zip']=row['Zip'],
                PhysicalAddress['address']=row['Address'],
                PostalAddress['address']=row['Address'],
                BillingAddress['address']=row['Address']
    )
    thisclient.reindexObject()
