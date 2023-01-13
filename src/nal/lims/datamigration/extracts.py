
from bika.lims import api
import pandas as pd
from datetime import datetime
import os

def extract_to_csvs():
    now = datetime.now().strftime("%d%m%Y%H%M%S")
    cwd = os.getcwd()
    dir = 'Extracts ' + now
    path = cwd + '/' + dir
    os.mkdir(path)

    #Client
    file = '{}/clients_{}.csv'.format(dir,now)
    get_clients_as_df().to_csv(file,encoding='utf-8')
    print("-Extracted Client Data to "+file)

    #Lab Contact
    file = '{}/labcontacts_{}.csv'.format(dir,now)
    get_labcontacts_as_df().to_csv(file,encoding='utf-8')
    print("-Extracted LabContact Data to "+file)

    #Method
    file = '{}/methods_{}.csv'.format(dir,now)
    get_methods_as_df().to_csv(file,encoding='utf-8')
    print("-Extracted Method Data to "+file)

    #SDG Label
    file = '{}/sdglabels_{}.csv'.format(dir,now)
    get_sdglabels_as_df().to_csv(file,encoding='utf-8')
    print("-Extracted SDG Label Data to "+file)

    #Sample Type
    file = '{}/sampletypes_{}.csv'.format(dir,now)
    get_sample_types_as_df().to_csv(file,encoding='utf-8')
    print("-Extracted Sample Type Data to "+file)

    #Analysis Category
    file = '{}/analysiscategories_{}.csv'.format(dir,now)
    get_analysis_categories_as_df().to_csv(file,encoding='utf-8')
    print("-Extracted Analysis Category Data to "+file)

    #Instrument Type
    file = '{}/instrumenttypes_{}.csv'.format(dir,now)
    get_instrument_types_as_df().to_csv(file,encoding='utf-8')
    print("-Extracted Instrument Type Data to "+file)

    #Manufacturer
    file = '{}/manufacturers_{}.csv'.format(dir,now)
    get_manufacturers_as_df().to_csv(file,encoding='utf-8')
    print("-Extracted Manufacturer Data to "+file)

    #Supplier
    file = '{}/suppliers_{}.csv'.format(dir,now)
    get_suppliers_as_df().to_csv(file,encoding='utf-8')
    print("-Extracted Supplier Data to "+file)

    #Instrument
    file = '{}/instruments_{}.csv'.format(dir,now)
    get_instruments_as_df().to_csv(file,encoding='utf-8')
    print("-Extracted Instrument Data to "+file)

    #Sample Locations
    file = '{}/samplelocations_{}.csv'.format(dir,now)
    get_samplelocations_as_df().to_csv(file,encoding='utf-8')
    print("-Extracted Sample Location Data to "+file)

    #Client Contact
    file = '{}/clientcontacts_{}.csv'.format(dir,now)
    get_clientcontacts_as_df().to_csv(file,encoding='utf-8')
    print("-Extracted Client Contact Data to "+file)

    #Sub-Groups (Pairs)
    file = '{}/subgroups_{}.csv'.format(dir,now)
    get_subgroups_as_df().to_csv(file,encoding='utf-8')
    print("-Extracted Subgroup Data to "+file)

    #SDG
    file = '{}/sdgs_{}.csv'.format(dir,now)
    get_sdgs_as_df().to_csv(file,encoding='utf-8')
    print("-Extracted SDG Data to "+file)

    #Analysis Services
    file = '{}/analysisservices_{}.csv'.format(dir,now)
    get_analysis_services_as_df().to_csv(file,encoding='utf-8')
    print("-Extracted Analysis Service Data to "+file)

    #Analysis Specs
    file = '{}/analysisspecs_{}.csv'.format(dir,now)
    get_analysis_specs_as_df().to_csv(file,encoding='utf-8')
    print("-Extracted Analysis Spec Data to "+file)

    #Calculations
    file = '{}/calculations_{}.csv'.format(dir,now)
    get_calculations_as_df().to_csv(file,encoding='utf-8')
    print("-Extracted Calculation Data to "+file)

    #Analysis Profiles
    file = '{}/analysisprofiles_{}.csv'.format(dir,now)
    get_analysis_profiles_as_df().to_csv(file,encoding='utf-8')
    print("-Extracted Analysis Profile Data to "+file)

    # Samples
    file = '{}/samples_{}.csv'.format(dir,now)
    get_samples_as_df().to_csv(file,encoding='utf-8')
    print("-Extracted Sample Data to "+file)

    # Analyses
    file = '{}/analyses_{}.csv'.format(dir,now)
    get_analyses_as_df().to_csv(file,encoding='utf-8')
    print("-Extracted Analysis Data to "+file)

    return None

