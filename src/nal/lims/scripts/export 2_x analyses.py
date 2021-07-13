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
    thisanalysis[cols[1]] = api.get_parent(i).id
    thisanalysis[cols[2]] = i.title
    thisanalysis[cols[3]] = i.id
    method = i.getMethod()
    if method:
        thisanalysis[cols[4]] = method.title
    thisanalysis[cols[5]] = i.getAnalyst()
    thisanalysis[cols[6]] = html.HTMLParser().unescape(i.getFormattedResult())
    thisanalysis[cols[7]] = i.getUnit()
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
