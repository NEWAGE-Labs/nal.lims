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
    import_labcontacts(labcontacts)
    print("Sucessfully Imported labcontacts")

    #analysiscategories
    print("Importing analysiscategories")
    import_analysiscategories(analysiscategories)
    print("Sucessfully Imported analysiscategories")

    #instrumenttypes
    print("Importing instrumenttypes")
    import_instrumenttypes(instrumenttypes)
    print("Sucessfully Imported instrumenttypes")

    #manufacturers
    print("Importing manufacturers")
    import_manufacturers(manufacturers)
    print("Sucessfully Imported manufacturers")

    #suppliers
    print("Importing suppliers")
    import_suppliers(suppliers)
    print("Sucessfully Imported suppliers")

    #subgroups
    print("Importing subgroups")
    import_subgroups(subgroups)
    print("Sucessfully Imported subgroups")

    #sdglabels
    print("Importing sdglabels")
    import_sdglabels(sdglabels)
    print("Sucessfully Imported sdglabels")

    #sampletypes
    print("Importing sampletypes")
    import_sampletypes(sampletypes)
    print("Sucessfully Imported sampletypes")

    #methods
    print("Importing methods")
    import_methods(methods)
    print("Sucessfully Imported methods")

    #instruments
    print("Importing instruments")
    import_instruments(instruments)
    print("Sucessfully Imported instruments")

    #analysisservices
    print("Importing analysisservices")
    import_analysisservices(analysisservices)
    print("Sucessfully Imported analysisservices")

    #analysisspecs
    print("Importing analysisspecs")
    import_analysisspecs(analysisspecs)
    print("Sucessfully Imported analysisspecs")

    #analysisprofiles
    print("Importing analysisprofiles")
    import_analysisprofiles(analysisprofiles)
    print("Sucessfully Imported analysisprofiles")

    #calculations
    print("Importing calculations")
    import_calculations(calculations)
    print("Sucessfully Imported calculations")

    ## Transaction Entities ##

    #clients
    print("Importing clients")
    import_clients(clients)
    print("Sucessfully Imported clients")

    #clientcontacts
    print("Importing clientcontacts")
    import_clientcontacts(clientcontacts)
    print("Sucessfully Imported clientcontacts")

    #samplelocations
    print("Importing samplelocations")
    import_samplelocations(samplelocations)
    print("Sucessfully Imported samplelocations")

    #sdgs
    print("Importing sdgs")
    import_sdgs(sdgs)
    print("Sucessfully Imported sdgs")

    #samples
    print("Importing samples")
    import_samples(samples)
    print("Sucessfully Imported samples")

def import_analysiscategories(file):

    create_loc = api.get_portal().bika_setup.bika_analysiscategories
    df = pd.read_csv(file,keep_default_na=False)
    analysiscategories = map(api.get_object,api.search({'portal_type':'AnalysisCategory'}))
    titles = [ac.title for ac in analysiscategories]
    for i,row in df.iterrows():
        if str(row["title"]) not in titles:
            api.create(create_loc, "AnalysisCategory", title=row["title"],description=row["description"])
    return None

def import_analysisprofiles(file):

    create_loc = api.get_portal().bika_setup.bika_analysisprofiles

    df = pd.read_csv(file,keep_default_na=False)
    # for i,row in df.iterrows():

    return None

def import_analysisservices(file):

    create_loc = api.get_portal().bika_setup.bika_analysisservices

    df = pd.read_csv(file,keep_default_na=False)
    analysisservices = map(api.get_object,api.search({'portal_type':'AnalysisService'}))
    keywords = [a.Keyword for a in analysisservices]
    for i,row in df.iterrows():
        if str(row["Keyword"]) not in keywords:
            cateogries = api.search({'portal_type':'AnalysisCategory','title':str(row['category'])})
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
    return None

def import_analysisspecs(file):

    create_loc = api.get_portal().bika_setup.bika_analysisspecs

    df = pd.read_csv(file,keep_default_na=False)
    # for i,row in df.iterrows():

    return None

def import_calculations(file):

    create_loc = api.get_portal().bika_setup.bika_calculations

    df = pd.read_csv(file,keep_default_na=False)
    # for i,row in df.iterrows():

    return None

def import_clientcontacts(file):

    df = pd.read_csv(file,keep_default_na=False)
    # for i,row in df.iterrows():

    return None

def import_clients(file):

    create_loc = api.get_portal().clients

    df = pd.read_csv(file,keep_default_na=False)
    # for i,row in df.iterrows():

    return None

