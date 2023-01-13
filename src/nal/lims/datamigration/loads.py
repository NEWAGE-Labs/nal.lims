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
    import_labcontacts()
    print("Sucessfully Imported labcontacts")

    #analysiscategories
    print("Importing analysiscategories")
    import_analysiscategories()
    print("Sucessfully Imported analysiscategories")

    #instrumenttypes
    print("Importing instrumenttypes")
    import_instrumenttypes()
    print("Sucessfully Imported instrumenttypes")

    #manufacturers
    print("Importing manufacturers")
    import_manufacturers()
    print("Sucessfully Imported manufacturers")

    #suppliers
    print("Importing suppliers")
    import_suppliers()
    print("Sucessfully Imported suppliers")

    #subgroups
    print("Importing subgroups")
    import_subgroups()
    print("Sucessfully Imported subgroups")

    #sdglabels
    print("Importing sdglabels")
    import_sdglabels()
    print("Sucessfully Imported sdglabels")

    #sampletypes
    print("Importing sampletypes")
    import_sampletypes()
    print("Sucessfully Imported sampletypes")

    #instruments
    print("Importing instruments")
    import_instruments()
    print("Sucessfully Imported instruments")

    #methods
    print("Importing methods")
    import_methods()
    print("Sucessfully Imported methods")

    #analysisservices
    print("Importing analysisservices")
    import_analysisservices()
    print("Sucessfully Imported analysisservices")

    #analysisspecs
    print("Importing analysisspecs")
    import_analysisspecs()
    print("Sucessfully Imported analysisspecs")

    #analysisprofiles
    print("Importing analysisprofiles")
    import_analysisprofiles()
    print("Sucessfully Imported analysisprofiles")

    #calculations
    print("Importing calculations")
    import_calculations()
    print("Sucessfully Imported calculations")

    ## Transaction Entities ##

    #clients
    print("Importing clients")
    import_clients()
    print("Sucessfully Imported clients")

    #clientcontacts
    print("Importing clientcontacts")
    import_clientcontacts()
    print("Sucessfully Imported clientcontacts")

    #samplelocations
    print("Importing samplelocations")
    import_samplelocations()
    print("Sucessfully Imported samplelocations")

    #sdgs
    print("Importing sdgs")
    import_sdgs()
    print("Sucessfully Imported sdgs")

    #samples
    print("Importing samples")
    import_samples()
    print("Sucessfully Imported samples")

def import_analysiscatories(file):

    create_loc = api.get_portal().bika_setup.bika_analysiscategories

    df = pd.read_csv(file,keep_default_na=False)
    for i,row in df.iterrows():

def import_analysisprofiles(file):

    create_loc = api.get_portal().bika_setup.bika_analysisprofiles

    df = pd.read_csv(file,keep_default_na=False)
    for i,row in df.iterrows():

def import_analysisservices(file):

    create_loc = api.get_portal().bika_setup.bika_analysisservices

    df = pd.read_csv(file,keep_default_na=False)
    for i,row in df.iterrows():

def import_analysisspecs(file):

    create_loc = api.get_portal().bika_setup.bika_analysisspecs

    df = pd.read_csv(file,keep_default_na=False)
    for i,row in df.iterrows():

def import_calculations(file):

    create_loc = api.get_portal().bika_setup.bika_calculations

    df = pd.read_csv(file,keep_default_na=False)
    for i,row in df.iterrows():

def import_clientcontacts(file):

    df = pd.read_csv(file,keep_default_na=False)
    for i,row in df.iterrows():

def import_clients(file):

    create_loc = api.get_portal().clients

    df = pd.read_csv(file,keep_default_na=False)
    for i,row in df.iterrows():

def import_instruments(file):

    create_loc = api.get_portal().bika_setup.bika_instruments

    df = pd.read_csv(file,keep_default_na=False)
    for i,row in df.iterrows():

def import_instrumenttypes(file):

    create_loc = api.get_portal().bika_setup.bika_instrumenttypes

    df = pd.read_csv(file,keep_default_na=False)
    for i,row in df.iterrows():

def import_labcontacts(file):

    create_loc = api.get_portal().bika_setup.bika_labcontacts

    df = pd.read_csv(file,keep_default_na=False)
    labcontacts = map(api.get_object,api.search({'portal_type':'LabContact'}))
    names = [lc.Firstname + ' ' + lc.Surname for lc in labcontacts]
    for i,row in df.iterrows():
        if str(row["Firstname"] + ' ' row["Surname"]) not in names:
            api.create(create_loc, Firstname = row["Firstname"], Surname=row["Surname"], Initials=row["Initials"],EmailAddress=row["EmailAddress"])

    return None

def import_manufacturers(file):

    create_loc = api.get_portal().bika_setup.bika_manufacturers

    df = pd.read_csv(file,keep_default_na=False)
    for i,row in df.iterrows():

def import_methods(file):

    create_loc = api.get_portal().methods

    df = pd.read_csv(file,keep_default_na=False)
    for i,row in df.iterrows():

def import_samplelocations(file):

    df= pd.read_csv(file,keep_default_na=False)
    for i,row in df.iterrows():

def import_samples(file):

    df = pd.read_csv(file,keep_default_na=False)
    for i,row in df.iterrows():

def import_sampletypes(file):

    create_loc = api.get_portal().bika_setup.bika_sampletypes

    df = pd.read_csv(file,keep_default_na=False)
    for i,row in df.iterrows():

def import_sdglabels(file):

    create_loc = api.get_portal().bika_setup.bika_batchlabels

    df = pd.read_csv(file,keep_default_na=False)
    for i,row in df.iterrows():

def import_sdgs(file):

    df = pd.read_csv(file,keep_default_na=False)
    for i,row in df.iterrows():

def import_subgroups(file):

    create_loc = api.get_portal().bika_setup.bika_subgroups

    df = pd.read_csv(file,keep_default_na=False)
    for i,row in df.iterrows():

def import_suppliers(file):

    create_loc = api.get_portal().bika_setup.bika_suppliers

    df = pd.read_csv(file,keep_default_na=False)
    for i,row in df.iterrows():
