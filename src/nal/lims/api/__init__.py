from bika.lims import api
from plone import api as papi
from math import floor
from math import log10
import pandas as pd
from management import get_samples_by_week
from retract import retract_batches_by_keyword

BAD = ['invalid','cancelled','rejected','retracted']
CLIENT_COLS = [
	'nal_number',
	'client_name',
	'client_address',
	'sample_delivery_group',
	'internal_lab_id',
	'date_received',
	'time_received',
	'project_contact',
	'sampler_contact',
	'grower_contact',
	'client_sample_id',
	'nal_sample_id',
	'date_sampled',
	'time_sampled',
	'sample_type',
	'sample_location'
]

SAP_COLS = [
	'pair',
	'plant_type',
	'variety',
	'growth_stage',
	'vigor',
	'new_old',
	'nitrogen_conversion_efficiency'
]

def ok(xobj):
	try:
		obj = api.get_object(xobj)
	except Exception as e:
		raise(e)

	if api.get_workflow_status_of(obj) not in BAD:
		return True
	else:
		return False

def moveSDG(sdg_title,target_client_id):
	sdg_brain = api.search({'portal_type':'Batch','title':sdg_title})
	sdg_count = len(sdg_brain)
	if sdg_count == 1:
		sdg = api.get_object(sdg_brain[0])
	elif sdg_count > 1:
		sdgs = map(api.get_object,sdg_brain)
		open = 0
		for i in sdgs:
			if api.get_workflow_status_of(i) == 'open':
				sdg = i
				open += 1
		if open > 1:
			raise Exception("Ambiguous SDG title. Please Close/Cancel duplicate SDGs.")
	else:
		raise Exception("No SDG found with that title. Please confirm SDG exists.")

	clients = api.search({'portal_type':'Client'})
	for i in clients:
		if i.getClientID == target_client_id:
			client = api.get_object(i)
	if client is None:
		raise Exception("Client ID does not exist.")

	if sdg is not None and client is not None:
		papi.content.move(sdg,client)
		returnstr = "The following items were moved to {}:\n{}".format(client.ClientID + " - " + client.Name,sdg.title)
		ars = sdg.getAnalysisRequests()
		for i in ars:
			papi.content.move(source=i,target=client)
			returnstr = returnstr + "\n{}".format(i.id)
	return returnstr

def login():
    from AccessControl import getSecurityManager
    from AccessControl.User import UnrestrictedUser
    from AccessControl.SecurityManagement import newSecurityManager
    portal = api.get_portal()
    me = UnrestrictedUser(getSecurityManager().getUser().getUserName(), '', ['LabManager'], '')
    me = me.__of__(portal.acl_users)
    return newSecurityManager(None, me)

def get_clean_ARs(ARList):
	ARs = map(api.get_object,ARList)
	bad_ars = []
	#Remove invalid samples
	for ar in ARs:
		if api.get_workflow_status_of(ar) in BAD:
			bad_ars.append(ar)
	for ar in bad_ars:
		ARs.remove(ar)

	return ARs

def get_other_cols(ARs,xcols):
	cols = list(xcols)
	if ARs is None or len(ARs) == 0:
		return cols
	ar_cols = []
	for ar in ARs:
		if ar.getSampleType().title in ['Sap','Root','Fruit','Soil'] and 'plant_type' not in cols and ok(ar):
			cols = cols + SAP_COLS

		for an in map(api.get_object,ar.getAnalyses()):
			if ok(an) and an.Keyword not in cols and an.Keyword not in ar_cols:
				ar_cols.append(str(an.Keyword))
			ar_cols.sort()
	cols = cols + ar_cols
	return cols

def get_address(addressdict):
	exportaddress = ''
	if addressdict['address'] != '':
		exportaddress = exportaddress + addressdict['address']
	if addressdict['city'] != '':
		exportaddress = exportaddress + ', ' + addressdict['city']
	if addressdict['state'] != '':
		exportaddress = exportaddress + ', ' + addressdict['state']
	if addressdict['zip'] != '':
		exportaddress = exportaddress + ' ' + addressdict['zip']
	return exportaddress

