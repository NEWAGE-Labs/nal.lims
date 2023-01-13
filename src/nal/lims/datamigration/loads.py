from bika.lims import api
import pandas as pd
from datetime import datetime
import os

def import_from_csvs(eid):

    dir = 'Extracts ' + eid + '/'

    analysiscategories = dir + 'analysiscategories_'+eid+'.csv'
    analysisprofiles = dir + 'analysisprofiles_'+eid+'.csv'
    analysisservices = dir + 'analysisservices_'+eid+'.csv'
    analysisspecs = dir + 'analysisspecs_'+eid+'.csv'
    calculations = dir + 'calculations_'+eid+'.csv'
    clientcontacts = dir + 'clientcontacts_'+eid+'.csv'
    clients = dir + 'clients_'+eid+'.csv'
    instruments = dir + 'instruments_'+eid+'.csv'
    instrumenttypes = dir + 'instrumenttypes_'+eid+'.csv'
    labcontacts = dir + 'labcontacts_'+eid+'.csv'
    manufacturers = dir + 'manufacturers_'+eid+'.csv'
    methods = dir + 'methods_'+eid+'.csv'
    samplelocations = dir + 'samplelocations_'+eid+'.csv'
    samples = dir + 'samples_'+eid+'.csv'
    sampletypes = dir + 'sampletypes_'+eid+'.csv'
    sdglabels = dir + 'sdglabels_'+eid+'.csv'
    sdgs = dir + 'sdgs_'+eid+'.csv'
    subgroups = dir + 'subgroups_'+eid+'.csv'
    suppliers = dir + 'suppliers_'+eid+'.csv'

    ## Setup Entities ##

    #labcontacts
    print("Importing labcontacts")
    count = import_labcontacts(labcontacts)
    print("Sucessfully Imported {} labcontacts".format(count))

    #analysiscategories
    print("Importing analysiscategories")
    count = import_analysiscategories(analysiscategories)
    print("Sucessfully Imported {} analysiscategories".format(count))

    #instrumenttypes
    print("Importing instrumenttypes")
    count = import_instrumenttypes(instrumenttypes)
    print("Sucessfully Imported {} instrumenttypes".format(count))

    #manufacturers
    print("Importing manufacturers")
    count = import_manufacturers(manufacturers)
    print("Sucessfully Imported {} manufacturers".format(count))

    #suppliers
    print("Importing suppliers")
    count = import_suppliers(suppliers)
    print("Sucessfully Imported {} suppliers".format(count))

    #subgroups
    print("Importing subgroups")
    count = import_subgroups(subgroups)
    print("Sucessfully Imported {} subgroups".format(count))

    #sdglabels
    print("Importing sdglabels")
    count = import_sdglabels(sdglabels)
    print("Sucessfully Imported {} sdglabels".format(count))

    #sampletypes
    print("Importing sampletypes")
    count = import_sampletypes(sampletypes)
    print("Sucessfully Imported {} sampletypes".format(count))

    #methods
    print("Importing methods")
    count = import_methods(methods)
    print("Sucessfully Imported {} methods".format(count))

    #instruments
    print("Importing instruments")
    count = import_instruments(instruments)
    print("Sucessfully Imported {} instruments".format(count))

    #analysisservices
    print("Importing analysisservices")
    count = import_analysisservices(analysisservices)
    print("Sucessfully Imported {} analysisservices".format(count))

    #analysisspecs
    print("Importing analysisspecs")
    count = import_analysisspecs(analysisspecs)
    print("Sucessfully Imported {} analysisspecs".format(count))

    #analysisprofiles
    print("Importing analysisprofiles")
    count = import_analysisprofiles(analysisprofiles)
    print("Sucessfully Imported {} analysisprofiles".format(count))

    #calculations
    print("Importing calculations")
    count = import_calculations(calculations)
    print("Sucessfully Imported {} calculations".format(count))

    ## Transaction Entities ##

    #clients
    print("Importing clients")
    count = import_clients(clients)
    print("Sucessfully Imported {} clients".format(count))

    # #clientcontacts
    # print("Importing clientcontacts")
    # count = import_clientcontacts(clientcontacts)
    # print("Sucessfully Imported {} clientcontacts".format(count))

    #samplelocations
    print("Importing samplelocations")
    count = import_samplelocations(samplelocations)
    print("Sucessfully Imported {} samplelocations".format(count))

    #sdgs
    print("Importing sdgs")
    count = import_sdgs(sdgs)
    print("Sucessfully Imported {} sdgs".format(count))

    #samples
    print("Importing samples")
    count = import_samples(samples)
    print("Sucessfully Imported {} samples".format(count))

