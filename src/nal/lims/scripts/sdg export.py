rootpath = '/mnt'
path = '/Data/LIMS Sap CSV Exports/'
filepath = path + sdg.title + '.csv'
fullpath = rootpath + filepath
export_dict = {}
cols = [
    'Sample Number',
    'Received',
    'dSampled',
    'dResultsConfirmed',
    'dReportIssued',
    'dRecCompleted',
    'Grower',
    'Block',
    'Crop',
    'Specimen #',
    'Customer Code',
    'EC (W)',
    'Phosphorus (Sap-ICP)',
    'Calcium (Sap-ICP)',
    'Manganese (Sap-ICP)',
    'Zinc (Sap-ICP)',
    'Sulfur (Sap-ICP)',
    'Copper (Sap-ICP)',
    'Magnesium (Sap-ICP)',
    'Iron (Sap-ICP)',
    'Boron (Sap-ICP)',
    'Brix (Sap)',
    'pH (sap)',
    'Cl (sap)',
    'Sodium (Sap-ICP)',
    'Silicon (Sap-ICP)',
    'Aluminium (Sap-ICP)',
    'Cobalt (Sap-ICP)',
    'Molybdenum (Sap-ICP)',
    'NH4-N',
    'TN~',
    'Total Sugars',
    'N (sap)',
    'Nitrogen as Nitrate',
    'K/Ca Ratio',
    'Nitrogen Conversion Efficiency',
]

for i in range(len(cols)):
    export_dict[cols[i]] = []
