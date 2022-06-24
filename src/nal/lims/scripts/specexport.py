from AccessControl import getSecurityManager
from AccessControl.User import UnrestrictedUser
from AccessControl.SecurityManagement import newSecurityManager
from bika.lims import api
portal = api.get_portal()
me = UnrestrictedUser(getSecurityManager().getUser().getUserName(), '', ['LabManager'], '')
me = me.__of__(portal.acl_users)
newSecurityManager(None, me)
import pandas as pd

specs = map(api.get_object,api.search({'portal_type':'AnalysisSpec'}))

names = []
types = []
sugars_min = []
brix_min = []
ph_min = []
ec_min = []
cl_min = []
s_min = []
p_min = []
ca_min = []
k_min = []
mg_min = []
na_min = []
al_min = []
b_min = []
co_min = []
cu_min = []
fe_min = []
mn_min = []
mo_min = []
ni_min = []
se_min = []
si_min = []
zn_min = []
nh4_min = []
no3_min = []
n_min = []
sugars_max = []
brix_max = []
ph_max = []
ec_max = []
cl_max = []
s_max = []
p_max = []
ca_max = []
k_max = []
mg_max = []
na_max = []
al_max = []
b_max = []
co_max = []
cu_max = []
fe_max = []
mn_max = []
mo_max = []
ni_max = []
se_max = []
si_max = []
zn_max = []
nh4_max = []
no3_max = []
n_max = []

tests = [
    ('sap_total_sugar',sugars_min,sugars_max),
    ('sap_brix',brix_min,brix_max),
    ('sap_ph',ph_min,ph_max),
    ('sap_ec',ec_min,ec_max),
    ('sap_chloride',cl_min,cl_max),
    ('sap_sulfur',s_min,s_max),
    ('sap_phosphorous',p_min,p_max),
    ('sap_calcium',ca_min,ca_max),
    ('sap_potassium',k_min,k_max),
    ('sap_magnesium',mg_min,mg_max),
    ('sap_sodium',na_min,na_max),
    ('sap_aluminum',al_min,al_max),
    ('sap_boron',b_min,b_max),
    ('sap_cobalt',co_min,co_max),
    ('sap_copper',cu_min,cu_max),
    ('sap_iron',fe_min,fe_max),
    ('sap_manganese',mn_min,mn_max),
    ('sap_molybdenum',mo_min,mo_max),
    ('sap_nickel',ni_min,ni_max),
    ('sap_selenium',se_min,se_max),
    ('sap_silica',si_min,si_max),
    ('sap_zinc',zn_min,zn_max),
    ('sap_nitrogen_as_ammonium',nh4_min,nh4_max),
    ('sap_nitrogen_as_nitrate',no3_min,no3_max),
    ('sap_total_nitrogen',n_min,n_max),
]

data_cols = [[
    names,
    types
    ],[
    'OL Title',
    'Sample Type'
    ]]
for i in tests:
    data_cols[0].append(i[1])
    data_cols[1].append(i[0]+'_min')
    data_cols[0].append(i[2])
    data_cols[1].append(i[0]+'_max')

for i in specs:
    #Get Spec-level details
    names.append(i.title)
    types.append(i.getSampleType().title)
    kws = [] #Reset keyword list for this spec
    #Get Keyword list for this spec
    for j in i.ResultsRange:
        kws.append(j['keyword'])
    #Iterate through tests
    for j in tests:
        #Check for blanks
        if j[0] not in kws:
            j[1].append('')
            j[2].append('')
        else:
            pass
        #Iterate through analyses to find a match
        for k in i.ResultsRange:
            if k['keyword'] == j[0]:
                    j[1].append(k['min'])
                    j[2].append(k['max'])
            else:
                pass

## CHECK TO ENSURE EACH LIST IS THE SAME LENGTH!

out = pd.DataFrame(data_cols[0]).transpose()
out.columns = data_cols[1]
out.to_csv('June 22 OLs.csv')