def import_instruments(file):

    create_loc = api.get_portal().bika_setup.bika_instruments

    df = pd.read_csv(file,keep_default_na=False)
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
    return None

def import_instrumenttypes(file):

    create_loc = api.get_portal().bika_setup.bika_instrumenttypes
    df = pd.read_csv(file,keep_default_na=False)
    instrumenttypes = map(api.get_object,api.search({'portal_type':'InstrumentType'}))
    titles = [it.title for it in instrumenttypes]
    for i,row in df.iterrows():
        if str(row["title"]) not in titles:
            api.create(create_loc, "InstrumentType", title=row["title"],description=row["description"])
    return None

def import_labcontacts(file):
    create_loc = api.get_portal().bika_setup.bika_labcontacts
    df = pd.read_csv(file,keep_default_na=False)
    labcontacts = map(api.get_object,api.search({'portal_type':'LabContact'}))
    names = [lc.Firstname + ' ' + lc.Surname for lc in labcontacts]
    for i,row in df.iterrows():
        if str(row["Firstname"] + ' ' + row["Surname"]) not in names:
            api.create(create_loc, "LabContact", Firstname = row["Firstname"], Surname=row["Surname"], Initials=row["Initials"],EmailAddress=row["EmailAddress"])
    return None

def import_manufacturers(file):

    create_loc = api.get_portal().bika_setup.bika_manufacturers
    df = pd.read_csv(file,keep_default_na=False)
    manufacturers = map(api.get_object,api.search({'portal_type':'Manufacturer'}))
    titles = [m.title for m in manufacturers]
    for i,row in df.iterrows():
        if str(row["title"]) not in titles:
            api.create(create_loc, "Manufacturer", title=row["title"],description=row["description"])
    return None

def import_methods(file):

    create_loc = api.get_portal().methods

    df = pd.read_csv(file,keep_default_na=False)
    methods = map(api.get_object,api.search({'portal_type':'Method'}))
    titles = [m.title for m in methods]
    for i,row in df.iterrows():
        if str(row["title"]) not in titles:
            api.create(create_loc, "Method", title=row["title"],description=row["description"])
    return None

def import_samplelocations(file):

    df= pd.read_csv(file,keep_default_na=False)
    # for i,row in df.iterrows():

    return None

def import_samples(file):

    df = pd.read_csv(file,keep_default_na=False)
    # for i,row in df.iterrows():

    return None

def import_sampletypes(file):

    create_loc = api.get_portal().bika_setup.bika_sampletypes

    df = pd.read_csv(file,keep_default_na=False)
    sampletypes = map(api.get_object,api.search({'portal_type':'SampleType'}))
    titles = [st.title for st in sampletypes]
    for i,row in df.iterrows():
        if str(row["title"]) not in titles:
            api.create(create_loc, "SampleType", title=row["title"],description=row["description"])
    return None

def import_sdglabels(file):

    create_loc = api.get_portal().bika_setup.bika_batchlabels

    df = pd.read_csv(file,keep_default_na=False)
    batchlabels = map(api.get_object,api.search({'portal_type':'BatchLabel'}))
    titles = [bl.title for bl in batchlabels]
    for i,row in df.iterrows():
        if str(row["title"]) not in titles:
            api.create(create_loc, "BatchLabel", title=row["title"],description=row["description"])
    return None

def import_sdgs(file):

    df = pd.read_csv(file,keep_default_na=False)
    # for i,row in df.iterrows():

    return None

def import_subgroups(file):

    create_loc = api.get_portal().bika_setup.bika_subgroups

    df = pd.read_csv(file,keep_default_na=False)
    subgroups = map(api.get_object,api.search({'portal_type':'SubGroup'}))
    titles = [sg.title for sg in subgroups]
    for i,row in df.iterrows():
        if str(row["title"]) not in titles:
            api.create(create_loc, "SubGroup", title=row["title"],description=row["description"])
    return None

def import_suppliers(file):

    create_loc = api.get_portal().bika_setup.bika_suppliers

    df = pd.read_csv(file,keep_default_na=False)
    suppliers = map(api.get_object,api.search({'portal_type':'Supplier'}))
    names = [s.Name for s in suppliers]
    for i,row in df.iterrows():
        if str(row["Name"]) not in names:
            api.create(create_loc, "Supplier", Name=row["Name"],EmailAddress=row["EmailAddress"])
    return None