def get_clients_as_df():
    """
    :return: Returns a DataFrame of active Clients. Each row is a Client \
    Each column is a Field.
    :rtype: pandas.DataFrame
    :param None: No Parameters

    **Columns**:
    - Column list is define inside the local variable 'cols'
    """

    clients = api.search({'portal_type':'Client'})
    cols = [
        #Default
        'id',
        'Name',
        'NAL Number',
        'Phone',
        'Fax',
        'Email',
        'CSV',
        #Addresses
        ## Physical Address
        'PhysCountry',
        'PhysState',
        'PhysDistrict',
        'PhysCity',
        'PhysPostal',
        'PhysAddress',
        ## Postal Address
        'PostCountry',
        'PostState',
        'PostDistrict',
        'PostCity',
        'PostPostal',
        'PostAddress',
        ## Billing Address
        'BillCountry',
        'BillState',
        'BillDistrict',
        'BillCity',
        'BillPostal',
        'BillAddress',
        #Bank details
        'Bank Account Type',
        'Bank Account Name',
        'Bank Account Number',
        'Bank Name',
        'Bank Branch',
        #Grower info
        'MBGNumber',
        'TrueBlueNumber',
    ]
    client_dict = {}
    for i in cols:
        client_dict[i] = []

    for i in clients:
        if api.get_workflow_status_of(i) == 'active':
            client = api.get_object(i)
            #Default
            client_dict['id'].append(client.id) #Required
            client_dict['Name'].append(client.Name) #Required
            client_dict['NAL Number'].append(client.ClientID) #Required
            client_dict['Phone'].append(client.Phone or '')
            client_dict['Fax'].append(client.Fax or '')
            client_dict['Email'].append(client.EmailAddress or '')
            client_dict['CSV'].append(client.CSV or '')
            #Addresses
            ## Physical Address
            client_dict['PhysCountry'].append(client.PhysicalAddress.get('country',''))
            client_dict['PhysState'].append(client.PhysicalAddress.get('state',''))
            client_dict['PhysDistrict'].append(client.PhysicalAddress.get('district',''))
            client_dict['PhysCity'].append(client.PhysicalAddress.get('city',''))
            client_dict['PhysPostal'].append(client.PhysicalAddress.get('zip',''))
            client_dict['PhysAddress'].append(client.PhysicalAddress.get('address',''))
            ## Postal Address
            client_dict['PostCountry'].append(client.PostalAddress.get('country',''))
            client_dict['PostState'].append(client.PostalAddress.get('state',''))
            client_dict['PostDistrict'].append(client.PostalAddress.get('district',''))
            client_dict['PostCity'].append(client.PostalAddress.get('city',''))
            client_dict['PostPostal'].append(client.PostalAddress.get('zip',''))
            client_dict['PostAddress'].append(client.PostalAddress.get('address',''))
            ## Billing Address
            client_dict['BillCountry'].append(client.BillingAddress.get('country',''))
            client_dict['BillState'].append(client.BillingAddress.get('state',''))
            client_dict['BillDistrict'].append(client.BillingAddress.get('district',''))
            client_dict['BillCity'].append(client.BillingAddress.get('city',''))
            client_dict['BillPostal'].append(client.BillingAddress.get('zip',''))
            client_dict['BillAddress'].append(client.BillingAddress.get('address',''))
            #Bank details
            client_dict['Bank Account Type'].append(client.AccountType or '')
            client_dict['Bank Account Name'].append(client.AccountName or '')
            client_dict['Bank Account Number'].append(client.AccountNumber or '')
            client_dict['Bank Name'].append(client.BankName or '')
            client_dict['Bank Branch'].append(client.BankBranch or '')
            #Grower info
            client_dict['MBGNumber'].append(client.MBGGrowerNumber or '')
            client_dict['TrueBlueNumber'].append(client.TBGrowerNumber or '')

    return pd.DataFrame(client_dict)[cols]

