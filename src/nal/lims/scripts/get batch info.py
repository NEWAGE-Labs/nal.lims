#Purpose: Get all Batches from debug mode in Senaite
#Author: Paul VanderWeele
#Date: 19 May 2020
################################################################################

from AccessControl import getSecurityManager
from AccessControl.User import UnrestrictedUser
from AccessControl.SecurityManagement import newSecurityManager
from bika.lims import api
from datetime import datetime

portal = api.get_portal()
me = UnrestrictedUser(getSecurityManager().getUser().getUserName(), '', ['LabManager'], '')
me = me.__of__(portal.acl_users)
newSecurityManager(None, me)

batches = api.searhc({'portal_type':'Batch'})

#Print all Batch info
for batch in batches:
    x = api.get_object(batch)
    id = x.getId()
    title = x.getClientBatchID()
    client = x.getClient().getName()
    recvX = x.BatchDate
    if recvX is not None:
        recv = "" + recvX.Date() + " " + recvX.Time()
    else:
        recv = ""
    testX = x.DateTimeIn
    if testX is not None:
        test = "" + testX.Date() + " " + testX.Time()
    else:
        test = ""
    print("ID: {}\nTitle: {}\nClient: {}\nReceived Date/Time: {}\nTest Date/Time: {}\n".format(id,title,client,recv,test))

#Save all batch info
file = open("/home/naladmin/batches.csv", "w", 1) #Change File name here
file.write("ID;Title;Client;Received Date/Time;Test Date/Time\n")
for batch in batches:
    x = api.get_object(batch)
    id = x.getId()
    title = x.getClientBatchID()
    client = x.getClient().getName()
    recvX = x.BatchDate
    if recvX is not None:
        recv = "" + recvX.Date() + " " + recvX.Time()
    else:
        recv = ""
    testX = x.DateTimeIn
    if testX is not None:
        test = "" + testX.Date() + " " + testX.Time()
    else:
        test = ""
    file.write("{};{};{};{};{}\n".format(id,title,client,recv,test))


file.close()