def get_sample_basic_info(xexport_dict,sample,sdg,client):
	export_dict = dict(xexport_dict)
	#NAL Number
	export_dict['nal_number'].append(client.getClientID())

	#Client Name
	export_dict['client_name'].append(client.getName())

	#Client Address
	export_dict['client_address'].append(get_address(client.getPhysicalAddress()))

	#SDG
	export_dict['sample_delivery_group'].append(sdg.title)

	#ILI
	export_dict['internal_lab_id'].append(sample.InternalLabID)

	#Date Received
	dreceived = sdg.SDGDate.strftime('%m-%d-%Y')
	export_dict['date_received'].append(dreceived)

	#Time Received
	export_dict['time_received'].append(sdg.SDGTime)

	#Project Contact
	project_brain = sdg.getReferences(relationship="SDGProjectContact")
	if len(project_brain) > 0:
		project_contact = project_brain[0]
		project_contact_name = project_contact.Firstname + " " + project_contact.Surname
	elif hasattr(sdg,'ProjectContact'):
		project_contact = api.get_object_by_uid(sdg.ProjectContact)
		project_contact_name = project_contact.Firstname + " " + project_contact.Surname
	else:
		project_contact_name = ''
	export_dict['project_contact'].append(project_contact_name)

	#Sampler Contact
	sampler_brain = sdg.getReferences(relationship="SDGSamplerContact")
	if len(sampler_brain) > 0:
		sampler_contact = sampler_brain[0]
		sampler_contact_name = sampler_contact.Firstname + " " + sampler_contact.Surname
	elif hasattr(sdg,'SamplerContact') and sdg.SamplerContact is not None:
		sampler_contact = api.get_object_by_uid(sdg.SamplerContact)
		sampler_contact_name = sampler_contact.Firstname + " " + sampler_contact.Surname
	else:
		sampler_contact_name = ''
	export_dict['sampler_contact'].append(sampler_contact_name)

	#Grower Contact
	grower_brain = sdg.getReferences(relationship="SDGGrowerContact")
	if len(grower_brain) > 0:
		grower_contact = grower_brain[0]
		grower_contact_name = grower_contact.Firstname + " " + grower_contact.Surname
	elif hasattr(sdg,'GrowerContact') and sdg.GrowerContact != '':
		grower_contact = api.get_object_by_uid(sdg.GrowerContact)
		grower_contact_name = grower_contact.Firstname + " " + grower_contact.Surname
	else:
		grower_contact_name = ''
	export_dict['grower_contact'].append(grower_contact_name)

	#Client Sample ID
	export_dict['client_sample_id'].append(sample.getClientSampleID())

	#NAL Sample ID
	export_dict['nal_sample_id'].append(sample.id)

	#Date Sampled
	export_dict['date_sampled'].append(sample.DateOfSampling.strftime('%m-%d-%Y'))

	#Time Sampled
	export_dict['time_sampled'].append(sample.TimeOfSampling)

	#Sample Type
	export_dict['sample_type'].append(sample.getSampleType().title)

	#Sample Location
	if sample.getSamplePoint() is not None:
		export_dict['sample_location'].append(sample.getSamplePoint().title)
	else:
		export_dict['sample_location'].append('')
	return export_dict

def get_sample_sap_info(xexport_dict, sample, cols):
	export_dict = dict(xexport_dict)
	if 'plant_type' in cols:
		#Pair
		if hasattr(sample,'SubGroup') and sample.getSubGroup() is not None:
			export_dict['pair'].append(sample.getSubGroup().title)
		else:
			export_dict['pair'].append('')
		#Plant Type
		export_dict['plant_type'].append(sample.PlantType)
		#Variety
		export_dict['variety'].append(sample.Variety)
		#Growth Stage
		export_dict['growth_stage'].append(sample.GrowthStage)
		#Vigor
		if hasattr(sample,'Vigor'):
			export_dict['vigor'].append(sample.Vigor)
		#New/Old
		new_old = ''
		## If Sample has a Pair, Then assign a 'New' or 'Old'
		if sample.getSampleType().title == 'Sap' and sample.getSubGroup() is not None:
			if sample.NewLeaf is True:
				new_old = 'New'
			elif sample.NewLeaf is False:
				new_old = 'Old'
		export_dict['new_old'].append(new_old)

	return export_dict