def get_labcontacts_as_df():
    """
    :return: Returns a DataFrame of active LabContacts
    :rtype: DataFrame
    """

    labcontacts = api.search({'portal_type':'LabContact'})
    cols = [
        'Firstname',
        'Surname',
        'Initials',
        'EmailAddress',
    ]

    labcontact_dict = {}
    for i in cols:
        labcontact_dict[i] = []

    for i in labcontacts:
        if api.get_workflow_status_of(i) == 'active':
            labcontact = api.get_object(i)
            labcontact_dict['Firstname'].append(labcontact.Firstname) #Required
            labcontact_dict['Surname'].append(labcontact.Surname) #Required
            labcontact_dict['Initials'].append(labcontact.Initials or '')
            labcontact_dict['EmailAddress'].append(labcontact.EmailAddress or '')

    return pd.DataFrame(labcontact_dict)[cols]

def get_methods_as_df():
    """
    :return: Returns a DataFrame of active Methods
    :rtype: DataFrame
    """

    methods = api.search({'portal_type':"Method"})
    cols = [
        'title',
        'description',
        'accredited',
    ]

    method_dict = {}
    for i in cols:
        method_dict[i] = []

    for i in methods:
        if api.get_workflow_status_of(i) == 'active':
            method = api.get_object(i)
            method_dict['title'].append(method.title) #Required
            method_dict['description'].append(method.description or '')
            method_dict['accredited'].append(method.Accredited or '')

    return pd.DataFrame(method_dict)[cols]

def get_sdglabels_as_df():
    """
    :return: Returns a DataFrame of active SDG Labels
    :rtype: DataFrame
    """

    sdglabels = api.search({'portal_type':"BatchLabel"})
    cols = [
        'title',
        'description',
    ]

    sdglabel_dict = {}
    for i in cols:
        sdglabel_dict[i] = []

    for i in sdglabels:
        if api.get_workflow_status_of(i) == 'active':
            sdglabel = api.get_object(i)
            sdglabel_dict['title'].append(sdglabel.title) #Required
            sdglabel_dict['description'].append(sdglabel.description or '')

    return pd.DataFrame(sdglabel_dict)[cols]

def get_sample_types_as_df():
    """
    :return: Returns a DataFrame of active Sample Types
    :rtype: DataFrame
    """

    stypes = api.search({'portal_type':"SampleType"})
    cols = [
        'title',
        'description',
    ]

    stype_dict = {}
    for i in cols:
        stype_dict[i] = []

    for i in stypes:
        if api.get_workflow_status_of(i) == 'active':
            stype = api.get_object(i)
            stype_dict['title'].append(stype.title) #Required
            stype_dict['description'].append(stype.description or '')

    return pd.DataFrame(stype_dict)[cols]

def get_analysis_categories_as_df():
    """
    :return: Returns a DataFrame of active Analysis Categories
    :rtype: DataFrame
    """

    categories = api.search({'portal_type':"AnalysisCategory"})
    cols = [
        'title',
        'description',
    ]

    category_dict = {}
    for i in cols:
        category_dict[i] = []

    for i in categories:
        if api.get_workflow_status_of(i) == 'active':
            category = api.get_object(i)
            category_dict['title'].append(category.title) #Required
            category_dict['description'].append(category.description or '')

    return pd.DataFrame(category_dict)[cols]

def get_instrument_types_as_df():
    """
    :return: Returns a DataFrame of active Instrument Types
    :rtype: DataFrame
    """

    itypes = api.search({'portal_type':"InstrumentType"})
    cols = [
        'title',
        'description',
    ]

    itype_dict = {}
    for i in cols:
        itype_dict[i] = []

    for i in itypes:
        if api.get_workflow_status_of(i) == 'active':
            itype = api.get_object(i)
            itype_dict['title'].append(itype.title) #Required
            itype_dict['description'].append(itype.description or '')

    return pd.DataFrame(itype_dict)[cols]

def get_manufacturers_as_df():
    """
    :return: Returns a DataFrame of active Manufacturers
    :rtype: DataFrame
    """

    manufacturers = api.search({'portal_type':"Manufacturer"})
    cols = [
        'title',
        'description',
    ]

    manufacturer_dict = {}
    for i in cols:
        manufacturer_dict[i] = []

    for i in manufacturers:
        if api.get_workflow_status_of(i) == 'active':
            manufacturer = api.get_object(i)
            manufacturer_dict['title'].append(manufacturer.title) #Required
            manufacturer_dict['description'].append(manufacturer.description or '')

    return pd.DataFrame(manufacturer_dict)[cols]