for i in sdg.getAnalysisRequests():
    if api.get_workflow_status_of(i) not in ['cancelled','invalid'] and i.getSampleType().title == 'Sap':
        export_dict[cols[0]].append(i.id)
        received = sdg.SDGDate.strftime('%m-%d-%Y') + " " + sdg.SDGTime
        export_dict[cols[1]].append(received)
        sampled = i.DateOfSampling.strftime('%m-%d-%Y') + " " + i.TimeOfSampling
        export_dict[cols[2]].append(sampled)
        confirmed = i.getDateVerified()
        export_dict[cols[3]].append(confirmed)
        export_dict[cols[4]].append('')
        export_dict[cols[5]].append('')
        export_dict[cols[6]].append(i.getClient().Name)
        export_dict[cols[7]].append(i.getSamplePoint().title)
        export_dict[cols[8]].append(i.PlantType)
        export_dict[cols[9]].append(i.getClientSampleID())
        export_dict[cols[10]].append('')
        #EC
        ec = -0.01
        found = False
        for j in range(20, 0, -1):
            if found==False:
                version = 'sap_ec-'+str(j)
                if hasattr(i,version):
                    found = True
                    ec = float(i[version].Result)
        if found == False and hasattr(i,'sap_ec'):
            ec = float(i.sap_ec.Result)
        if ec <= 0.01:
            ec = -0.01
        export_dict[cols[11]].append(ec)
        #Phosphorus
        phosphorus = -0.01
        found = False
        for j in range(20, 0, -1):
            if found==False:
                version = 'sap_phosphorous-'+str(j)
                if hasattr(i,version):
                    found = True
                    phosphorus = float(i[version].Result)
        if found == False and hasattr(i,'sap_phosphorous'):
            phosphorus = float(i.sap_phosphorous.Result)
        if phosphorus <= 0.01:
            phosphorus = -0.01
        export_dict[cols[12]].append(phosphorus)
        #calcium
        calcium = -0.01
        found = False
        for j in range(20, 0, -1):
            if found==False:
                version = 'sap_calcium-'+str(j)
                if hasattr(i,version):
                    found = True
                    calcium = float(i[version].Result)
        if found == False and hasattr(i,'sap_calcium'):
            calcium = float(i.sap_calcium.Result)
        if calcium <= 0.01:
            calcium = -0.01
        export_dict[cols[13]].append(calcium)
        #manganese
        manganese = -0.01
        found = False
        for j in range(20, 0, -1):
            if found==False:
                version = 'sap_manganese-'+str(j)
                if hasattr(i,version):
                    found = True
                    manganese = float(i[version].Result)
        if found == False and hasattr(i,'sap_manganese'):
            manganese = float(i.sap_manganese.Result)
        if manganese <= 0.01:
            manganese = -0.01
        export_dict[cols[14]].append(manganese)
        #zinc
        zinc = -0.01
        found = False
        for j in range(20, 0, -1):
            if found==False:
                version = 'sap_zinc-'+str(j)
                if hasattr(i,version):
                    found = True
                    zinc = float(i[version].Result)
        if found == False and hasattr(i,'sap_zinc'):
            zinc = float(i.sap_zinc.Result)
        if zinc <= 0.01:
            zinc = -0.01
        export_dict[cols[15]].append(zinc)
        #sulfur
        sulfur = -0.01
        found = False
        for j in range(20, 0, -1):
            if found==False:
                version = 'sap_sulfur-'+str(j)
                if hasattr(i,version):
                    found = True
                    sulfur = float(i[version].Result)
        if found == False and hasattr(i,'sap_sulfur'):
            sulfur = float(i.sap_sulfur.Result)
        if sulfur <= 0.01:
            sulfur = -0.01
        export_dict[cols[16]].append(sulfur)
        #copper
        copper = -0.01
        found = False
        for j in range(20, 0, -1):
            if found==False:
                version = 'sap_copper-'+str(j)
                if hasattr(i,version):
                    found = True
                    copper = float(i[version].Result)
        if found == False and hasattr(i,'sap_copper'):
            copper = float(i.sap_copper.Result)
        if copper <= 0.01:
            copper = -0.01
        export_dict[cols[17]].append(copper)
        #magnesium
        magnesium = -0.01
        found = False
        for j in range(20, 0, -1):
            if found==False:
                version = 'sap_magnesium-'+str(j)
                if hasattr(i,version):
                    found = True
                    magnesium = float(i[version].Result)
        if found == False and hasattr(i,'sap_magnesium'):
            magnesium = float(i.sap_magnesium.Result)
        if magnesium <= 0.01:
            magnesium = -0.01
        export_dict[cols[18]].append(magnesium)
        #iron
        iron = -0.01
        found = False
        for j in range(20, 0, -1):
            if found==False:
                version = 'sap_iron-'+str(j)
                if hasattr(i,version):
                    found = True
                    iron = float(i[version].Result)
        if found == False and hasattr(i,'sap_iron'):
            iron = float(i.sap_iron.Result)
        if iron <= 0.01:
            iron = -0.01
        export_dict[cols[19]].append(iron)
        #boron
        boron = -0.01
        found = False
        for j in range(20, 0, -1):
            if found==False:
                version = 'sap_boron-'+str(j)
                if hasattr(i,version):
                    found = True
                    boron = float(i[version].Result)
        if found == False and hasattr(i,'sap_boron'):
            boron = float(i.sap_boron.Result)
        if boron <= 0.01:
            boron = -0.01
        export_dict[cols[20]].append(boron)
        #brix
        brix = -0.01
        found = False
        for j in range(20, 0, -1):
            if found==False:
                version = 'sap_brix-'+str(j)
                if hasattr(i,version):
                    found = True
                    brix = float(i[version].Result)
        if found == False and hasattr(i,'sap_brix'):
            brix = float(i.sap_brix.Result)
        if brix <= 0.01:
            brix = -0.01
        export_dict[cols[21]].append(brix)
        #ph
        ph = -0.01
        found = False
        for j in range(20, 0, -1):
            if found==False:
                version = 'sap_ph-'+str(j)
                if hasattr(i,version):
                    found = True
                    ph = float(i[version].Result)
        if found == False and hasattr(i,'sap_ph'):
            ph = float(i.sap_ph.Result)
        if ph <= 0.01:
            ph = -0.01
        export_dict[cols[22]].append(ph)
        #chloride
        chloride = -0.01
        found = False
        for j in range(20, 0, -1):
            if found==False:
                version = 'sap_chloride-'+str(j)
                if hasattr(i,version):
                    found = True
                    manganese = float(i[version].Result)
        if found == False and hasattr(i,'sap_chloride'):
            chloride = float(i.sap_chloride.Result)
        if chloride <= 0.01:
            chloride = -0.01
        export_dict[cols[23]].append(chloride)
        #sodium
        sodium = -0.01
        found = False
        for j in range(20, 0, -1):
            if found==False:
                version = 'sap_sodium-'+str(j)
                if hasattr(i,version):
                    found = True
                    sodium = float(i[version].Result)
        if found == False and hasattr(i,'sap_sodium'):
            sodium = float(i.sap_sodium.Result)
        if sodium <= 0.01:
            sodium = -0.01
        export_dict[cols[24]].append(sodium)
        #silicon
        silicon = -0.01
        found = False
        for j in range(20, 0, -1):
            if found==False:
                version = 'sap_silicon-'+str(j)
                if hasattr(i,version):
                    found = True
                    silicon = float(i[version].Result)
        if found == False and hasattr(i,'sap_silicon'):
            silicon = float(i.sap_silicon.Result)
        if silicon <= 0.01:
            silicon = -0.01
        export_dict[cols[25]].append(silicon)
        #aluminium
        aluminium = -0.01
        found = False
        for j in range(20, 0, -1):
            if found==False:
                version = 'sap_aluminum-'+str(j)
                if hasattr(i,version):
                    found = True
                    aluminium = float(i[version].Result)
        if found == False and hasattr(i,'sap_aluminum'):
            aluminium = float(i.sap_aluminum.Result)
        if aluminium <= 0.01:
            aluminium = -0.01
        export_dict[cols[26]].append(aluminium)
        #cobalt
        cobalt = -0.01
        found = False
        for j in range(20, 0, -1):
            if found==False:
                version = 'sap_cobalt-'+str(j)
                if hasattr(i,version):
                    found = True
                    cobalt = float(i[version].Result)
        if found == False and hasattr(i,'sap_cobalt'):
            cobalt = float(i.sap_cobalt.Result)
        if cobalt <= 0.01:
            cobalt = -0.01
        export_dict[cols[27]].append(cobalt)
        #molybdenum
        molybdenum = -0.01
        found = False
        for j in range(20, 0, -1):
            if found==False:
                version = 'sap_molybdenum-'+str(j)
                if hasattr(i,version):
                    found = True
                    molybdenum = float(i[version].Result)
        if found == False and hasattr(i,'sap_molybdenum'):
            molybdenum = float(i.sap_molybdenum.Result)
        if molybdenum <= 0.01:
            molybdenum = -0.01
        export_dict[cols[28]].append(molybdenum)
        #Nitrogen from Ammonium
        n_nh4 = -0.01
        found = False
        for j in range(20, 0, -1):
            if found==False:
                version = 'sap_nitrogen_as_ammonium-'+str(j)
                if hasattr(i,version):
                    found = True
                    n_nh4 = float(i[version].Result)
        if found == False and hasattr(i,'sap_nitrogen_as_ammonium'):
            n_nh4 = float(i.sap_nitrogen_as_ammonium.Result)
        if n_nh4 <= 0.01:
            n_nh4 = -0.01
        export_dict[cols[29]].append(n_nh4)
        #Total Nitrogen
        tn = -0.01
        found = False
        for j in range(20, 0, -1):
            if found==False:
                version = 'sap_total_nitrogen-'+str(j)
                if hasattr(i,version):
                    found = True
                    tn = float(i[version].Result)
        if found == False and hasattr(i,'sap_total_nitrogen'):
            tn = float(i.sap_total_nitrogen.Result)
        if tn <= 0.01:
            tn = -0.01
        export_dict[cols[30]].append(tn)
        #Total Sugars
        ts = -0.01
        found = False
        for j in range(20, 0, -1):
            if found==False:
                version = 'sap_total_sugar-'+str(j)
                if hasattr(i,version):
                    found = True
                    ts = float(i[version].Result)
        if found == False and hasattr(i,'sap_total_sugar'):
            ts = float(i.sap_total_sugar.Result)
        if ts <= 0.01:
            ts = -0.01
        export_dict[cols[31]].append(ts)
        #nitrate
        # manganese = -0.01
        # found = False
        # for j in range(20, 0, -1):
        #     if found==False:
        #         version = 'sap_manganese-'+str(j)
        #         if hasattr(i,version):
        #             found = True
        #             manganese = float(i[version].Result)
        # if found == False and hasattr(i,'sap_manganese'):
        #     manganese = float(i.sap_manganese.Result)
        #
        # if manganese <= 0.01:
        #     manganese = -0.01
        export_dict[cols[32]].append('')
        #nitrogen as nitrate
        n_no3 = -0.01
        found = False
        for j in range(20, 0, -1):
            if found==False:
                version = 'sap_nitrogen_as_nitrate-'+str(j)
                if hasattr(i,version):
                    found = True
                    n_no3 = float(i[version].Result)
        if found == False and hasattr(i,'sap_nitrogen_as_nitrate'):
            n_no3 = float(i.sap_nitrogen_as_nitrate.Result)
        if n_no3 <= 0.01:
            n_no3 = -0.01
        export_dict[cols[33]].append(n_no3)
        #k/ca ratio
        kca = -0.01
        found = False
        for j in range(20, 0, -1):
            if found==False:
                version = 'sap_kcaratio-'+str(j)
                if hasattr(i,version):
                    found = True
                    kca = float(i[version].Result)
        if found == False and hasattr(i,'sap_kcaratio'):
            kca = float(i.sap_kcaratio.Result)
        if kca <= 0.01:
            kca = -0.01
        export_dict[cols[34]].append(kca)
        #Nitrogen conversion efficiency
        nce = ''
        if tn < 0.01:
            nce = ''
        else:
            if n_nh4 < 0.01:
                n_nh4 = 0
            if n_no3 < 0.01:
                n_no3 = 0
            nce = (1 - ((n_nh4 + n_no3) / tn))*100
        export_dict[cols[35]].append(nce)


df = pd.DataFrame()
for i in range(len(cols)):
    df[cols[i]] = export_dict[cols[i]]

df.to_csv(fullpath)
# IStatusMessage(i.request).addStatusMessage(
#         u"{} Successfully Exported to: {}".format(i.context.title, filepath)
#     )
# i.request.response.redirect(api.get_url(i.context))
