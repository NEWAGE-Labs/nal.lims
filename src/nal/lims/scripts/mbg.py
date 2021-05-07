#	MBG Extract Script
#	5/18/2020
#	Paul VanderWeele

from AccessControl import getSecurityManager
from AccessControl.User import UnrestrictedUser
from AccessControl.SecurityManagement import newSecurityManager
from bika.lims import api
from datetime import datetime

portal = api.get_portal()
me = UnrestrictedUser(getSecurityManager().getUser().getUserName(), '', ['LabManager'], '')
me = me.__of__(portal.acl_users)
newSecurityManager(None, me)

# #Print analyses per client for a given array of sample IDs
# for x in ARs:
# 	obj = api.get_object(x)
# 	id = api.get_object(x).getId()
# 	if id in mbg:
# 		print(id)
# 		client = obj.getClient().getName()
# 		analyses = obj.getAnalyses()
# 		for y in analyses:
# 			analysis = api.get_object(y)
# 			analysisId = analysis.getId()
# 			result = analysis.getResult()
# 			print("Client: {}\nSample: {}\nTest: {}\nResult: {}".format(client,id,analysisId,result))
#
#
# for x in ARs:
# 	obj = api.get_object(x)
# 	id = obj.getId()
# 	if id in mbg:
# 		print(id)
# 		client = obj.getClient().getName()
# 		analyses = obj.getAnalyses()
# 		for y in analyses:
# 			analysis = api.get_object(y)
# 			analysisId = analysis.getId()
# 			result = analysis.getResult()
# 			print("Client: {}\nSample: {}\nTest: {}\nResult: {}".format(client,id,analysisId,result))

#List of MBG sample IDs
mbg = [
'001567',
'001571',
'001572',
'001587',
'001588',
'001589',
'001590',
'001591',
'001592',
'001593',
'001578',
'001579',
'001580',
'001581',
'001582',
'001583',
'001584',
'001585',
'001576',
'001577'
]

#Open File
file = open("/home/naladmin/mbgtest.csv", "w", 1)
#Write headers
file.write("Sample Type;\
Supplier Type;\
Supplier ID;\
Sample Location Address;\
Sample Location;\
Sample Location State;\
Source Type;\
Source ID;\
Retest of Sample;\
Collection Date;\
Collection Time;\
Collected By;\
Lab Name;\
Received Date;\
Received Time;\
Sample ID;\
Test Date;\
Test Time;\
Coliforms;\
Ecoli;\
Salmonella;\
Listeria;\
Nitrate;\
Nitrite;\
Mold;\
Yeast;\
Enterobactereacea;\
Aerobic/Total Plate Count;\
Geomen;\
STV\n")

#Get all ARs (Sample)
ARs = api.search({'portal_type':'AnalysisRequest'})

#Get MBG ARs
mbgARs = {}
for i in ARs:
	AR = api.get_object(i)
	id = AR.getId()
	if id in mbg:
		mbgARs[i] = AR