def get_suppliers_as_df():
    """
    :return: Returns a DataFrame of active Suppliers
    :rtype: DataFrame
    """

    suppliers = api.search({'portal_type':"Supplier"})
    cols = [
        'Name',
        'Tax ID',
        'Phone',
        'Fax',
        'Remarks',
        'Website',
        'EmailAddress',
        ## Physical Address
        'PhysCountry',
        'PhysState',
        'PhysDistrict',
        'PhysCity',
        'PhysPostal',
        'PhysAddress',
        ## Postal Address
        'PostCountry',
        'PostState',
        'PostDistrict',
        'PostCity',
        'PostPostal',
        'PostAddress',
        ## Billing Address
        'BillCountry',
        'BillState',
        'BillDistrict',
        'BillCity',
        'BillPostal',
        'BillAddress',
        #Bank details
        'Bank Account Type',
        'Bank Account Name',
        'Bank Account Number',
        'Bank Name',
        'Bank Branch',
    ]

    supplier_dict = {}
    for i in cols:
        supplier_dict[i] = []

    for i in suppliers:
        if api.get_workflow_status_of(i) == 'active':
            supplier = api.get_object(i)
            supplier_dict['Name'].append(supplier.Name) #Required
            supplier_dict['Tax ID'].append(supplier.TaxNumber or '')
            supplier_dict['Phone'].append(supplier.Phone or '')
            supplier_dict['Fax'].append(supplier.Fax or '')
            supplier_dict['Remarks'].append(supplier.getRemarks() or '')
            supplier_dict['Website'].append(supplier.Website or '')
            supplier_dict['EmailAddress'].append(supplier.EmailAddress or '')
            ## Physical Address
            supplier_dict['PhysCountry'].append(supplier.PhysicalAddress.get('country',''))
            supplier_dict['PhysState'].append(supplier.PhysicalAddress.get('state',''))
            supplier_dict['PhysDistrict'].append(supplier.PhysicalAddress.get('district',''))
            supplier_dict['PhysCity'].append(supplier.PhysicalAddress.get('city',''))
            supplier_dict['PhysPostal'].append(supplier.PhysicalAddress.get('zip',''))
            supplier_dict['PhysAddress'].append(supplier.PhysicalAddress.get('address',''))
            ## Postal Address
            supplier_dict['PostCountry'].append(supplier.PostalAddress.get('country',''))
            supplier_dict['PostState'].append(supplier.PostalAddress.get('state',''))
            supplier_dict['PostDistrict'].append(supplier.PostalAddress.get('district',''))
            supplier_dict['PostCity'].append(supplier.PostalAddress.get('city',''))
            supplier_dict['PostPostal'].append(supplier.PostalAddress.get('zip',''))
            supplier_dict['PostAddress'].append(supplier.PostalAddress.get('address',''))
            ## Billing Address
            supplier_dict['BillCountry'].append(supplier.BillingAddress.get('country',''))
            supplier_dict['BillState'].append(supplier.BillingAddress.get('state',''))
            supplier_dict['BillDistrict'].append(supplier.BillingAddress.get('district',''))
            supplier_dict['BillCity'].append(supplier.BillingAddress.get('city',''))
            supplier_dict['BillPostal'].append(supplier.BillingAddress.get('zip',''))
            supplier_dict['BillAddress'].append(supplier.BillingAddress.get('address',''))
            #Bank details
            supplier_dict['Bank Account Type'].append(supplier.AccountType or '')
            supplier_dict['Bank Account Name'].append(supplier.AccountName or '')
            supplier_dict['Bank Account Number'].append(supplier.AccountNumber or '')
            supplier_dict['Bank Name'].append(supplier.BankName or '')
            supplier_dict['Bank Branch'].append(supplier.BankBranch or '')

    return pd.DataFrame(supplier_dict)[cols]