def get_sample_analysis_info(xexport_dict, sample):
	export_dict = dict(xexport_dict)
	sigfigs = 3 
	updated = []
	for analysis in [an for an in map(api.get_object,sample.getAnalyses()) if ok(an)]:
		if 'nitrogen_conversion_efficiency' not in analysis.Keyword:
			updated.append(analysis.Keyword)
			result = analysis.getResult()
			dil = (1 if (analysis.Dilution is None or analysis.Dilution == '') else analysis.Dilution)

			if result.replace('.','',1).replace('-','',1).isdigit() is False:
				export_dict[analysis.Keyword].append(result)
			else:
				result = float(result)

				loq = 0.01
				for method in analysis.getAnalysisService().MethodRecords:
					if hasattr(analysis,'CustomMethod') and method['methodid'] == analysis.CustomMethod:
						loq = method['loq']
				choices = None
				if loq == 'P|A':
					choices = analysis.getResultOptions()
				if choices:
					# Create a dict for easy mapping of result options
					values_texts = dict(map(lambda c: (str(c["ResultValue"]), c["ResultText"]), choices))
					# Result might contain a single result option
					match = values_texts.get(str(int(result)))
					if match:
						result = match
					else:
						result = '-'

				elif result < float(loq):
                                	result = '< {}'.format(float(loq) * float(dil))
				else:
					result = round((result*float(dil)), sigfigs-int(floor(log10(abs(result*float(dil)))))-1)
				export_dict[analysis.Keyword].append(result)

	for key in export_dict.keys():
		if key not in CLIENT_COLS and key not in SAP_COLS and key not in updated:
			export_dict[key].append('')
	return export_dict

def get_nce(xexport_dict, sample):
	export_dict = dict(xexport_dict)
	sigfigs = 3
	if sample.getSampleType().title == 'Sap' and hasattr(sample,'nitrogen_nitrate') and hasattr(sample,'nitrogen_ammonium') and hasattr(sample,'nitrogen'):
		nh4 = export_dict['nitrogen_ammonium'][-1]
		no3 = export_dict['nitrogen_nitrate'][-1]
		tn = export_dict['nitrogen'][-1]
		nce = 0

		if nh4 is None or nh4 == '< 0.01' or nh4 == '':
			nh4 = 0
		else:
			nh4 = float(nh4)
		if no3 is None or no3 == '< 0.01' or no3 == '':
			no3 = 0
		else:
			no3 = float(no3)
		if tn is None or tn == '< 0.01' or tn == '':
			tn = 0
		else:
			tn = float(tn)

		if tn > 0:
			nce = (1 - ((float(nh4) + float(no3)) / float(tn)))*100
			nce = round(nce, sigfigs-int(floor(log10(abs(nce))))-1)
			export_dict['nitrogen_conversion_efficiency'].append(nce)
		else:
			export_dict['nitrogen_conversion_efficiency'].append('')

	elif 'nitrogen_conversion_efficiency' in export_dict.keys():
		export_dict['nitrogen_conversion_efficiency'].append('')

	return export_dict