##### Get Sample Data #####
for mbgAR_brain in mbgARs:
	#Get AR object, Sample ID, Client, and Batch
	mbgAR = api.get_object(mbgAR_brain)
	id = mbgAR.getId()
	client = mbgAR.getClient()
	client_name = client.getName()
	batch = mbgAR.getBatch()
	analyses = mbgAR.getAnalyses()
	#Grower #
	no_grower = 0
	grower = client.getTaxNumber()
	if grower == '':
		no_grower = 1
		print("The sample {} for client {} does not have a grower #\n".format(id, client_name))
	if no_grower == 1:
		print("Missing Grower Number. Exiting Export")
		break;
	#Street Address
	no_address = 0
	address = client.getPostalAddress().get("address")
	if address == '':
		no_address = 1
		print("The sample {} for client {} does not have an address\n".format(id, client_name))
	if no_address == 1:
		print("Missing address. Exiting Export")
		break;
	#City
	no_city = 0
	city = client.getPostalAddress().get("city")
	if city == '':
		no_city = 1
		print("The sample {} for client {} does not have a city in the address\n".format(id, client_name))
	if no_city == 1:
		print("Missing city. Exiting Export")
		break;
	#State Abbreviation
	no_state = 0
	full_state = client.getPostalAddress().get("state")
	state = full_state[0:2]
	if state == '':
		no_state = 1
		print("The sample {} for client {} does not have a state in the address\n".format(id, client_name))
	if no_state == 1:
		print("Missing state. Exiting Export")
		break;
	#Source Type
	#NEED SOURCE TYPE ADDED TO AR CREATION
	#Source ID (Client Sample ID)
	no_CSID = 0
	CSID = mbgAR.getClientSampleID()
	if CSID == '':
		no_CSID = 1
		print("The sample {} for client {} does not have a Client Sample ID\n".format(id, client_name))
	if no_CSID == 1:
		print("Missing Client Sample ID Number. Exiting Export")
		break;
	#Retest (Primary Sample)
	#NEED 'PRIMARY SAMPLE' ADDED TO AR CREATION AS RETEST FIELD
	#Collection Date (Date Sampled)
	no_datesampled = 0
	datesampled = mbgAR.getDateSampled().Date()
	if datesampled == '':
		no_datesampled = 1
		print("The sample {} for client {} does not have a Date Sampled\n".format(id, client_name))
	if no_datesampled == 1:
		print("Missing Sampling Date. Exiting Export")
		break;
	#Collection Time (Time Sampled)
	no_timesampled = 0
	timesampled = mbgAR.getDateSampled().Time()
	if timesampled == '':
		no_timesampled = 1
		print("The sample {} for client {} does not have a Time Sampled\n".format(id, client_name))
	if no_timesampled == 1:
		print("Missing Sampling Time. Exiting Export")
		break;
	#Collected By (Sampler)
	no_sampler = 0
	sampler = mbgAR.CollectedBy
	if sampler == '':
		no_sampler = 1
		print("The sample {} for client {} does not have a Sampler\n".format(id, client_name))
	if no_sampler == 1:
		print("Missing Sampler. Exiting Export")
		break;
	#Lab name
	lab = "NEW AGE LABORATORIES"
	#Received Date (BatchDate.Date)
	no_recvdate = 0
	recvdate = batch.getBatchDate().Date()
	if recvdate == '':
		no_recvdate = 1
		print("The sample {} for client {} does not have a Received Date\n".format(id, client_name))
	if no_recvdate == 1:
		print("Missing Received Date. Exiting Export")
		break;
	#Received Time (BatchDate.Time)
	no_recvtime = 0
	recvtime = batch.getBatchDate().Time()
	if recvtime == '':
		no_recvtime = 1
		print("The sample {} for client {} does not have a Received Time\n".format(id, client_name))
	if no_recvtime == 1:
		print("Missing Received Time. Exiting Export")
		break;
	#Id
	id = id
	#Test Date (DateTimeIn.Date)
	no_testdate = 0
	testdate = batch.DateTimeIn.Date()
	if testdate == '':
		no_testdate = 1
		print("The sample {} for client {} does not have a Test Date\n".format(id, client_name))
	if no_testdate == 1:
		print("Missing Test Date. Exiting Export")
		break;
	#Test Time (DateTimeIn.Time)
	no_testtime = 0
	testtime = batch.DateTimeIn.Time()
	if testtime == '':
		no_testtime = 1
		print("The sample {} for client {} does not have a Test Time\n".format(id, client_name))
	if no_testtime == 1:
		print("Missing Test Time. Exiting Export")
		break;
	##Analyses
	ecoli = ''
	coliform = ''
	salmonella = ''
	listeria = ''
	nitrate = ''
	nitrite = ''
	yeast = ''
	mold = ''
	eb = ''
	apc = ''
	geomen = ''
	stv = ''
	for analysis_brain in analyses:
		analysis = api.get_object(analysis_brain)
		result = analysis.getResult()
		#E.Coli PA
		if analysis.id == 'ecoli_pa':
			if result == '0':
				ecoli = 'ABSENT'
			if result == '1':
				ecoli = 'PRESENT'
		#Coliform PA
		if analysis.id == 'coliform_pa':
			if result == '0':
				coliform = 'ABSENT'
			if result == '1':
				coliform = 'PRESENT'
		#E.Coli MPN
		if analysis.id == 'ecoli_mpn':
			ecoli = result
			if float(result) > 2419.6:
				ecoli = '> 2419.6'
			if float(result) < 1.0:
				ecoli = '< 1.0'
		#Coliform MPN
		if analysis.id == 'coliform_mpn':
			coliform = result
			if float(result) > 2419.6:
				coliform = '> 2419.6'
			if float(result) < 1.0:
				coliform = '< 1.0'
		#Nitrate
		if analysis.id == 'nitrate':
			nitrate = result
		#Nitrite
		if analysis.id == 'nitrite':
			nitrite = result
	#Get Geometric Mean for this sample's source ID.
		#Search all ARs for this client where this.CSID = that.CSID
		#Of those ARs, keep the most recent 10 ecoli_mpn results
		#Apply Geomean() to those results.
	file.write("{};{};{};{};{};{};{};{};{};{};{};{};{};{};{};{};{};{};{};{};{};\
	{};{};{};{};{};{};{};{};{};\n".format(
	'W',
	'G',
	grower,
	address,
	city,
	state,
	'',
	CSID,
	'',
	datesampled,
	timesampled,
	sampler,
	'NEW AGE LABORATORIES',
	recvdate,
	recvtime,
	id,
	testdate,
	testtime,
	coliform,
	ecoli,
	salmonella,
	listeria,
	nitrate,
	nitrite,
	mold,
	yeast,
	eb,
	apc,
	geomen,
	stv
	))
##### End Get Sample Data #####