def get_instruments_as_df():
    """
    :return: Returns a DataFrame of active Instruments
    :rtype: DataFrame
    """

    instruments = api.search({'portal_type':"Instrument"})
    cols = [
        'title',
        'asset number',
        'description',
        'instrumenttype',
        'manufacturer',
        'supplier',
        'model',
        'serial number',
        'methods',
    ]

    instrument_dict = {}
    for i in cols:
        instrument_dict[i] = []

    for i in instruments:
        if api.get_workflow_status_of(i) == 'active':
            instrument = api.get_object(i)
            instrument_dict['title'].append(instrument.title) #Required
            instrument_dict['asset number'].append(instrument.AssetNumber or '')
            instrument_dict['description'].append(instrument.description or '')
            itype = instrument.getReferences('InstrumentInstrumentType')
            if itype:
                instrument_dict['instrumenttype'].append(itype[0].title)
            else:
                instrument_dict['instrumenttype'].append('')
            manufacturer = instrument.getReferences('InstrumentManufacturer')
            if manufacturer:
                instrument_dict['manufacturer'].append(manufacturer[0].title)
            else:
                instrument_dict['manufacturer'].append('')
            supplier = instrument.getReferences('InstrumentSupplier')
            if supplier:
                instrument_dict['supplier'].append(supplier[0].title)
            else:
                instrument_dict['supplier'].append('')
            instrument_dict['model'].append(instrument.Model or '')
            instrument_dict['serial number'].append(instrument.SerialNo or '')
            methods = instrument.getReferences('InstrumentMethods')
            if methods:
                instrument_dict['methods'].append(','.join([m.title for m in map(api.get_object,methods)]) or '')
            else:
                instrument_dict['methods'].append('')

    return pd.DataFrame(instrument_dict)[cols]

def get_samplelocations_as_df():
    """
    :return: Returns a DataFrame of active Sample Locations
    :rtype: DataFrame
    """

    locations = api.search({'portal_type':"SamplePoint"})
    cols = [
        'locationid',
        'client',
        'title',
        'description',
        'formatted address',
        'water source type',
        'wssn'
    ]

    location_dict = {}
    for i in cols:
        location_dict[i] = []

    for i in locations:
        if api.get_workflow_status_of(i) == 'active':
            location = api.get_object(i)
            location_dict['locationid'].append(location.getId()) #Required
            client = location.aq_parent
            print("Client is: {}".format(client))
            if client and client.getId() != 'clients':
                location_dict['client'].append(client.ClientID or '')
            else:
                location_dict['client'].append('')
            location_dict['title'].append(location.title) #Required
            location_dict['description'].append(location.description or '')
            try:
                location_dict['formatted address'].append(location.FormattedAddress)
            except AttributeError:
                location_dict['formatted address'].append('')
            try:
                location_dict['water source type'].append(location.WaterSourceType)
            except AttributeError:
                location_dict['water source type'].append('')
            try:
                location_dict['wssn'].append(location.WSSN)
            except AttributeError:
                location_dict['wssn'].append('')

    return pd.DataFrame(location_dict)[cols]

def get_clientcontacts_as_df():
    """
    :return: Returns a DataFrame of active Client Contacts
    :rtype: DataFrame
    """

    clientcontacts = api.search({'portal_type':"Contact"})
    cols = [
        'ClientID',
        'Firstname',
        'Initials',
        'Middlename',
        'Surname',
        'JobTitle',
        'Department',
        'EmailAddress',
        'BusinessPhone',
        'Fax',
        'HomePhone',
        'MobilePhone',
        ## Physical Address
        'PhysCountry',
        'PhysState',
        'PhysDistrict',
        'PhysCity',
        'PhysPostal',
        'PhysAddress',
        ## Postal Address
        'PostCountry',
        'PostState',
        'PostDistrict',
        'PostCity',
        'PostPostal',
        'PostAddress',
        ## Billing Address
        'BillCountry',
        'BillState',
        'BillDistrict',
        'BillCity',
        'BillPostal',
        'BillAddress',
    ]

    clientcontact_dict = {}
    for i in cols:
        clientcontact_dict[i] = []

    for i in clientcontacts:
        if api.get_workflow_status_of(i) == 'active':
            clientcontact = api.get_object(i)
            clientcontact_dict['ClientID'].append(clientcontact.getParent().ClientID or '') #Required
            clientcontact_dict['Firstname'].append(clientcontact.Firstname)
            clientcontact_dict['Initials'].append(clientcontact.Initials)
            clientcontact_dict['Middlename'].append(clientcontact.Middlename)
            clientcontact_dict['Surname'].append(clientcontact.Surname)
            clientcontact_dict['JobTitle'].append(clientcontact.JobTitle)
            clientcontact_dict['Department'].append(clientcontact.Department)
            clientcontact_dict['EmailAddress'].append(clientcontact.EmailAddress)
            clientcontact_dict['BusinessPhone'].append(clientcontact.BusinessPhone)
            clientcontact_dict['Fax'].append(clientcontact.Fax)
            clientcontact_dict['HomePhone'].append(clientcontact.HomePhone)
            clientcontact_dict['MobilePhone'].append(clientcontact.MobilePhone)
            ## Physical Address
            clientcontact_dict['PhysCountry'].append(clientcontact.PhysicalAddress.get('country',''))
            clientcontact_dict['PhysState'].append(clientcontact.PhysicalAddress.get('state',''))
            clientcontact_dict['PhysDistrict'].append(clientcontact.PhysicalAddress.get('district',''))
            clientcontact_dict['PhysCity'].append(clientcontact.PhysicalAddress.get('city',''))
            clientcontact_dict['PhysPostal'].append(clientcontact.PhysicalAddress.get('zip',''))
            clientcontact_dict['PhysAddress'].append(clientcontact.PhysicalAddress.get('address',''))
            ## Postal Address
            clientcontact_dict['PostCountry'].append(clientcontact.PostalAddress.get('country',''))
            clientcontact_dict['PostState'].append(clientcontact.PostalAddress.get('state',''))
            clientcontact_dict['PostDistrict'].append(clientcontact.PostalAddress.get('district',''))
            clientcontact_dict['PostCity'].append(clientcontact.PostalAddress.get('city',''))
            clientcontact_dict['PostPostal'].append(clientcontact.PostalAddress.get('zip',''))
            clientcontact_dict['PostAddress'].append(clientcontact.PostalAddress.get('address',''))
            ## Billing Address
            clientcontact_dict['BillCountry'].append(clientcontact.BillingAddress.get('country',''))
            clientcontact_dict['BillState'].append(clientcontact.BillingAddress.get('state',''))
            clientcontact_dict['BillDistrict'].append(clientcontact.BillingAddress.get('district',''))
            clientcontact_dict['BillCity'].append(clientcontact.BillingAddress.get('city',''))
            clientcontact_dict['BillPostal'].append(clientcontact.BillingAddress.get('zip',''))
            clientcontact_dict['BillAddress'].append(clientcontact.BillingAddress.get('address',''))

    return pd.DataFrame(clientcontact_dict)[cols]