def getCSVDFbyAR(ARList, excl_client=False):
	ARs = get_clean_ARs(ARList)
	if len(ARs) == 0:
		return None
	export_dict = {}

	#Get Client Columns
	base_cols = [col for col in CLIENT_COLS]

	#Get Sap and AR Columns
	cols = get_other_cols(ARs,base_cols)

        #initialize dictionary of lists, one for each column
	for i in range(len(cols)):
		export_dict[cols[i]] = []

	for sample in ARs:
		#Skip invalid samples
		if not ok(sample):
			pass

		#Get SDG for this sample and skip if it is invalid
	    	sdg = sample.getBatch()
		if sdg is None or not ok(sdg):
			pass

		#Get Client for this SDG and skip if it is invalid
		client = sdg.getClient()
		if client is None or not ok(client):
			pass

		#Get Basic Sample information
		export_dict = get_sample_basic_info(export_dict,sample,sdg,client)
		#Get Sap Sample information
		export_dict = get_sample_sap_info(export_dict,sample,cols)
		#Get Sample Analysis information
		export_dict = get_sample_analysis_info(export_dict,sample)
		#Get Nitrogen Conversion Efficiency for Sap samples
		export_dict = get_nce(export_dict,sample)

	#Exclude Client Cols
	if excl_client==True:
	    for col in [ccol for ccol in CLIENT_COLS if ccol != 'nal_sample_id']:
		del export_dict[col]
		cols.remove(col)

	#Convert to DataFrame
	df = pd.DataFrame()
	for key in export_dict.keys():
		print('Creating Column for: {}'.format(key))
		df[key] = export_dict[key]

	#Return DataFrame
	return df[cols]

