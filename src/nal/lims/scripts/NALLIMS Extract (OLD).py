#	NALLIMS Extract Script
#	07/13/2020
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
#Open File
file = open("/home/naladmin/NALLIMS_EXPORT.csv", "w", 1)
#Write headers
file.write("Status;\
Batch;\
Received Date;\
Received Time;\
Client ID;\
Client Name;\
Sample ID;\
Sample Name;\
Sample Type;\
Sample Location;\
Sampler;\
Sampling Date;\
Sampling Time;\
Test Date;\
Test Time;\
Analyte;\
Result\n")
#Get all ARs (Sample)
ARs = api.search({'portal_type':'AnalysisRequest'})
##### Get Sample Data #####
for AR_brain in ARs:
#AR Object
	AR = api.get_object(AR_brain)
#Status
	status = api.get_review_status(AR)
#Batch
## Title
## Received Date
## Test Date
	batch = AR.getBatch()
	if batch is not None and batch != '':
		batch_title = api.get_title(batch)
		recv_datetime = batch.getBatchDate()
		if recv_datetime is not None and recv_datetime != '':
			received_date = recv_datetime.Date()
			received_time = recv_datetime.Time()
		test_datetime = batch.DateTimeIn
		if test_datetime is not None and test_datetime != '':
			test_date = test_datetime.Date()
			test_time = test_datetime.Time()
#Client
## ID
## Name
	client = AR.getClient()
	client_ID = client.getClientID()
	client_name = client.getName()
#Sample 
## ID
## Name
	sample_ID = AR.getId()
	sample_name = AR.getClientSampleID()
#Sample Type
	sampletype = AR.getSampleType()
	if sampletype is not None:
		sample_type = api.get_title(sampletype)
#Sample Location
	sample_point = AR.getSamplePoint()
	if sample_point is not None:
		sample_location = api.get_title(sample_point)
#Sampler
	sampler = AR.CollectedBy
#Sampling Datetime
	sampling_datetime = AR.getDateSampled()
	if sampling_datetime is not None and sampling_datetime != '':
		sampling_date = sampling_datetime.Date()
		sampling_time = sampling_datetime.Time()
#Analyses array
	analyses = AR.getAnalyses()
	for analysis_brain in analyses:
		#Analysis object
		analysis = api.get_object(analysis_brain)		
		#Analyte
		if analysis is not None:
			analyte = api.get_title(analysis)
		#Result
		result = analysis.getResult()
		file.write("{};{};{};{};{};{};{};{};{};{};{};{};{};{};{};{};{};\n".format(
		status,
		batch_title,
		received_date,
		received_time,
		client_ID,
		client_name,
		sample_ID,
		sample_name,
		sample_type,
		sample_location,
		sampler,
		sampling_date,
		sampling_time,
		test_date,
		test_time,
		analyte,
		result))