def get_subgroups_as_df():
    """
    :return: Returns a DataFrame of active SubGroups (Pairs)
    :rtype: DataFrame
    """

    subgroups = api.search({'portal_type':"SubGroup"})
    cols = [
        'title',
        'description',
    ]

    subgroup_dict = {}
    for i in cols:
        subgroup_dict[i] = []

    for i in subgroups:
        if api.get_workflow_status_of(i) == 'active':
            subgroup = api.get_object(i)
            subgroup_dict['title'].append(subgroup.title) #Required
            subgroup_dict['description'].append(subgroup.description or '')

    return pd.DataFrame(subgroup_dict)[cols]

def get_sdgs_as_df():
    """
    :return: Returns a DataFrame of active SDG
    :rtype: DataFrame
    """

    sdgs = api.search({'portal_type':"Batch"})
    cols = [
        'title',
        'description',
        'BatchID',
        'Client',
        'ClientBatchID',
        'BatchLabels',
        'SDGDate',
        'SDGTime',
        'ReportContact',
        'ProjectContact',
        'SamplerContact',
        'GrowerContact',
        'COC',
    ]

    sdg_dict = {}
    for i in cols:
        sdg_dict[i] = []

    for i in sdgs:
        if api.get_workflow_status_of(i) == 'closed':
            sdg = api.get_object(i)
            sdg_dict['title'].append(sdg.title) #Required
            sdg_dict['description'].append(sdg.description or '')
            sdg_dict['BatchID'].append(sdg.id or '')
            sdg_dict['Client'].append(sdg.aq_parent.ClientID or '')
            sdg_dict['ClientBatchID'].append(sdg.ClientBatchID or '')
            sdg_dict['BatchLabels'].append(','.join(sdg.getLabelNames()) or '')
            sdg_dict['SDGDate'].append(sdg.SDGDate or '')
            sdg_dict['SDGTime'].append(sdg.SDGTime or '')
            sdg_dict['ReportContact'].append(sdg.ReportContact or '')
            pcontacts=sdg.getReferences(relationship="SDGProjectContact")
            if pcontacts:
                sdg_dict['ProjectContact'].append(pcontacts[0].Firstname + ' ' + pcontacts[0].Surname) ##
            else:
                sdg_dict['ProjectContact'].append('')
            scontacts=sdg.getReferences(relationship="SDGSamplerContact")
            if scontacts:
                sdg_dict['SamplerContact'].append(scontacts[0].Firstname + ' ' + scontacts[0].Surname) ##
            else:
                sdg_dict['SamplerContact'].append('')
            gcontacts=sdg.getReferences(relationship="SDGGrowerContact")
            if gcontacts:
                sdg_dict['GrowerContact'].append(gcontacts[0].Firstname + ' ' + gcontacts[0].Surname) ##
            else:
                sdg_dict['GrowerContact'].append('')
            if hasattr(sdg,'COC'):
                sdg_dict['COC'].append(sdg.COC)
            else:
                sdg_dict['COC'].append('')