def getSDGCSV(batch, excl_client=False):
	sdg = api.get_object(batch)
	export_dict = {}
        #Get a Column list based on:
        # 1) Client Fields
        # 2) SDG Fields
        # 3) Relevant Sample fields (Crop details)
        # 4) The unique list of analyses on all samples of the SDG
        client_cols = [
            'nal_number',
            'client_name',
            'client_address',
            'sample_delivery_group',
	    'internal_lab_id',
            'date_received',
            'time_received',
            'project_contact',
            'sampler_contact',
            'grower_contact',
            'client_sample_id',
            'nal_sample_id',
            'date_sampled',
            'time_sampled',
            'sample_type',
            'sample_location'
        ]
	cols = [col for col in client_cols]
        ARs = sdg.getAnalysisRequests()
        for i in ARs:
            if i.getSampleType().title in ['Sap','Root','Fruit','Soil'] and 'plant_type' not in cols and api.get_workflow_status_of(i) not in BAD:
                sap_cols = [
                    'plant_type',
                    'variety',
                    'growth_stage',
                    'vigor',
                    'new_old',
                    'nitrogen_conversion_efficiency'
                ]
                cols = cols + sap_cols

	    ar_cols = []
            for j in map(api.get_object,i.getAnalyses()):
                if api.get_workflow_status_of(j) not in BAD and j.Keyword not in cols and j.Keyword not in ar_cols:
                    ar_cols.append(str(j.Keyword))
	    ar_cols.sort()

	    cols = cols + ar_cols
        #initialize dictionary of lists
        for i in range(len(cols)):
            export_dict[cols[i]] = []

        sample_count = 0
        for i in ARs:
            if api.get_workflow_status_of(i) not in BAD:

                sample_count = sample_count+1

                client = sdg.getClient()

                #NAL Number
                export_dict['nal_number'].append(client.getClientID())

                #Client Name
                export_dict['client_name'].append(client.getName())

                #Client Address
                addressdict = client.getPhysicalAddress()
                exportaddress = ''
                if addressdict['address'] != '':
                    exportaddress = exportaddress + addressdict['address']
                if addressdict['city'] != '':
                    exportaddress = exportaddress + ', ' + addressdict['city']
                if addressdict['state'] != '':
                    exportaddress = exportaddress + ', ' + addressdict['state']
                if addressdict['zip'] != '':
                    exportaddress = exportaddress + ' ' + addressdict['zip']
                export_dict['client_address'].append(exportaddress)

                #SDG
                export_dict['sample_delivery_group'].append(sdg.title)
                #SDG
                export_dict['internal_lab_id'].append(i.InternalLabID)

                #Date Received
                dreceived = sdg.SDGDate.strftime('%m-%d-%Y')
                export_dict['date_received'].append(dreceived)

                #Time Received
                export_dict['time_received'].append(sdg.SDGTime)

		#Project Contact
                project_brain = sdg.getReferences(relationship="SDGProjectContact")
                if len(project_brain) > 0:
                    project_contact = project_brain[0]
                else:
                    project_contact = api.get_object_by_uid(sdg.ProjectContact)
                project_contact_name = project_contact.Firstname + " " + project_contact.Surname
                export_dict['project_contact'].append(project_contact_name)

                #Sampler Contact
                sampler_brain = sdg.getReferences(relationship="SDGSamplerContact")
                if len(sampler_brain) > 0:
                    sampler_contact = sampler_brain[0]
                else:
                    sampler_contact = api.get_object_by_uid(sdg.SamplerContact)
                sampler_contact_name = sampler_contact.Firstname + " " + sampler_contact.Surname
                export_dict['sampler_contact'].append(sampler_contact_name)

                #Grower Contact
		grower_brain = sdg.getReferences(relationship="SDGGrowerContact")
                if len(grower_brain) > 0:
                    grower_contact = grower_brain[0]
                    grower_contact_name = grower_contact.Firstname + " " + grower_contact.Surname
                elif hasattr(sdg,'GrowerContact') and sdg.GrowerContact != '':
                    grower_contact = api.get_object_by_uid(sdg.GrowerContact)
                    grower_contact_name = grower_contact.Firstname + " " + grower_contact.Surname
                else:
                    grower_contact_name = ''
                export_dict['grower_contact'].append(grower_contact_name)

                #Client Sample ID
                export_dict['client_sample_id'].append(i.getClientSampleID())

                #NAL Sample ID
                export_dict['nal_sample_id'].append(i.id)

                #Date Sampled
                export_dict['date_sampled'].append(i.DateOfSampling.strftime('%m-%d-%Y'))

                #Time Sampled
                export_dict['time_sampled'].append(i.TimeOfSampling)

                #Sample Type
                export_dict['sample_type'].append(i.getSampleType().title)

                #Sample Location
                if i.getSamplePoint() is not None:
                    export_dict['sample_location'].append(i.getSamplePoint().title)
                else:
                    export_dict['sample_location'].append('')

                if 'plant_type' in cols:
                    #Plant Type
                    export_dict['plant_type'].append(i.PlantType)

                    #Variety
                    export_dict['variety'].append(i.Variety)

                    #Growth Stage
                    export_dict['growth_stage'].append(i.GrowthStage)

                    #Vigor
                    if hasattr(i,'Vigor'):
                        export_dict['vigor'].append(i.Vigor)

                    #New/Old
                    new_old = ''
                    ## If Sample has a Pair, Then assign a 'New' or 'Old'
                    if i.getSampleType().title == 'Sap' and i.getSubGroup() is not None:
                        if i.NewLeaf is True:
                            new_old = 'New'
                        elif i.NewLeaf is False:
                            new_old = 'Old'
                    export_dict['new_old'].append(new_old)

                for j in map(api.get_object,i.getAnalyses()):
                    if api.get_workflow_status_of(j) not in BAD and 'nitrogen_conversion_efficiency' not in j.Keyword:
                        sigfigs = 3
                        result = j.getResult()
			dil = (1 if (j.Dilution is None or j.Dilution == '') else j.Dilution)
                        if result.replace('.','',1).replace('-','',1).isdigit() is False:
                            export_dict[j.Keyword].append(result)
                        else:
                            result = float(result)
			    loq = 0.01
			    for k in j.getAnalysisService().MethodRecords:
				if k['methodid'] == j.CustomMethod:
				    loq = k['loq']
			    if loq == 'P|A':
				choices = j.getResultOptions()
				print("Choices are {}".format(choices))
				if choices:
            				# Create a dict for easy mapping of result options
            				values_texts = dict(map(lambda c: (str(c["ResultValue"]), c["ResultText"]), choices))
            				# Result might contain a single result option
            				match = values_texts.get(str(int(result)))
            				if match:
                				result = match
					else:
						result = '-'
				else:
					result = '-'
                            elif result < float(loq):
                                result = '< {}'.format(float(loq) * float(dil))
                            else:
                                result = round((result*float(dil)), sigfigs-int(floor(log10(abs(result*float(dil)))))-1)

                            export_dict[j.Keyword].append(result)

                if i.getSampleType().title == 'Sap':
                    nh4 = export_dict['nitrogen_ammonium'][-1]
                    no3 = export_dict['nitrogen_nitrate'][-1]
                    tn = export_dict['nitrogen'][-1]
                    nce = 0

                    if nh4 is None or nh4 == '< 0.01' or nh4 == '':
                        nh4 = 0
                    if no3 is None or no3 == '< 0.01' or no3 == '':
                        no3 = 0
                    if tn is None or tn == '< 0.01' or tn == '':
                        tn = 0
                    else:
                        tn = float(tn)

                    if tn > 0:
                        nce = (1 - ((float(nh4) + float(no3)) / float(tn)))*100
                        nce = round(nce, sigfigs-int(floor(log10(abs(nce))))-1)
                        export_dict['nitrogen_conversion_efficiency'].append(nce)
                    else:
                        export_dict['nitrogen_conversion_efficiency'].append('')

                for j in cols:
                    if len(export_dict[j]) < sample_count:
                        export_dict[j].append('')

	#Exclude Client Cols
	if excl_client==True:
	    for col in [ccol for ccol in client_cols if ccol != 'nal_sample_id']:
		del export_dict[col]
		cols.remove(col)

	#Convert to DataFrame
        df = pd.DataFrame()

        for i in export_dict.keys():
            df[i] = export_dict[i]
	#Return DataFrame
	return df[cols]

