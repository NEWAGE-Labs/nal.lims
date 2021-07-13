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

analyses = map(api.get_object, api.search({'portal_type':'Analysis'}))
data = []
cols = ['Status',
        'Sample ID',
        'Sample Status'
        'Analysis Name',
        'Analysis Keyword',
        'Method',
        'Analyst',
        'Result',
        'Unit',
        'Inconclusive',

]
for i in analyses:
    thisanalysis = {}
    thisanalysis[cols[0]] = api.get_workflow_status_of(i)
    sample = api.get_parent(i)
    if sample:
        thisanalysis[cols[1]] = sample.id
        thisanalysis[cols[2]] = api.get_workflow_status_of(sample)
    thisanalysis[cols[3]] = i.title
    thisanalysis[cols[4]] = i.id
    method = i.getMethod()
    if method:
        thisanalysis[cols[5]] = method.title
    thisanalysis[cols[6]] = i.getAnalyst()
    thisanalysis[cols[7]] = html.HTMLParser().unescape(i.getFormattedResult())
    thisanalysis[cols[8]] = i.getUnit()
    try:
        thisanalysis[cols[8]] = i.Inconclusive
    except AttributeError:
        thisanalysis[cols[8]] = False
    data.append(thisanalysis)

try:
    with open("analyses_export.csv", 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=cols)
        writer.writeheader()
        for ananalysis in data:
            try:
                writer.writerow(ananalysis)
            except UnicodeEncodeError:
                print(ananalysis)
except IOError:
    print("I/O Error")