#
    return pd.DataFrame(sdg_dict)[cols]

def get_analysis_services_as_df():
    """
    :return: Returns a DataFrame of active Analysis Services
    :rtype: DataFrame
    """
    #CURRENTLY UNUSED DUE TO REDESIGN OF ANALYSIS SERVICES

    analysisservices = api.search({'portal_type':"AnalysisService"})
    cols = [
        'title',
        'keyword',
    ]

    analysisservice_dict = {}
    for i in cols:
        analysisservice_dict[i] = []

    for i in analysisservices:
        if api.get_workflow_status_of(i) == 'active':
            analysisservices = api.get_object(i)
            analysisservice_dict['title'].append(analysisservices.title) #Required
            analysisservice_dict['keyword'].append(analysisservices.Keyword or '')

    return pd.DataFrame(analysisservice_dict)[cols]

def get_analysis_specs_as_df():
    """
    :return: Returns a DataFrame of active Analysis Specifications (Optimal Levels)
    :rtype: DataFrame
    """

    specs = api.search({'portal_type':"AnalysisSpec"})
    cols = [
        'title',
        'sampletype',
        'description',
        'specifications'
    ]

    spec_dict = {}
    for i in cols:
        spec_dict[i] = []

    for i in specs:
        if api.get_workflow_status_of(i) == 'active':
            spec = api.get_object(i)
            spec_dict['title'].append(spec.title) #Required
            spec_dict['description'].append(spec.description or '')
            spec_dict['sampletype'].append(spec.getSampleType().title or '')
            ranges = spec.ResultsRange
            specl = []
            for j in ranges:
                specl.append(str((j['keyword'],j['min'],j['max'])))
            spec_str = ','.join(specl)
            spec_dict['specifications'].append(spec_str)

    return pd.DataFrame(spec_dict)[cols]

def get_calculations_as_df():
    """
    :return: Returns a DataFrame of active Calculations
    :rtype: DataFrame
    """

    calculations = api.search({'portal_type':"Calculation"})
    cols = [
        'title',
        'description',
        'formula',
    ]

    calc_dict = {}
    for i in cols:
        calc_dict[i] = []

    for i in calculations:
        if api.get_workflow_status_of(i) == 'active':
            calc = api.get_object(i)
            calc_dict['title'].append(calc.title) #Required
            calc_dict['description'].append(calc.description or '')
            calc_dict['formula'].append(calc.getFormula() or '')

    return pd.DataFrame(calc_dict)[cols]

def get_analysis_profiles_as_df():
    """
    :return: Returns a DataFrame of active AnalysisProfiles
    :rtype: DataFrame
    """

    profiles = api.search({'portal_type':"AnalysisProfile"})
    cols = [
        'title',
        'description',
    ]

    profile_dict = {}
    for i in cols:
        profile_dict[i] = []

    for i in profiles:
        if api.get_workflow_status_of(i) not in ['inactive','invalid','cancelled','rejected','retracted','unassigned','dispatched']:
            profile = api.get_object(i)
            profile_dict['title'].append(profile.title) #Required
            profile_dict['description'].append(profile.description or '')

    return pd.DataFrame(profile_dict)[cols]

