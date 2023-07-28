from bika.lims import api
from plone import api as papi
from math import floor
from math import log10
import pandas as pd

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

def getSDGCSV(batch):
	sdg = api.get_object(batch)
	export_dict = {}
        #Get a Column list based on:
        # 1) Client Fields
        # 2) SDG Fields
        # 3) Relevant Sample fields (Crop details)
        # 4) The unique list of analyses on all samples of the SDG
        cols = [
            'nal_number',
            'client_name',
            'client_address',
            'sample_delivery_group',
	    'internal_lab_id',
            'date_received',
            'time_received',
            'project_contact',
            'sampler_contact'
            ]
        if hasattr(sdg,'GrowerContact'):
            cols.append('grower_contact')

        xtra_cols = [
            'client_sample_id',
            'nal_sample_id',
            'date_sampled',
            'time_sampled',
            'sample_type',
            'sample_location'
        ]
        cols = cols + xtra_cols
        ARs = sdg.getAnalysisRequests()
        for i in ARs:
            if i.getSampleType().title == 'Sap' and 'plant_type' not in cols and api.get_workflow_status_of(i) not in ['cancelled','invalid']:
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
                if j.Keyword not in cols and j.Keyword not in ar_cols:
                    ar_cols.append(str(j.Keyword))
	    ar_cols.sort()

	    cols = cols + ar_cols
        #initialize dictionary of lists
        for i in range(len(cols)):
            export_dict[cols[i]] = []

        sample_count = 0
        for i in ARs:
            if api.get_workflow_status_of(i) not in ['cancelled','invalid']:

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
                project_contact = sdg.getReferences(relationship="SDGProjectContact")[0]
                project_contact_name = project_contact.Firstname + " " + project_contact.Surname
                export_dict['project_contact'].append(project_contact_name)

                #Sampler Contact
                sampler_contact = sdg.getReferences(relationship="SDGSamplerContact")[0]
                sampler_contact_name = sampler_contact.Firstname + " " + sampler_contact.Surname
                export_dict['sampler_contact'].append(sampler_contact_name)

                #Grower Contact
                grower_contact = sdg.getReferences(relationship="SDGGrowerContact")
                if len(grower_contact) > 0 and 'grower_contact' in cols:
                    grower_contact_name = grower_contact.Firstname + " " + grower_contact.Surname
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
                    if api.get_workflow_status_of(j) not in ['cancelled','invalid','retracted','rejected'] and 'nitrogen_conversion_efficiency' not in j.Keyword:
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

	#Convert to DataFrame
        df = pd.DataFrame()

        for i in cols:
            df[i] = export_dict[i]
	#Return DataFrame
	return df

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

def get_sap_emails():
	samples = map(api.get_object,api.search({'portal_type':'AnalysisRequest'}))
	sap = []
	for i in samples:
		if i.getSampleType().title == 'Sap' and i not in sap:
			sap.append(i)
	emails = {}
	emails['email'] = []
	emails['name'] = []
	clients = []
	for i in sap:
		client = i.getClient()
		if client and client not in clients:
			clients.append(client)
		if client and client.EmailAddress not in emails['email']:
			emails['email'].append(i.getClient().EmailAddress)
			emails['name'].append(i.getClient().Name)
	for i in clients:
		for j in i.getContacts():
			if j.EmailAddress not in emails['email']:
				emails['email'].append(j.EmailAddress)
				emails['name'].append(j.Firstname + ' ' + j.Surname)
	return pd.DataFrame(emails)
