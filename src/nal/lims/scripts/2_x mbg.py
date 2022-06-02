from AccessControl import getSecurityManager
from AccessControl.User import UnrestrictedUser
from AccessControl.SecurityManagement import newSecurityManager
from bika.lims import api
import csv
import HTMLParser as html
portal = api.get_portal()
me = UnrestrictedUser(getSecurityManager().getUser().getUserName(), '', ['LabManager'], '')
me = me.__of__(portal.acl_users)
newSecurityManager(None, me)
from datetime import datetime

def get_state(state):
    state_dict= {
    'ALABAMA': 'AL',
    'ALASKA': 'AK',
    'AMERICAN SAMOA': 'AS',
    'ARIZONA': 'AZ',
    'ARKANSAS': 'AR',
    'CALIFORNIA': 'CA',
    'COLORADO': 'CO',
    'CONNECTICUT': 'CT',
    'DELAWARE': 'DE',
    'DISTRICT OF COLUMBIA': 'DC',
    'FLORIDA': 'FL',
    'GEORGIA': 'GA',
    'GUAM': 'GU',
    'HAWAII': 'HI',
    'IDAHO': 'ID',
    'ILLINOIS': 'IL',
    'INDIANA': 'IN',
    'IOWA': 'IA',
    'KANSAS': 'KS',
    'KENTUCKY': 'KY',
    'LOUISIANA': 'LA',
    'MAINE': 'ME',
    'MARYLAND': 'MD',
    'MASSACHUSETTS': 'MA',
    'MICHIGAN': 'MI',
    'MINNESOTA': 'MN',
    'MISSISSIPPI': 'MS',
    'MISSOURI': 'MO',
    'MONTANA': 'MT',
    'NEBRASKA': 'NE',
    'NEVADA': 'NV',
    'NEW HAMPSHIRE': 'NH',
    'NEW JERSEY': 'NJ',
    'NEW MEXICO': 'NM',
    'NEW YORK': 'NY',
    'NORTH CAROLINA': 'NC',
    'NORTH DAKOTA': 'ND',
    'NORTHERN MARIANA IS': 'MP',
    'OHIO': 'OH',
    'OKLAHOMA': 'OK',
    'OREGON': 'OR',
    'PENNSYLVANIA': 'PA',
    'PUERTO RICO': 'PR',
    'RHODE ISLAND': 'RI',
    'SOUTH CAROLINA': 'SC',
    'SOUTH DAKOTA': 'SD',
    'TENNESSEE': 'TN',
    'TEXAS': 'TX',
    'UTAH': 'UT',
    'VERMONT': 'VT',
    'VIRGINIA': 'VA',
    'VIRGIN ISLANDS': 'VI',
    'WASHINGTON': 'WA',
    'WEST VIRGINIA': 'WV',
    'WISCONSIN': 'WI',
    'WYOMING': 'WY',
    'BRITISH COLUMBIA': 'BC',
    }
    abbrev = None
    if state is not None and state.upper() in state_dict:
        abbrev = state_dict[state.upper()]
    if abbrev is not None:
        state = abbrev
    return state

def get_result(analysis):
    if analysis == '':
        return ''
    result = analysis.getResult()
    choices = analysis.getResultOptions()
    if choices:
        # Create a dict for easy mapping of result options
        values_texts = dict(map(
            lambda c: (str(c["ResultValue"]), c["ResultText"]), choices
        ))
        # Result might contain a single result option
        match = values_texts.get(str(result))
        if match:
            return match
    return analysis.getFormattedResult()

sdgs = map(api.get_object, api.search({'portal_type':'Batch'}))
this_batch = []
for i in sdgs:
    if 'Send to MBG' in i.getLabelNames() and api.get_workflow_status_of(i) == 'open':
        this_batch.append(i)

ars = []
analyses = []
for i in this_batch:
    for j in i.getAnalysisRequests():
        if api.get_workflow_status_of(j) not in ['retracted','rejected','invalid','cancelled']:
            ars.append(j)
            for k in j.getAnalyses():
                if api.get_workflow_status_of(api.get_object(k)) not in ['retracted','rejected','invalid','cancelled']:
                    analyses.append(api.get_object(k))
print("Starting Analysis List")

for i in analyses:
    print(i.id)

print("Ending Analysis List")

