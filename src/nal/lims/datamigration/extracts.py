
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

    #SDG
    file = '{}/sdgs_{}.csv'.format(dir,now)
    get_sdgs_as_df().to_csv(file,encoding='utf-8')
    print("-Extracted SDG Data to "+file)

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
        if api.get_workflow_status_of(i) in ['open','closed']:
            sdg = api.get_object(i)
            sdg_dict['title'].append(sdg.title) #Required
            sdg_dict['description'].append(sdg.description or '')
            sdg_dict['BatchID'].append(sdg.id or '')
            sdg_dict['Client'].append(sdg.aq_parent.ClientID or '')
            sdg_dict['ClientBatchID'].append(sdg.ClientBatchID or '')
            sdg_dict['BatchLabels'].append(sdg.getLabelNames() or '')
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
                instrument_dict['methods'].append([m.title for m in map(api.get_object,methods)])
            else:
                instrument_dict['methods'].append(set(['']))

    return pd.DataFrame(instrument_dict)[cols]

def get_samplelocations_as_df():
    """
    :return: Returns a DataFrame of active Sample Locations
    :rtype: DataFrame
    """

    locations = api.search({'portal_type':"SamplePoint"})
    cols = [
        'title',
        'description',
        'formatted address',
        'water source type',
        'wssn'
    ]

    location_dict = {}
    for i in cols:
        location_dict[i] = []

    for i in instruments:
        if api.get_workflow_status_of(i) == 'active':
            instrument = api.get_object(i)
            location_dict['title'].append(instrument.title) #Required
            location_dict['description'].append(instrument.description or '')
            location_dict['formatted address'].append(instrument.FormattedAddress or '')
            location_dict['water source type'].append(instrument.WaterSourceType or '')
            location_dict['wssn'].append(instrument.WSSN or '')

    return pd.DataFrame(location_dict)[cols]

def get_XXX_as_df():
    """
    :return: Returns a DataFrame of active XXX
    :rtype: DataFrame
    """

    instruments = api.search({'portal_type':"XXX"})
    cols = [
        'title',
        'description',
    ]

    xxx_dict = {}
    for i in cols:
        xxx_dict[i] = []

    for i in instruments:
        if api.get_workflow_status_of(i) == 'active':
            instrument = api.get_object(i)
            xxx_dict['title'].append(instrument.title) #Required
            xxx_dict['description'].append(instrument.description or '')

    return pd.DataFrame(xxx_dict)[cols]

def get_XXX_as_df():
    """
    :return: Returns a DataFrame of active XXX
    :rtype: DataFrame
    """

    instruments = api.search({'portal_type':"XXX"})
    cols = [
        'title',
        'description',
    ]

    xxx_dict = {}
    for i in cols:
        xxx_dict[i] = []

    for i in instruments:
        if api.get_workflow_status_of(i) == 'active':
            instrument = api.get_object(i)
            xxx_dict['title'].append(instrument.title) #Required
            xxx_dict['description'].append(instrument.description or '')

    return pd.DataFrame(xxx_dict)[cols]

def get_XXX_as_df():
    """
    :return: Returns a DataFrame of active XXX
    :rtype: DataFrame
    """

    instruments = api.search({'portal_type':"XXX"})
    cols = [
        'title',
        'description',
    ]

    xxx_dict = {}
    for i in cols:
        xxx_dict[i] = []

    for i in instruments:
        if api.get_workflow_status_of(i) == 'active':
            instrument = api.get_object(i)
            xxx_dict['title'].append(instrument.title) #Required
            xxx_dict['description'].append(instrument.description or '')

    return pd.DataFrame(xxx_dict)[cols]

def get_XXX_as_df():
    """
    :return: Returns a DataFrame of active XXX
    :rtype: DataFrame
    """

    instruments = api.search({'portal_type':"XXX"})
    cols = [
        'title',
        'description',
    ]

    xxx_dict = {}
    for i in cols:
        xxx_dict[i] = []

    for i in instruments:
        if api.get_workflow_status_of(i) == 'active':
            instrument = api.get_object(i)
            xxx_dict['title'].append(instrument.title) #Required
            xxx_dict['description'].append(instrument.description or '')

    return pd.DataFrame(xxx_dict)[cols]

def get_XXX_as_df():
    """
    :return: Returns a DataFrame of active XXX
    :rtype: DataFrame
    """

    instruments = api.search({'portal_type':"XXX"})
    cols = [
        'title',
        'description',
    ]

    xxx_dict = {}
    for i in cols:
        xxx_dict[i] = []

    for i in instruments:
        if api.get_workflow_status_of(i) == 'active':
            instrument = api.get_object(i)
            xxx_dict['title'].append(instrument.title) #Required
            xxx_dict['description'].append(instrument.description or '')

    return pd.DataFrame(xxx_dict)[cols]
