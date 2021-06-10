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
cols = ['Sample ID', 'Analysis Name', 'Analysis Keyword', 'Method', 'Analyst', 'Result', 'Unit' ]
for i in analyses:
    thisanalysis = {}
    thisanalysis[cols[0]] = api.get_parent(i).id
    thisanalysis[cols[1]] = i.title
    thisanalysis[cols[2]] = i.id
    thisanalysis[cols[3]] = i.getMethod()
    if thisanalysis[cols[3]]:
        thisanalysis[cols[3]] = thisanalysis[cols[3]].title
    thisanalysis[cols[4]] = i.getAnalyst()
    thisanalysis[cols[5]] = html.HTMLParser().unescape(i.getFormattedResult())
    thisanalysis[cols[6]] = i.Unit
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