def get_sap_by_samples(samples):
	cols = [
		'id',
		'Client',
		'Crop',
		'Growth Stage',
		'Variety',
		'Vigor',
		'Sugars',
		'Brix',
		'pH',
		'EC',
		'Chloride',
		'Phosphorus',
		'Sulfur',
		'Calcium',
		'Potassium',
		'K/Ca Ratio',
		'Magnesium',
		'Sodium',
		'Aluminum',
		'Boron',
		'Cobalt',
		'Copper',
		'Iron',
		'Manganese',
		'Molybdenum',
		'Nickel',
		'Selenium',
		'Silica',
		'Zinc',
		'Ammonium-Nitrogen',
		'Nitrate-Nitrogen',
		'Nitrogen',
		'Nitrogen Conversion Efficiency'
	]
	dict = {}
	for i in cols:
		dict[i] = []

	for sample in samples:
		dict['id'].append(sample.id)
		dict['Client'].append(sample.aq_parent.Name)
		dict['Crop'].append(('' if not hasattr(sample,'PlantType') else sample.PlantType))
		dict['Growth Stage'].append(('' if not hasattr(sample,'GrowthStage') else sample.GrowthStage))
		dict['Variety'].append(('' if not hasattr(sample,'Variety') else sample.Variety))
		dict['Vigor'].append(('' if not hasattr(sample,'Vigor') else sample.Vigor))
		sugars = None
		brix = None
		ph = None
		ec = None
		chloride = None
		phosphorus = None
		sulfur = None
		calcium = None
		potassium = None
		magnesium = None
		sodium = None
		aluminum = None
		boron = None
		cobalt = None
		copper = None
		iron = None
		manganese = None
		molybdenum = None
		nickel = None
		selenium = None
		silica = None
		zinc = None
		ammonium = None
		nitrate = None
		nitrogen = None
		nce = None

		for analysis in map(api.get_object,sample.getAnalyses()):
			if api.get_workflow_status_of(analysis) not in ['retracted','rejected','invalid','cancelled']:
				keyword = analysis.Keyword
				try:
					result = float(analysis.Result)
					if result < 0:
						result = 0
				except ValueError as ve:
					result = ''
					print("Saving {} for {} - {}".format(result,analysis,keyword))
				if 'sugar' in keyword:
					sugars = result
				elif 'brix' in keyword:
					brix = result
				elif 'ph' in keyword and 'phos' not in keyword:
					ph = result
				elif 'ec' in keyword:
					ec = result
				elif 'chloride' in keyword:
					chloride = result
				elif 'phosph' in keyword:
					phosphorus = result
				elif 'sulfur' in keyword:
					sulfur = result
				elif 'calcium' in keyword:
					calcium = result
				elif 'potassium' in keyword:
					potassium = result
				elif 'magnesium' in keyword:
					magnesium = result
				elif 'sodium' in keyword:
					sodium = result
				elif 'aluminum' in keyword:
					aluminum = result
				elif 'boron' in keyword:
					boron = result
				elif 'cobalt' in keyword:
					cobalt = result
				elif 'copper' in keyword:
					copper = result
				elif 'iron' in keyword:
					iron = result
				elif 'manganese' in keyword:
					manganese = result
				elif 'molybdenum' in keyword:
					molybdenum = result
				elif 'nickel' in keyword:
					nickel = result
				elif 'selenium' in keyword:
					selenium = result
				elif 'silica' in keyword:
					silica = result
				elif 'zinc' in keyword:
					zinc = result
				elif 'nitrate' in keyword:
					nitrate = result
				elif 'ammoni' in keyword:
					ammonium = result
				elif 'nitrogen' == keyword:
					nitrogen = result

		dict['Sugars'].append(sugars)
		dict['Brix'].append(brix)
		dict['pH'].append(ph)
		dict['EC'].append(ec)
		dict['Chloride'].append(chloride)
		dict['Phosphorus'].append(phosphorus)
		dict['Sulfur'].append(sulfur)
		dict['Calcium'].append(calcium)
		dict['Potassium'].append(potassium)
		if potassium is None or calcium is None or potassium == '' or calcium == '':
			dict['K/Ca Ratio'].append('')
		else:
			dict['K/Ca Ratio'].append(potassium/calcium)
		dict['Magnesium'].append(magnesium)
		dict['Sodium'].append(sodium)
		dict['Aluminum'].append(aluminum)
		dict['Boron'].append(boron)
		dict['Cobalt'].append(cobalt)
		dict['Copper'].append(copper)
		dict['Iron'].append(iron)
		dict['Manganese'].append(manganese)
		dict['Molybdenum'].append(molybdenum)
		dict['Nickel'].append(nickel)
		dict['Selenium'].append(selenium)
		dict['Silica'].append(silica)
		dict['Zinc'].append(zinc)
		dict['Ammonium-Nitrogen'].append(ammonium)
		dict['Nitrate-Nitrogen'].append(nitrate)
		dict['Nitrogen'].append(nitrogen)
		if ammonium < 0.01:
			ammonium = 0
		elif ammonium is None:
			ammonium = ''
		if nitrate < 0.01:
			nitrate = 0
		elif nitrate is None:
			nitrate = ''
		if nitrogen is None or nitrogen < 0.01:
			nitrogen = 0
		if nitrogen > 0 and nitrate != '' and ammonium != '':
			from math import log10
			from math import floor
			nce_raw = (1 - (ammonium + nitrate) / (nitrogen))*100
			nce = round(nce_raw,3-int(floor(log10(abs(nce_raw))))-1)
		dict['Nitrogen Conversion Efficiency'].append(nce)

	return pd.DataFrame(dict)

def get_emails(sampletype=[]):
	emails = {}
	emails['email'] = []
	emails['name'] = []
	if len(sampletype) == 0:
		clients = map(api.get_object,api.search({'portal_type':'Client'}))
	else:
		samples = map(api.get_object,api.search({'portal_type':'AnalysisRequest'}))
		clients = []
		for i in samples:
			client = i.getClient()
			if client is not None and i.getSampleType().title in sampletype and i not in typelist and client not in clients:
				clients.append(i.getClient())

	for client in clients:
		if client.EmailAddress != "" and client.EmailAddress not in emails['email']:
			emails['email'].append(client.EmailAddress)
			emails['name'].append(client.Name)
		for contact in client.getContacts():
			if contact.EmailAddress != "" and contact.EmailAddress not in emails['email']:
				emails['email'].append(contact.EmailAddress)
				emails['name'].append(contact.Firstname + ' ' + contact.Surname)

	return pd.DataFrame(emails)