def import_analysiscategories(file):
    count = 0
    create_loc = api.get_portal().bika_setup.bika_analysiscategories
    df = pd.read_csv(file,keep_default_na=False,encoding="latin1")
    analysiscategories = map(api.get_object,api.search({'portal_type':'AnalysisCategory'}))
    titles = [ac.title for ac in analysiscategories]
    for i,row in df.iterrows():
        if str(row["title"]) not in titles:
            api.create(create_loc, "AnalysisCategory", title=row["title"],description=row["description"])
            count = (count + 1)
    return count

def import_analysisprofiles(file):
    count = 0
    create_loc = api.get_portal().bika_setup.bika_analysisprofiles

    df = pd.read_csv(file,keep_default_na=False,encoding="latin1")
    # for i,row in df.iterrows():

    return count

def import_analysisservices(file):
    count = 0
    create_loc = api.get_portal().bika_setup.bika_analysisservices

    df = pd.read_csv(file,keep_default_na=False,encoding="latin1")
    analysisservices = map(api.get_object,api.search({'portal_type':'AnalysisService'}))
    keywords = [a.Keyword for a in analysisservices]
    for i,row in df.iterrows():
        if str(row["Keyword"]) not in keywords:
            categories = api.search({'portal_type':'AnalysisCategory','title':str(row['category'])})
            if categories:
                category = api.get_uid(categories[0])
            api.create( create_loc,
                        "AnalysisService",
                        title=row["title"],
                        Keyword=row["Keyword"],
                        Category=category,
                        Unit=row["Unit"],
                        LowerDetectionLimit=row["LowerDetectionLimit"],
                        ShowTotal=row["ShowTotal"],
                        ShowMethodInName=row["ShowMethodInName"])
            count = (count + 1)
    return count

def import_analysisspecs(file):
    count = 0
    create_loc = api.get_portal().bika_setup.bika_analysisspecs

    df = pd.read_csv(file,keep_default_na=False,encoding="latin1")
    # for i,row in df.iterrows():

    return count

def import_calculations(file):
    count = 0
    create_loc = api.get_portal().bika_setup.bika_calculations

    df = pd.read_csv(file,keep_default_na=False,encoding="latin1")
    # for i,row in df.iterrows():

    return count

def import_clientcontacts(file):
    count = 0
    df = pd.read_csv(file,keep_default_na=False,encoding="latin1")
    clients = map(api.get_object,api.search({'portal_type':'Client'}))
    for i,row in df.iterrows():
        name = str(row["Firstname"] or '') + ' ' + str(row["Surname"] or '')
        for j in clients:
            if row["ClientID"] == j.ClientID:
            # and name not in [str(c.Firstname or '') + ' ' + str(c.Surname or '') for c in j.getContacts()]:
                create_loc = api.get_object(j)
                api.create( create_loc,
                            "Contact",
                            Firstname=row["Firstname"],
                            Surname=row["Surname"],
                            BusinessPhone=row["BusinessPhone"],
                            EmailAddress=row["EmailAddress"]
                            )
                count = (count + 1)
    return count

def import_clients(file):
    count = 0
    create_loc = api.get_portal().clients

    df = pd.read_csv(file,keep_default_na=False,encoding="latin1")
    clients = map(api.get_object,api.search({'portal_type':'Client'}))
    cids = [c.ClientID for c in clients]
    for i,row in df.iterrows():
        if row["NAL Number"] not in cids:
            PhysAddress={'country':row['PhysCountry']
                        ,'state':row['PhysState']
                        ,'district':row['PhysDistrict']
                        ,'city':row['PhysCity']
                        ,'zip':row['PhysPostal']
                        ,'address':row['PhysAddress']}

            PostAddress={'country':row['PostCountry']
                        ,'state':row['PostState']
                        ,'district':row['PostDistrict']
                        ,'city':row['PostCity']
                        ,'zip':row['PostPostal']
                        ,'address':row['PostAddress']}

            BillAddress={'country':row['BillCountry']
                        ,'state':row['BillState']
                        ,'district':row['BillDistrict']
                        ,'city':row['BillCity']
                        ,'zip':row['BillPostal']
                        ,'address':row['BillAddress']}

            api.create( create_loc,
                        "Client",
                        title=row["Name"],
                        ClientID=row["NAL Number"],
                        Phone=row["Phone"],
                        Fax=row["Fax"],
                        EmailAddress=row["Email"],
                        CSV=row["CSV"],
                        PhysicalAddress=PhysAddress,
                        PostalAddress=PostAddress,
                        BillingAddress=BillAddress,
                        MBGNumber=row["MBGNumber"],
                        TrueBlueNumber=row["TrueBlueNumber"],
                        )
            count = (count + 1)

    return count

