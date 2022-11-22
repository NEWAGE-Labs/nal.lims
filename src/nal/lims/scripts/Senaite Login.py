from AccessControl import getSecurityManager
from AccessControl.User import UnrestrictedUser
from AccessControl.SecurityManagement import newSecurityManager
from bika.lims import api
portal = api.get_portal()
me = UnrestrictedUser(getSecurityManager().getUser().getUserName(), '', ['LabManager'], '')
me = me.__of__(portal.acl_users)
newSecurityManager(None, me)

#Useful imports
import transaction as t
import nal.lims.datamigration as dm
import pandas as pd
from datetime import datetime
import os

#Example
sample = map(api.get_object,api.search({'portal_type':'SamplePoint'}))
location = map(api.get_object,api.search({'portal_type':'SamplePoint','id':'samplepoint-483'}))[0]