def get_samples_as_df():
    """
    :return: Returns a DataFrame of active Samples
    :rtype: DataFrame
    """

    samples = api.search({'portal_type':"AnalysisRequest"})
    cols = [
        'sid',
        'contacts',
        'client',
        'ccemails',
        'sdg',
        'clientsid',
        'labid',
        'datesampled',
        'timesampled',
        'sampletype',
        'location',
        'profile',
        'ol',
        'pair',
        'wst',
        'plant',
        'variety',
        'growth',
        'newold',
        'vigor'
    ]

    sample_dict = {}
    for i in cols:
        sample_dict[i] = []

    for i in samples:
        if api.get_workflow_status_of(i) not in ['inactive','invalid','cancelled','rejected','retracted','unassigned','dispatched']:
            sample = api.get_object(i)
            sample_dict['sid'].append(sample.getId())
            contacts = sample.getReferences('AnalysisRequestCCContact')
            if contacts:
                sample_dict['contacts'].append(','.join([c.Firstname + ' ' + c.Surname for c in contacts]) or '')
            else:
                sample_dict['contacts'].append('')
            sample_dict['client'].append(sample.getClient().ClientID or '')
            sample_dict['ccemails'].append(sample.CCEmails or '')
            batch = sample.getBatch()
            if batch:
                sample_dict['sdg'].append(batch.getId() or '')
            else:
                sample_dict['sdg'].append('')
            sample_dict['clientsid'].append(sample.ClientSampleID or '')
            sample_dict['labid'].append(sample.InternalLabID or '')
            sample_dict['datesampled'].append(sample.DateOfSampling.strftime('%m/%d/%Y') or '')
            sample_dict['timesampled'].append(sample.TimeOfSampling or '')
            type = sample.getSampleType()
            if type:
                sample_dict['sampletype'].append(type.title or '')
            else:
                sample_dict['sampletype'].append('')
            location = sample.getSamplePoint()
            if location:
                sample_dict['location'].append(location.getId() or '')
            else:
                sample_dict['location'].append('')
            sample_dict['profile'].append(','.join(map(api.get_title,sample.getProfiles())) or '')
            spec = sample.getSpecification()
            if spec:
                sample_dict['ol'].append(spec.title or '')
            else:
                sample_dict['ol'].append('')
            pair = sample.getSubGroup()
            if pair:
                sample_dict['pair'].append(pair.title or '')
            else:
                sample_dict['pair'].append('')
            if hasattr(sample,'WaterSourceType'):
                sample_dict['wst'].append(sample.WaterSourceType or '')
            else:
                sample_dict['wst'].append('')
            sample_dict['plant'].append(sample.PlantType or '')
            sample_dict['variety'].append(sample.Variety or '')
            sample_dict['growth'].append(sample.GrowthStage or '')
            sample_dict['newold'].append(sample.NewLeaf or '')
            if hasattr(sample,'Vigor'):
                sample_dict['vigor'].append(sample.Vigor or '')
            else:
                sample_dict['vigor'].append('')

    return pd.DataFrame(sample_dict)[cols]

def get_analyses_as_df():
    """
    :return: Returns a DataFrame of active Analyses
    :rtype: DataFrame
    """

    analyses = api.search({'portal_type':"Analyses"})
    cols = [
        'sid',
        'Keyword',
        'method',
        'instrument',
        'analyst',
        'result',
        'lod',
        'unit',
        'analysisdatetime',
        # 'inconclusive',
        # 'weight',
        # 'volume',
        # 'dilution',
        # ''
    ]

    analysis_dict = {}
    for i in cols:
        analysis_dict[i] = []

    for i in analyses:
        if api.get_workflow_status_of(i) not in ['inactive','invalid','cancelled','rejected','retracted','unassigned','dispatched']:
            analysis = api.get_object(i)
            analysis_dict['sid'].append(api.get_id(analysis.ac_parent)) #Required
            analysis_dict['Keyword'].append(analysis.Keyword or '')
            analysis_dict['method'].append(analysis.getMethod() or '')
            analysis_dict['instrument'].append(analysis.getInstrument() or '')
            analysis_dict['analyst'].append(analysis.getAnalyst() or '')
            analysis_dict['result'].append(analysis.Result or '')
            analysis_dict['lod'].append(analysis.LowerDetectionLimit or '')
            analysis_dict['unit'].append(analysis.Unit or '')
            analysis_dict['analysisdatetime'].append(analysis.AnalysisDateTime or '')

    return pd.DataFrame(analysis_dict)[cols]

def get_reports_as_df():
    """
    :return: Returns a DataFrame of active Reports
    :rtype: DataFrame
    """

    reports = api.search({'portal_type':"Report"})
    cols = [
        'title',
        'description',
    ]

    sample_dict = {}
    for i in cols:
        sample_dict[i] = []

    for i in samples:
        if api.get_workflow_status_of(i) not in ['inactive','invalid','cancelled','rejected','retracted','unassigned','dispatched']:
            sample = api.get_object(i)
            sample_dict['title'].append(sample.title) #Required
            sample_dict['description'].append(sample.description or '')

    return pd.DataFrame(sample_dict)[cols]