def import_instruments(file):
    count = 0
    create_loc = api.get_portal().bika_setup.bika_instruments

    df = pd.read_csv(file,keep_default_na=False,encoding="latin1")
    instruments = map(api.get_object,api.search({'portal_type':'Instrument'}))
    titles = [i.title for i in instruments]
    for i,row in df.iterrows():
        if row["title"] not in titles:
            instrumenttypes = api.search({'portal_type':'InstrumentType','title':str(row['instrumenttype'])})
            if instrumenttypes:
                instrumenttype = api.get_uid(instrumenttypes[0])
            manufacturers = api.search({'portal_type':'Manufacturer','title':str(row['manufacturer'])})
            if manufacturers:
                manufacturer = api.get_uid(manufacturers[0])
            imethods = row["methods"].split(",")
            methods = api.search({'portal_type':'Method','title':imethods})
            api.create( create_loc, "Instrument",
                        title=row["title"],
                        AssetNumber=row["asset number"],
                        description=row["description"],
                        InstrumentType = instrumenttype,
                        Manufacturer=manufacturer,
                        Model=row["model"],
                        SerialNo=row["serial number"],
                        Methods=methods)
            count = (count + 1)
    return count

def import_instrumenttypes(file):
    count = 0
    create_loc = api.get_portal().bika_setup.bika_instrumenttypes
    df = pd.read_csv(file,keep_default_na=False,encoding="latin1")
    instrumenttypes = map(api.get_object,api.search({'portal_type':'InstrumentType'}))
    titles = [it.title for it in instrumenttypes]
    for i,row in df.iterrows():
        if str(row["title"]) not in titles:
            api.create(create_loc, "InstrumentType", title=row["title"],description=row["description"])
            count = (count + 1)
    return count

def import_labcontacts(file):
    count = 0
    create_loc = api.get_portal().bika_setup.bika_labcontacts
    df = pd.read_csv(file,keep_default_na=False,encoding="latin1")
    labcontacts = map(api.get_object,api.search({'portal_type':'LabContact'}))
    names = [lc.Firstname + ' ' + lc.Surname for lc in labcontacts]
    for i,row in df.iterrows():
        if str(row["Firstname"] + ' ' + row["Surname"]) not in names:
            api.create(create_loc, "LabContact", Firstname = row["Firstname"], Surname=row["Surname"], Initials=row["Initials"],EmailAddress=row["EmailAddress"])
            count = (count + 1)
    return count

def import_manufacturers(file):
    count = 0
    create_loc = api.get_portal().bika_setup.bika_manufacturers
    df = pd.read_csv(file,keep_default_na=False,encoding="latin1")
    manufacturers = map(api.get_object,api.search({'portal_type':'Manufacturer'}))
    titles = [m.title for m in manufacturers]
    for i,row in df.iterrows():
        if str(row["title"]) not in titles:
            api.create(create_loc, "Manufacturer", title=row["title"],description=row["description"])
            count = (count + 1)
    return count

def import_methods(file):
    count = 0
    create_loc = api.get_portal().methods

    df = pd.read_csv(file,keep_default_na=False,encoding="latin1")
    methods = map(api.get_object,api.search({'portal_type':'Method'}))
    titles = [m.title for m in methods]
    for i,row in df.iterrows():
        if str(row["title"]) not in titles:
            api.create(create_loc, "Method", title=row["title"],description=row["description"])
            count = (count + 1)
    return count

def import_samplelocations(file):
    count = 0
    df= pd.read_csv(file,keep_default_na=False,encoding="latin1")
    clients = map(api.get_object,api.search({'portal_type':'Client'}))
    locations = map(api.get_object,api.search({'portal_type':'SamplePoint'}))
    loc_ids = [l.id for l in locations]
    for i,row in df.iterrows():
        for j in clients:
            if row["client"] == j.ClientID and str(row["locationid"]) not in loc_ids:
                create_loc = j
                loc = api.create(create_loc, "SamplePoint", title=row["title"],description=row["description"],ArchiveID=str(row["locationid"]))
                count= (count + 1)
    return count

