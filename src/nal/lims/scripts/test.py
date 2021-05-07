from zope.component.hooks import setSite
from AccessControl import getSecurityManager
from AccessControl.User import UnrestrictedUser
from AccessControl.SecurityManagement import newSecurityManager
from Testing.makerequest import makerequest
from bika.lims import api
from plone import api as plone_api

#Setup site and portal
app = makerequest(app)
app._p_jar.sync()
setSite(app['nallims'])
portal = api.get_portal()

#Log in as a Labmanager
me = UnrestrictedUser(getSecurityManager().getUser().getUserName(), '', ['Labmanager'], '')
me = me.__of__(portal.acl_users)
newSecurityManager(None, me)

with plone_api.env.adopt_user(username="naladmin"):

	#Get All clients
	clients = api.search({'portal_type': 'Client'})

	#Write client list to a file.
	file = open("/home/naladmin/test.txt", 'w', 1)
	for client in clients:
		print("{}\n".format(api.get_object(client).getName()))
		file.write("{}\n".format(api.get_object(client).getName()))
	file.close()