data = []
cols = ['Sample Type',
        'Supplier Type',
        'Supplier ID',
        'Sample Location Address',
        'Sample Location City',
        'Sample Location State',
        'Source Type',
        'Source ID',
        'Retest of Sample',
        'Collection Date',
        'Collection Time',
        'Collected By',
        'Lab Name',
        'Received Date',
        'Received Time',
        'Sample ID',
        'Test Date',
        'Test Time',
        'Coliforms',
        'Ecoli',
        'Salmonella',
        'Listeria',
        'Nitrate',
        'Nitrite',
        'Mold',
        'Yeast',
        'Enterobactereacea',
        'Aerobic/Total Plate Count',
        'Geomen',
        'STV',
]
for i in ars:
    thissample = {}
    #Sample Type
    thissample[cols[0]] = 'W'
    #Supplier Type
    thissample[cols[1]] = 'G'
    #Supplier ID
    thissample[cols[2]] = i.getClient().MBGGrowerNumber
    #Sample Location Address
    thissample[cols[3]] = i.getClient().getPhysicalAddress()['address']
    #Sample Location
    thissample[cols[4]] = i.getClient().getPhysicalAddress()['city']
    #State
    thissample[cols[5]] = get_state(i.getClient().getPhysicalAddress()['state'])
    #Source Type
    thissample[cols[6]] = i.getSamplePoint().MBGType
    #Source ID
    thissample[cols[7]] = i.getClientSampleID()
    #Retest of Sample
    thissample[cols[8]] = ''
    #Collection Date
    thissample[cols[9]] = i.DateOfSampling.strftime("%m/%d/%Y")
    #Collection Time
    thissample[cols[10]] = i.TimeOfSampling
    #Collected By
    thissample[cols[11]] = i.getBatch().getReferences(relationship="SDGSamplerContact")[0].getFullname()
    #Lab Name
    thissample[cols[12]] = "NEW AGE LABORATORIES"
    #Received Date
    thissample[cols[13]] = i.getBatch().SDGDate
    #Received Time
    thissample[cols[14]] = i.getBatch().SDGTime
    #Sample ID
    thissample[cols[15]] = i.id
    #Test Date
    thissample[cols[16]] = i.DateReceived.strftime("%m/%d/%Y")
    #Test Time
    thissample[cols[17]] = i.DateReceived.strftime("%H:%M")
    an = []
    for j in i.getAnalyses():
        if api.get_workflow_status_of(j) not in ['rejected','retracted','invalid','cancelled']:
            an.append(api.get_object(j))
    coliform = ''
    ecoli = ''
    salm = ''
    list = ''
    no3 = ''
    no2 = ''
    mold = ''
    yeast = ''
    entero = ''
    apc = ''
    geomen = ''
    stv = ''
    for j in an:
        if 'drinking_coliform_pa' in j.id:
            coliform = j
        elif 'surface_coliform_mpn' in j.id:
            coliform = j
        elif 'drinking_ecoli_pa' in j.id:
            ecoli = j
        elif 'surface_coli_mpn' in j.id or 'surface_ecoli_mpn' in j.id:
            ecoli = j
        elif 'drinking_nitrate' in j.id:
            no2 = j
        elif 'drinking_nitrite' in j.id:
            no3 = j
    #Coliform
    thissample[cols[18]] = get_result(coliform)
    #Ecoli
    thissample[cols[19]] = get_result(ecoli)
    #Salmonella
    thissample[cols[20]] = get_result(salm)
    #Listeria
    thissample[cols[21]] = get_result(list)
    #Nitrate
    thissample[cols[22]] = get_result(no3)
    #Nitrite
    thissample[cols[23]] = get_result(no2)
    #Mold
    thissample[cols[24]] = get_result(mold)
    #Yeast
    thissample[cols[25]] = get_result(yeast)
    #Enterobactereacea
    thissample[cols[26]] = get_result(entero)
    #Aerobic/Total Plate Count
    thissample[cols[27]] = get_result(apc)
    #Geomen
    thissample[cols[28]] = get_result(geomen)
    #STV
    thissample[cols[29]] = get_result(stv)
    data.append(thissample)



# for i in analyses:
#     thisanalysis = {}
#     thisanalysis[cols[0]] = api.get_workflow_status_of(i)
#     sample = api.get_parent(i)
#     if sample:
#         thisanalysis[cols[1]] = sample.id
#         thisanalysis[cols[2]] = api.get_workflow_status_of(sample)
#     thisanalysis[cols[3]] = i.title
#     thisanalysis[cols[4]] = i.id
#     method = i.getMethod()
#     if method:
#         thisanalysis[cols[5]] = method.title
#     thisanalysis[cols[6]] = i.getAnalyst()
#     thisanalysis[cols[7]] = html.HTMLParser().unescape(i.getFormattedResult())
#     thisanalysis[cols[8]] = i.getUnit()
#     try:
#         thisanalysis[cols[9]] = i.Inconclusive
#     except AttributeError:
#         thisanalysis[cols[9]] = False
#     data.append(thisanalysis)
#
try:
    with open("mbg_export.csv", 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=cols)
        writer.writeheader()
        for ananalysis in data:
            try:
                writer.writerow(ananalysis)
            except UnicodeEncodeError:
                print(ananalysis)
except IOError:
    print("I/O Error")