def import_samples(file):
    count = 0
    # df = pd.read_csv(file,keep_default_na=False,encoding="latin1")
    # clients = map(api.get_object,api.search({'portal_type':'Client'}))
    # locations = map(api.get_object,api.search({'portal_type':'SamplePoint'}))
    # contacts = map(api.get_object,api.search({'portal_type':'Contact'}))
    # sdgs = map(api.get_object,api.search({'portal_type':'Batch'}))
    # samples = map(api.get_object,api.search({'portal_type':'AnalysisRequest'}))
    # sids = [s.id for s in samples]
    # # for i,row in df.iterrows():
    # #     if row['sid'] not in sids:
    # #         client = api.get_object(api.search({'portal_type':'Client','getClientID':row['client']})[0])
    # #         create_loc = client
    # #         sdg = api.get_object(api.search({'portal_type':'Batch','id':row['sdg']})[0])
    # #         location =
    # #         #profile
    # #         type =
    # #         #ol
    # #         subgroup =
    # #         api.create

    return count

def import_sampletypes(file):
    count = 0
    create_loc = api.get_portal().bika_setup.bika_sampletypes

    df = pd.read_csv(file,keep_default_na=False,encoding="latin1")
    sampletypes = map(api.get_object,api.search({'portal_type':'SampleType'}))
    titles = [st.title for st in sampletypes]
    for i,row in df.iterrows():
        if str(row["title"]) not in titles:
            api.create(create_loc, "SampleType", title=row["title"],description=row["description"])
            count = (count + 1)
    return count

def import_sdglabels(file):
    count = 0
    create_loc = api.get_portal().bika_setup.bika_batchlabels

    df = pd.read_csv(file,keep_default_na=False,encoding="latin1")
    batchlabels = map(api.get_object,api.search({'portal_type':'BatchLabel'}))
    titles = [bl.title for bl in batchlabels]
    for i,row in df.iterrows():
        if str(row["title"]) not in titles:
            api.create(create_loc, "BatchLabel", title=row["title"],description=row["description"])
            count = (count + 1)
    return count

def import_sdgs(file):
    count = 0
    df = pd.read_csv(file,keep_default_na=False,encoding="latin1")
    clients = map(api.get_object,api.search({'portal_type':'Client'}))
    contacts = map(api.get_object,api.search({'portal_type':'Contact'}))
    sdgs = map(api.get_object,api.search({'portal_type':'Batch'}))
    bids = [s.BatchID for s in sdgs]
    for i,row in df.iterrows():
        for j in clients:
            if row["Client"] == j.ClientID and str(row["BatchID"]) not in bids:
                print("We should be creating an SDG for: {}".format(row["title"]))
                create_loc = j
                client_uid = api.get_uid(j)
                sdglabels = []
                # for label in row["BatchLabels"].split(","):
                #     blabels = api.search({'portal_type':'BatchLabel','title':label})
                #     if blabels:
                #         sdglabels.append(api.get_object(blabels[0]))
                pcontact = None
                scontact = None
                gcontact = None
                for contact in contacts:
                    name = contact.Firstname + ' ' + contact.Surname
                    contact_uid = api.get_uid(contact)
                    if name == row["ProjectContact"] and contact.aq_parent == j:
                        pcontact = contact_uid
                    if name == row["SamplerContact"] and contact.aq_parent == j:
                        scontact = contact_uid
                    if name == row["GrowerContact"] and contact.aq_parent == j:
                        gcontact = contact_uid
                b = api.create( create_loc,
                            "Batch",
                            title=row["title"],
                            description=row["description"],
                            BatchID=row["BatchID"],
                            Client=client_uid,
                            BatchLabels=sdglabels,
                            SDGDate=row["SDGDate"],
                            SDGTime=row["SDGTime"],
                            ReportContact=row["ReportContact"],
                            ProjectContact=pcontact,
                            SamplerContact=scontact,
                            GrowerContact=gcontact
                            )
                b.BatchID = row["BatchID"]
                b.aq_parent.manage_renameObject(b.id,str(row["BatchID"]))
                count = (count + 1)

    return count

def import_subgroups(file):
    count = 0
    create_loc = api.get_portal().bika_setup.bika_subgroups

    df = pd.read_csv(file,keep_default_na=False,encoding="latin1")
    subgroups = map(api.get_object,api.search({'portal_type':'SubGroup'}))
    titles = [sg.title for sg in subgroups]
    for i,row in df.iterrows():
        if str(row["title"]) not in titles:
            api.create(create_loc, "SubGroup", title=row["title"],description=row["description"])
            count = (count + 1)
    return count

def import_suppliers(file):
    count = 0
    create_loc = api.get_portal().bika_setup.bika_suppliers

    df = pd.read_csv(file,keep_default_na=False,encoding="latin1")
    suppliers = map(api.get_object,api.search({'portal_type':'Supplier'}))
    names = [s.Name for s in suppliers]
    for i,row in df.iterrows():
        if str(row["Name"]) not in names:
            api.create(create_loc, "Supplier", title=row["Name"],EmailAddress=row["EmailAddress"])
            count = (count + 1)
    return count
