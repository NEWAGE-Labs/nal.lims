#Login
from AccessControl import getSecurityManager
from AccessControl.User import UnrestrictedUser
from AccessControl.SecurityManagement import newSecurityManager
from bika.lims import api
portal = api.get_portal()
me = UnrestrictedUser(getSecurityManager().getUser().getUserName(), '', ['LabManager'], '')
me = me.__of__(portal.acl_users)
newSecurityManager(None, me)

#Portal Types
clients = portal.clients
labcontacts = portal.bika_setup.bika_labcontacts
departments = portal.bika_setup.bika_departments
categories = portal.bika_setup.bika_analysiscategories
methods = portal.methods
instruments = portal.bika_setup.bika_instruments
instrumenttypes = portal.bika_setup.bika_instrumenttypes
calculations = portal.bika_setup.bika_calculations
profiles = portal.bika_setup.bika_analysisprofiles
specs = portal.bika_setup.bika_analysisspecs
sampletypes = portal.bika_setup.bika_sampletypes
subgroups = portal.bika_setup.bika_subgroups
labels = portal.bika_setup.bika_batchlabels
samplepoints = portal.bika_setup.bika_samplepoints
analysisservices = portal.bika_setup.bika_analysisservices


#LabContacts
paul = api.create(labcontacts, "LabContact", Firstname="Paul", Surname="VanderWeele", EmailAddress="pvanderweele@newagelaboratories.com").UID()
brian = api.create(labcontacts, "LabContact", Firstname="Brian", Surname="Kreiger", EmailAddress="bkrieger@newagelaboratories.com").UID()
scott = api.create(labcontacts, "LabContact", Firstname="Scott", Surname="Wall", EmailAddress="swall@newagelaboratories.com").UID()
melissa = api.create(labcontacts, "LabContact", Firstname="Melissa", Surname="Abshire", EmailAddress="mabshire@newagelaboratories.com").UID()
kim = api.create(labcontacts, "LabContact", Firstname="Kim", Surname="Crago", EmailAddress="kcrago@newagelaboratories.com").UID()
irish = api.create(labcontacts, "LabContact", Firstname="Irish", Surname="Gallagher", EmailAddress="igallagher@newagelaboratories.com").UID()
tami = api.create(labcontacts, "LabContact", Firstname="Tami", Surname="Kruger", EmailAddress="tkruger@newagelaboratories.com").UID()
sarah = api.create(labcontacts, "LabContact", Firstname="Sarah", Surname="Powell", EmailAddress="spowell@newagelaboratories.com").UID()
chelsey = api.create(labcontacts, "LabContact", Firstname="Chelsey", Surname="Lynch", EmailAddress="clynch@newagelaboratories.com").UID()
# taylor = api.create(labcontacts, "LabContact", Firstname="Taylor", Surname="Opolka", EmailAddress="topolka@newagelaboratories.com").UID()

for i in api.search({'portal_type':'LabContact'}):
    api.get_object(i).reindexObject()

#Department
newage = api.create(departments, "Department", title="NEW AGE Lab", DepartmentID="newage", Manager=scott).UID()

for i in api.search({'portal_type':'Department'}):
    api.get_object(i).reindexObject()

#AnalysisCategories

sapcategory = api.create(categories, "AnalysisCategory", title="Sap").UID()
drinkingcategory = api.create(categories, "AnalysisCategory", title="Water, Drinking").UID()
surfacecategory = api.create(categories, "AnalysisCategory", title="Water, Surface").UID()
surfacecategory = api.create(categories, "AnalysisCategory", title="Water, Waste").UID()
cannabiscategory = api.create(categories, "AnalysisCategory", title="Cannabis Flower").UID()
soilcategory = api.create(categories, "AnalysisCategory", title="Soil").UID()
liqfertcategory = api.create(categories, "AnalysisCategory", title="Water, Liquid Fertilizer").UID()
frozencategory = api.create(categories, "AnalysisCategory", title="Food, Frozen").UID()
rawcategory = api.create(categories, "AnalysisCategory", title="Food, Raw").UID()
aircategory = api.create(categories, "AnalysisCategory", title="Compressed Air").UID()
prepcategory = api.create(categories, "AnalysisCategory", title="Prep").UID()
cleancategory = api.create(categories, "AnalysisCategory", title="Cleanup").UID()

for i in api.search({'portal_type':'AnalysisCategory'}):
    api.get_object(i).reindexObject()

#Methods

aoac974_21 = api.create(methods, "Method", title="AOAC 974.21", description="PCB").UID()
aoac983_21 = api.create(methods, "Method", title="AOAC 983.21", description="Pesticide").UID()
aoac984_21 = api.create(methods, "Method", title="AOAC 984.21", description="Pesticide").UID()
aoac990_06 = api.create(methods, "Method", title="AOAC 990.06", description="Pesticide").UID()
aoac2004_01 = api.create(methods, "Method", title="AOAC 2004.01 QuEChERS", description="Pesticide Food Residue").UID()
aoac2007_01 = api.create(methods, "Method", title="AOAC 2007.01", description="VOC/SVOC/Pest").UID()
epa3510a = api.create(methods, "Method", title="EPA 3510A", description="Funnel Liq-Liq").UID()
epa3535a = api.create(methods, "Method", title="EPA 3535A", description="SPE").UID()
epa3546 = api.create(methods, "Method", title="EPA 3546", description="Soluable Organic Compounds").UID()
epa3541 = api.create(methods, "Method", title="EPA 3541", description="DRO").UID()
epa3550 = api.create(methods, "Method", title="EPA 3550", description="Ultrasonic (Soil)").UID()
epa3620b = api.create(methods, "Method", title="EPA 3620B", description="Sulfur-Cleanup").UID()
epa3660b = api.create(methods, "Method", title="EPA 3660B", description="Sulfur-Cleanup").UID()
epa3665a = api.create(methods, "Method", title="EPA 3665A", description="Sulfur/Permanganate").UID()
epa5030c = api.create(methods, "Method", title="EPA 5030C", description="P+T VOC").UID()
epa5035a = api.create(methods, "Method", title="EPA 5035A", description="Soil").UID()
epa8081b = api.create(methods, "Method", title="EPA 8081B", description="Pesticide").UID()
epa8082a = api.create(methods, "Method", title="EPA 8082A", description="PCB").UID()
epa8260 = api.create(methods, "Method", title="EPA 8260B, C, D", description="VOC").UID()
epa8270 = api.create(methods, "Method", title="EPA 8270 D,E", description="SVOC").UID()
aoac932_14 = api.create(methods, "Method", title="AOAC 932.14", description="Brix").UID()
aoac973_41 = api.create(methods, "Method", title="AOAC 973.41", description="pH").UID()
aoac978_18 = api.create(methods, "Method", title="AOAC 978.18", description="Water Activity").UID()
aoac994_16 = api.create(methods, "Method", title="AOAC 994.16", description="Soil pH").UID()
sm1664a = api.create(methods, "Method", title="SM1664A", description="Oil/Grease").UID()
sm2320b = api.create(methods, "Method", title="SM2320B", description="Phenolphthalein/Alkalinity").UID()
sm2340a = api.create(methods, "Method", title="SM2340A", description="Hardness").UID()
sm2510b = api.create(methods, "Method", title="SM2510B", description="Conductivity").UID()
sm2540c = api.create(methods, "Method", title="SM2540C", description="TDS/Soluable Salts").UID()
sm2540d = api.create(methods, "Method", title="SM2540D", description="TSS").UID()
sm4500_modnh3 = api.create(methods, "Method", title="MOD.SM4500-NH3 G-2011", description="Ammonia (NH4)").UID()
sm4500_nh3 = api.create(methods, "Method", title="SM4500 NH3-D", description="NH3D Ammonia").UID()
sm4500_no3d = api.create(methods, "Method", title="SM4500 NO-3D", description="Nitrate").UID()
sm4500_no2b = api.create(methods, "Method", title="SM4500 NO-2B", description="Nitrite").UID()
sm4500_cl = api.create(methods, "Method", title="SM4500 Cl-", description="Chloride").UID()
sm4500_hb = api.create(methods, "Method", title="SM4500-H+B", description="pH").UID()
sm5210b = api.create(methods, "Method", title="SM5210B", description="BOD").UID()
sm5220d = api.create(methods, "Method", title="SM5220D", description="COD").UID()
astmd93 = api.create(methods, "Method", title="ASTM D93", description="Flash Point").UID()
gallery = api.create(methods, "Method", title="GALLERY", description="Entire Gallery+Platform").UID()
hach8043 = api.create(methods, "Method", title="HACH 8043", description="BOD").UID()
hach8113 = api.create(methods, "Method", title="HACH 8113", description="Chlorine").UID()
hach10208 = api.create(methods, "Method", title="HACH 10208", description="Total Nitrogen").UID()
iso19822 = api.create(methods, "Method", title="ISO 19822:20181E", description="HA-FA").UID()
aoac971_21 = api.create(methods, "Method", title="AOAC 971.21", description="Hg").UID()
aoac990_08 = api.create(methods, "Method", title="AOAC 990.08", description="ICP").UID()
aoac993_14 = api.create(methods, "Method", title="AOAC 993.14", description="ICP").UID()
aoac2012_007 = api.create(methods, "Method", title="AOAC 2012.007", description="ICP (Food)").UID()
epa3010a = api.create(methods, "Method", title="EPA 3010A", description="Liquids").UID()
epa3050b = api.create(methods, "Method", title="EPA 3050B", description="Soil").UID()
epa6010c = api.create(methods, "Method", title="EPA 6010C", description="Metals").UID()
epa200_5 = api.create(methods, "Method", title="EPA 200.5", description="ICP Pb/Cu").UID()
epa7470 = api.create(methods, "Method", title="EPA 7470", description="Hg-Water").UID()
epa7471b = api.create(methods, "Method", title="EPA 7471B", description="Hg-Soil").UID()
sp3050 = api.create(methods, "Method", title="SP-3050 (Metals)", description="Soil").UID()
sp3010 = api.create(methods, "Method", title="SP-3010 (Metals)", description="Liquids").UID()
aoac990_12 = api.create(methods, "Method", title="AOAC 990.12", description="APC").UID()
aoac991_14 = api.create(methods, "Method", title="AOAC 991.14", description="E. coli Food P/A").UID()
aoac997_02 = api.create(methods, "Method", title="AOAC 997.02", description="Yeast/Mold").UID()
aoac2003_01 = api.create(methods, "Method", title="AOAC 2003.01", description="EB").UID()
aoac2003_07 = api.create(methods, "Method", title="AOAC 2003.07", description="Staph.").UID()
aoac2013_09 = api.create(methods, "Method", title="AOAC 2013.09", description="Salm. For Food").UID()
aoac2014_01 = api.create(methods, "Method", title="AOAC 2014.01", description="Salm Spp. P/A").UID()
aoac2014_06 = api.create(methods, "Method", title="AOAC 2014.06", description="Listeria Spp.").UID()
aoac2014_07 = api.create(methods, "Method", title="AOAC 2014.07", description="Listeria Mono.").UID()
aoac2017_01 = api.create(methods, "Method", title="AOAC 2017.01", description="E. coli 0157").UID()
aoac041701 = api.create(methods, "Method", title="AOAC #041701", description="Lactic Acid").UID()
aoac041101 = api.create(methods, "Method", title="AOAC #041101", description="Listeria 25g").UID()
aoac960801 = api.create(methods, "Method", title="AOAC #960801", description="Salm 25g").UID()
colilert_18pa = api.create(methods, "Method", title="Colilert-18 P/A (SM9223B)", description="P/A").UID()
colilert_18qt = api.create(methods, "Method", title="Colilert-18 QT-2000 (SM9223B)", description="").UID()
sm9223b = api.create(methods, "Method", title="SM9223B", description="MPN").UID()
aoac972_32 = api.create(methods, "Method", title="AOAC 972.43", description="Total Nitrogen").UID()
aoac985_09 = api.create(methods, "Method", title="AOAC 985.09", description="Total Sugar").UID()


for i in api.search({'portal_type':'Method'}):
    api.get_object(i).reindexObject()


#InstrumentTypes

pcr3m = api.create(instrumenttypes, "InstrumentType", title="3M PCR").UID()
autoclave = api.create(instrumenttypes, "InstrumentType", title="Autoclave").UID()
balance = api.create(instrumenttypes, "InstrumentType", title="Balance").UID()
centri = api.create(instrumenttypes, "InstrumentType", title="Centrifuge").UID()
coldpress = api.create(instrumenttypes, "InstrumentType", title="Cold Press").UID()
cvaa = api.create(instrumenttypes, "InstrumentType", title="CVAA (Flameless)").UID()
electro = api.create(instrumenttypes, "InstrumentType", title="Electrometer").UID()
gallery = api.create(instrumenttypes, "InstrumentType", title="Gallery").UID()
gcecd = api.create(instrumenttypes, "InstrumentType", title="GC-ECD").UID()
gcfid = api.create(instrumenttypes, "InstrumentType", title="GC-FID").UID()
gcms = api.create(instrumenttypes, "InstrumentType", title="GC-MS").UID()
icpoes = api.create(instrumenttypes, "InstrumentType", title="ICP-OES").UID()
incub = api.create(instrumenttypes, "InstrumentType", title="Incubator").UID()
leco = api.create(instrumenttypes, "InstrumentType", title="LECO").UID()
mercury = api.create(instrumenttypes, "InstrumentType", title="Mercury Analyzer").UID()
hood = api.create(instrumenttypes, "InstrumentType", title="Outtake Hood").UID()
oven = api.create(instrumenttypes, "InstrumentType", title="Ovens and Environmental Chambers").UID()
pipette = api.create(instrumenttypes, "InstrumentType", title="Pipette").UID()
thermometer = api.create(instrumenttypes, "InstrumentType", title="Thermometer").UID()
weights = api.create(instrumenttypes, "InstrumentType", title="Weights").UID()

for i in api.search({'portal_type':'InstrumentType'}):
    api.get_object(i).reindexObject()

#AnalysisService

##Sap
sap_al = api.create(analysisservices, "AnalysisService", title="Aluminum (Al)", Keyword = "sap_aluminum", Methods=[aoac993_14], Accredited=True, Unit="ppm" ,PointOfCapture="lab", Category=sapcategory, LowerDetectionLimit="0.05", Precision=2, ExponentialFormatPrecision=7).UID()
sap_b = api.create(analysisservices, "AnalysisService", title="Boron (B)", Keyword = "sap_boron", Methods=[aoac993_14], Accredited=True, Unit="ppm", PointOfCapture="lab", Category=sapcategory, LowerDetectionLimit="0.05", Precision=2, ExponentialFormatPrecision=7).UID()
sap_brix = api.create(analysisservices, "AnalysisService", title="Brix", Keyword = "sap_brix", Methods=aoac932_14, Accredited=True, Unit="-", PointOfCapture="lab", Category=sapcategory, LowerDetectionLimit="0.01", Precision=3, ExponentialFormatPrecision=7).UID()
sap_sugar = api.create(analysisservices, "AnalysisService", title="Sugars, Total", Keyword = "sap_total_sugar", Methods=aoac985_09, Accredited=True, Unit="%", PointOfCapture="lab", Category=sapcategory, Precision=1, ExponentialFormatPrecision=7).UID()
sap_ca = api.create(analysisservices, "AnalysisService", title="Calcium (Ca)", Keyword = "sap_calcium", Methods=[aoac993_14], Accredited=True, Unit="ppm", PointOfCapture="lab", Category=sapcategory, LowerDetectionLimit="0.05", Precision=2, ExponentialFormatPrecision=7).UID()
sap_cl = api.create(analysisservices, "AnalysisService", title="Chloride (Cl-)", Keyword = "sap_chloride", Methods=sm4500_cl, Accredited=True, Unit="ppm", PointOfCapture="lab", Category=sapcategory, LowerDetectionLimit="0.05", Precision=2, ExponentialFormatPrecision=7).UID()
sap_co = api.create(analysisservices, "AnalysisService", title="Cobalt (Co)", Keyword = "sap_cobalt", Methods=[aoac993_14], Accredited=True, Unit="ppm", PointOfCapture="lab", Category=sapcategory, LowerDetectionLimit="0.05", Precision=2, ExponentialFormatPrecision=7).UID()
sap_cu = api.create(analysisservices, "AnalysisService", title="Copper (Cu)", Keyword = "sap_copper", Methods=[aoac993_14], Accredited=True, Unit="ppm", PointOfCapture="lab", Category=sapcategory, LowerDetectionLimit="0.05", Precision=2, ExponentialFormatPrecision=7).UID()
sap_ec = api.create(analysisservices, "AnalysisService", title="EC", Keyword = "sap_ec", Methods=sm2510b, Accredited=True, Unit="mS/cm", PointOfCapture="lab", Category=sapcategory, LowerDetectionLimit="0.001", Precision=3, ExponentialFormatPrecision=7).UID()
sap_fe = api.create(analysisservices, "AnalysisService", title="Iron (Fe)", Keyword = "sap_iron", Methods=[aoac993_14], Accredited=True, Unit="ppm", PointOfCapture="lab", Category=sapcategory, LowerDetectionLimit="0.05", Precision=2, ExponentialFormatPrecision=7).UID()
sap_kca = api.create(analysisservices, "AnalysisService", title="K/Ca Ratio", Keyword = "sap_kcaratio", Accredited=True, Unit="-", PointOfCapture="lab", Category=sapcategory, LowerDetectionLimit="0.0001", Precision=4, ExponentialFormatPrecision=7).UID()
sap_mg = api.create(analysisservices, "AnalysisService", title="Magnesium (Mg)", Keyword = "sap_magnesium", Methods=[aoac993_14], Accredited=True, Unit="ppm", PointOfCapture="lab", Category=sapcategory, LowerDetectionLimit="0.05", Precision=2, ExponentialFormatPrecision=7).UID()
sap_mn = api.create(analysisservices, "AnalysisService", title="Manganese (Mn)", Keyword = "sap_manganese", Methods=[aoac993_14], Accredited=True, Unit="ppm", PointOfCapture="lab", Category=sapcategory, LowerDetectionLimit="0.05", Precision=2, ExponentialFormatPrecision=7).UID()
sap_mo = api.create(analysisservices, "AnalysisService", title="Molybdenum (Mo)", Keyword = "sap_molybdenum", Methods=[aoac993_14], Accredited=True, Unit="ppm", PointOfCapture="lab", Category=sapcategory, LowerDetectionLimit="0.05", Precision=2, ExponentialFormatPrecision=7).UID()
sap_ni = api.create(analysisservices, "AnalysisService", title="Nickel (Ni)", Keyword = "sap_nickel", Methods=[aoac993_14], Accredited=True, Unit="ppm", PointOfCapture="lab", Category=sapcategory, LowerDetectionLimit="0.05", Precision=2, ExponentialFormatPrecision=7).UID()
sap_ncr = api.create(analysisservices, "AnalysisService", title="Nitrogen Conversion Effeciency", Keyword = "sap_nitratogen_conversion_ratio", Accredited=True, Unit="%", PointOfCapture="lab", Category=sapcategory, LowerDetectionLimit="0.001", Precision=3, ExponentialFormatPrecision=7).UID()
sap_no3 = api.create(analysisservices, "AnalysisService", title="Nitrate (NO3)", Keyword = "sap_nitrate", Accredited=True, Unit="ppm", PointOfCapture="lab", Category=sapcategory, LowerDetectionLimit="0.001", Precision=3, ExponentialFormatPrecision=7).UID()
sap_nnh4 = api.create(analysisservices, "AnalysisService", title="Nitrogen as Ammonium (NH4)", Keyword = "sap_nitrogen_as_ammonium", Methods=sm4500_nh3, Accredited=True, Unit="ppm", PointOfCapture="lab", Category=sapcategory, LowerDetectionLimit="0.05", Precision=2, ExponentialFormatPrecision=7).UID()
sap_nno3 = api.create(analysisservices, "AnalysisService", title="Nitrogen as Nitrate (NO3)", Keyword = "sap_nitrogen_as_nitrate", Methods=sm4500_no3d, Accredited=True, Unit="ppm", PointOfCapture="lab", LowerDetectionLimit="0.05", Precision=2, Category=sapcategory, ExponentialFormatPrecision=7).UID()
sap_totaln = api.create(analysisservices, "AnalysisService", title="Nitrogen (N), Total", Keyword = "sap_total_nitrogen", Methods=aoac972_32, Accredited=True, Unit="ppm", PointOfCapture="lab", LowerDetectionLimit="0.05", Precision=2, Category=sapcategory, ExponentialFormatPrecision=7).UID()
sap_ph = api.create(analysisservices, "AnalysisService", title="pH", Keyword = "sap_ph", Methods=aoac973_41, Accredited=True, Unit="-", PointOfCapture="lab", Category=sapcategory, LowerDetectionLimit="0.01", Precision=2, ExponentialFormatPrecision=7).UID()
sap_p = api.create(analysisservices, "AnalysisService", title="Phosphorous (P)", Keyword = "sap_phosphorous", Methods=[aoac993_14], Accredited=True, Unit="ppm", PointOfCapture="lab", Category=sapcategory, LowerDetectionLimit="0.05", Precision=2, ExponentialFormatPrecision=7).UID()
sap_k = api.create(analysisservices, "AnalysisService", title="Potassium (K)", Keyword = "sap_potassium", Methods=[aoac993_14], Accredited=True, Unit="ppm", PointOfCapture="lab", Category=sapcategory, LowerDetectionLimit="0.05", Precision=2, ExponentialFormatPrecision=7).UID()
sap_se = api.create(analysisservices, "AnalysisService", title="Selenium (Se)", Keyword = "sap_selenium", Methods=[aoac993_14], Accredited=True, Unit="ppm", PointOfCapture="lab", Category=sapcategory, LowerDetectionLimit="0.05", Precision=2, ExponentialFormatPrecision=7).UID()
sap_si = api.create(analysisservices, "AnalysisService", title="Silica (Si)", Keyword = "sap_silica", Methods=[aoac993_14], Accredited=True, Unit="ppm", PointOfCapture="lab", Category=sapcategory, LowerDetectionLimit="0.05", Precision=2, ExponentialFormatPrecision=7).UID()
sap_na = api.create(analysisservices, "AnalysisService", title="Sodium (Na)", Keyword = "sap_sodium", Methods=[aoac993_14], Accredited=True, Unit="ppm", PointOfCapture="lab", Category=sapcategory, LowerDetectionLimit="0.05", Precision=2, ExponentialFormatPrecision=7).UID()
sap_s = api.create(analysisservices, "AnalysisService", title="Sulfur (S)", Keyword = "sap_sulfur", Methods=[aoac993_14], Accredited=True, Unit="ppm", PointOfCapture="lab", Category=sapcategory, LowerDetectionLimit="0.05", Precision=2, ExponentialFormatPrecision=7).UID()
sap_zn = api.create(analysisservices, "AnalysisService", title="Zinc (Zn)", Keyword = "sap_zinc", Methods=[aoac993_14], Accredited=True, Unit="ppm", PointOfCapture="lab", Category=sapcategory, LowerDetectionLimit="0.05", Precision=2, ExponentialFormatPrecision=7).UID()

##Drinking Water

drinking_f = api.create(analysisservices, "AnalysisService", title="Flouride (F)", Keyword = "drinking_flouride", Accredited=True, Unit="mg/L", PointOfCapture="lab", Category=drinkingcategory, LowerDetectionLimit="0.01", Precision=2, ExponentialFormatPrecision=7).UID()
drinking_pb = api.create(analysisservices, "AnalysisService", title="Lead (Pb)", Keyword = "drinking_lead", Methods=epa200_5, Accredited=True, Unit="µg/L", PointOfCapture="lab", Category=drinkingcategory, LowerDetectionLimit="5.0", Precision=1, ExponentialFormatPrecision=7).UID()
drinking_cu = api.create(analysisservices, "AnalysisService", title="Copper (Cu)", Keyword = "drinking_copper", Methods=epa200_5, Accredited=True, Unit="µg/L", PointOfCapture="lab", Category=drinkingcategory, LowerDetectionLimit="5.0", Precision=1, ExponentialFormatPrecision=7).UID()
drinking_no2 = api.create(analysisservices, "AnalysisService", title="Nitrite (NO2)", Keyword = "drinking_nitrite", Methods=sm4500_no2b, Accredited=False, Unit="mg/L", PointOfCapture="lab", Category=drinkingcategory, LowerDetectionLimit="0.1", Precision=2, ExponentialFormatPrecision=7).UID()
drinking_no3 = api.create(analysisservices, "AnalysisService", title="Nitrate (NO3)", Keyword = "drinking_nitrate", Methods=sm4500_no3d, Accredited=True, Unit="mg/L", PointOfCapture="lab", Category=drinkingcategory, LowerDetectionLimit="0.001", Precision=3, ExponentialFormatPrecision=7).UID()
drinking_coliform_pa = api.create(analysisservices, "AnalysisService", title="Coliform (PA)", Keyword = "drinking_coliform_pa", Methods=sm9223b, Accredited=True, Unit="-", PointOfCapture="lab", Category=drinkingcategory, LowerDetectionLimit="0", ExponentialFormatPrecision=7, ResultOptions=[{'ResultValue':'0','ResultText':'ABSENT'},{'ResultValue':'1','ResultText':'PRESENT'},{'ResultValue':'-1','ResultText':'INCONCLUSIVE'}]).UID()
drinking_ecoli_pa = api.create(analysisservices, "AnalysisService", title="E.coli (PA)", Keyword = "drinking_ecoli_pa", Methods=sm9223b, Accredited=True, Unit="-", PointOfCapture="lab", Category=drinkingcategory, LowerDetectionLimit="0", ExponentialFormatPrecision=7, ResultOptions=[{'ResultValue':'0','ResultText':'ABSENT'},{'ResultValue':'1','ResultText':'PRESENT'},{'ResultValue':'-1','ResultText':'INCONCLUSIVE'}]).UID()
drinking_fecal = api.create(analysisservices, "AnalysisService", title="Fecal Coliform", Keyword = "drinking_fecal_coliform", Methods=sm9223b, Accredited=True, Unit="-", PointOfCapture="lab", Category=drinkingcategory, LowerDetectionLimit="0", ExponentialFormatPrecision=7, ResultOptions=[{'ResultValue':'0','ResultText':'ABSENT'},{'ResultValue':'1','ResultText':'PRESENT'},{'ResultValue':'-1','ResultText':'INCONCLUSIVE'}]).UID()

##Surface Water

surface_coliform_mpn = api.create(analysisservices, "AnalysisService", title="Coliform (MPN)", Keyword = "surface_coliform_mpn", Methods=sm9223b, Accredited=True, Unit="mpn/100mL", PointOfCapture="lab", Category=surfacecategory, LowerDetectionLimit="1", Precision=0, ExponentialFormatPrecision=7).UID()
surface_ecoli_mpn = api.create(analysisservices, "AnalysisService", title="E.coli (MPN)", Keyword = "surface_coli_mpn", Methods=sm9223b, Accredited=True, Unit="mpn/100mL", PointOfCapture="lab", Category=surfacecategory, LowerDetectionLimit="1", Precision=0, ExponentialFormatPrecision=7).UID()
surface_coliform_mpn_10x = api.create(analysisservices, "AnalysisService", title="Coliform (MPN) - 10x", Keyword = "surface_coliform_mpn_10x", Methods=sm9223b, Accredited=True, Unit="mpn/10mL", PointOfCapture="lab", Category=surfacecategory, LowerDetectionLimit="10", Precision=0, ExponentialFormatPrecision=7).UID()
surface_ecoli_mpn_10x = api.create(analysisservices, "AnalysisService", title="E.coli (MPN) - 10x", Keyword = "surface_ecoli_mpn_10x", Methods=sm9223b, Accredited=True, Unit="mpn/10mL", PointOfCapture="lab", Category=surfacecategory, LowerDetectionLimit="10", Precision=0, ExponentialFormatPrecision=7).UID()
surface_coliform_mpn_fsma = api.create(analysisservices, "AnalysisService", title="Coliform (MPN) - FSMA", Keyword = "surface_oliform_mpn_fsma", Methods=sm9223b, Accredited=True, Unit="mpn/100mL", PointOfCapture="lab", Category=surfacecategory, LowerDetectionLimit="1", Precision=0, ExponentialFormatPrecision=7).UID()
surface_ecoli_mpn_fsma = api.create(analysisservices, "AnalysisService", title="E.coli (MPN) - FSMA", Keyword = "surface_ecoli_mpn_fsma", Methods=sm9223b, Accredited=True, Unit="mpn/100mL", PointOfCapture="lab", Category=surfacecategory, LowerDetectionLimit="1", Precision=0, ExponentialFormatPrecision=7).UID()

##Hydro Water

liqfert_ph = api.create(analysisservices, "AnalysisService", title="pH", Keyword="liqfert_ph", Methods=aoac973_41, Accredited=True, Unit="-", PointOfCapture="lab", Category=liqfertcategory, LowerDetectionLimit="0.01", ExponentialFormatPrecision=7).UID()
liqfert_soluablesalts = api.create(analysisservices, "AnalysisService", title="Soluable Salts", Keyword="liqfert_soluablesalts", Methods=sm2540c, Accredited=True, Unit="mS/cm", PointOfCapture="lab", Category=liqfertcategory, LowerDetectionLimit="0.01", Precision=2, ExponentialFormatPrecision=7).UID()
liqfert_tds = api.create(analysisservices, "AnalysisService", title="Total Dissolved Solids (TDS)", Keyword="liqfert_tds", Methods=sm2510b, Accredited=True, Unit="ppm", PointOfCapture="lab", Category=liqfertcategory, LowerDetectionLimit="0.1", Precision=2, ExponentialFormatPrecision=7).UID()
liqfert_chloride = api.create(analysisservices, "AnalysisService", title="Chloride (Cl-)", Keyword="liqfert_chloride", Methods=sm4500_cl, Accredited=True, Unit="ppm", PointOfCapture="lab", Category=liqfertcategory, LowerDetectionLimit="0.05", Precision=2, ExponentialFormatPrecision=7).UID()
liqfert_sulfur = api.create(analysisservices, "AnalysisService", title="Sulfur (S)", Keyword="liqfert_sulfur", Methods=[aoac993_14], Accredited=True, Unit="ppm", PointOfCapture="lab", Category=liqfertcategory, LowerDetectionLimit="0.05", Precision=2, ExponentialFormatPrecision=7).UID()
liqfert_phosphorus = api.create(analysisservices, "AnalysisService", title="Phosphorous (P)", Keyword="liqfert_phosphorous", Methods=[aoac993_14], Accredited=True, Unit="ppm", PointOfCapture="lab", Category=liqfertcategory, LowerDetectionLimit="0.05", Precision=2, ExponentialFormatPrecision=7).UID()
liqfert_calcium = api.create(analysisservices, "AnalysisService", title="Calcium (Ca)", Keyword="liqfert_calcium", Methods=[aoac993_14], Accredited=True, Unit="ppm", PointOfCapture="lab", Category=liqfertcategory, LowerDetectionLimit="0.05", Precision=2, ExponentialFormatPrecision=7).UID()
liqfert_potassium = api.create(analysisservices, "AnalysisService", title="Potassium (K)", Keyword="liqfert_potassium", Methods=[aoac993_14], Accredited=True, Unit="ppm", PointOfCapture="lab", Category=liqfertcategory, LowerDetectionLimit="0.05", Precision=2, ExponentialFormatPrecision=7).UID()
liqfert_magnesium = api.create(analysisservices, "AnalysisService", title="Magnesium (Mg)", Keyword="liqfert_magnesium", Methods=[aoac993_14], Accredited=True, Unit="ppm", PointOfCapture="lab", Category=liqfertcategory, LowerDetectionLimit="0.05", Precision=2, ExponentialFormatPrecision=7).UID()
liqfert_sodium = api.create(analysisservices, "AnalysisService", title="Sodium (Na)", Keyword="liqfert_sodium", Methods=[aoac993_14], Accredited=True, Unit="ppm", PointOfCapture="lab", Category=liqfertcategory, LowerDetectionLimit="0.05", Precision=2, ExponentialFormatPrecision=7).UID()
liqfert_aluminum = api.create(analysisservices, "AnalysisService", title="Aluminum (Al)", Keyword="liqfert_aluminum", Methods=[aoac993_14], Accredited=True, Unit="ppm", PointOfCapture="lab", Category=liqfertcategory, LowerDetectionLimit="0.05", Precision=2, ExponentialFormatPrecision=7).UID()
liqfert_boron = api.create(analysisservices, "AnalysisService", title="Boron (B)", Keyword="liqfert_boron", Methods=[aoac993_14], Accredited=True, Unit="ppm", PointOfCapture="lab", Category=liqfertcategory, LowerDetectionLimit="0.05", Precision=2, ExponentialFormatPrecision=7).UID()
liqfert_cobalt = api.create(analysisservices, "AnalysisService", title="Cobalt (Co)", Keyword="liqfert_cobalt", Methods=[aoac993_14], Accredited=True, Unit="ppm", PointOfCapture="lab", Category=liqfertcategory, LowerDetectionLimit="0.05", Precision=2, ExponentialFormatPrecision=7).UID()
liqfert_copper = api.create(analysisservices, "AnalysisService", title="Copper (Cu)", Keyword="liqfert_copper", Methods=[aoac993_14], Accredited=True, Unit="ppm", PointOfCapture="lab", Category=liqfertcategory, LowerDetectionLimit="0.05", Precision=2, ExponentialFormatPrecision=7).UID()
liqfert_iron = api.create(analysisservices, "AnalysisService", title="Iron (Fe)", Keyword="liqfert_iron", Methods=[aoac993_14], Accredited=True, Unit="ppm", PointOfCapture="lab", Category=liqfertcategory, LowerDetectionLimit="0.05", Precision=2, ExponentialFormatPrecision=7).UID()
liqfert_manganese = api.create(analysisservices, "AnalysisService", title="Manganese (Mn)", Keyword="liqfert_manganese", Methods=[aoac993_14], Accredited=True, Unit="ppm", PointOfCapture="lab", Category=liqfertcategory, LowerDetectionLimit="0.05", Precision=2, ExponentialFormatPrecision=7).UID()
liqfert_molybdenum = api.create(analysisservices, "AnalysisService", title="Molybdenum (Mo)", Keyword="liqfert_molybdenum", Methods=[aoac993_14], Accredited=True, Unit="ppm", PointOfCapture="lab", Category=liqfertcategory, LowerDetectionLimit="0.05", Precision=2, ExponentialFormatPrecision=7).UID()
liqfert_nickel = api.create(analysisservices, "AnalysisService", title="Nickel (Ni)", Keyword="liqfert_nickel", Methods=[aoac993_14], Accredited=True, Unit="ppm", PointOfCapture="lab", Category=liqfertcategory, LowerDetectionLimit="0.05", Precision=2, ExponentialFormatPrecision=7).UID()
liqfert_selenium = api.create(analysisservices, "AnalysisService", title="Selenium (Se)", Keyword="liqfert_selenium", Methods=[aoac993_14], Accredited=True, Unit="ppm", PointOfCapture="lab", Category=liqfertcategory, LowerDetectionLimit="0.05", Precision=2, ExponentialFormatPrecision=7).UID()
liqfert_silica = api.create(analysisservices, "AnalysisService", title="Silica (Si)", Keyword="liqfert_silica", Methods=[aoac993_14], Accredited=True, Unit="ppm", PointOfCapture="lab", Category=liqfertcategory, LowerDetectionLimit="0.05", Precision=2, ExponentialFormatPrecision=7).UID()
liqfert_zinc = api.create(analysisservices, "AnalysisService", title="Zinc (Zn)", Keyword="liqfert_zinc", Methods=[aoac993_14], Accredited=True, Unit="ppm", PointOfCapture="lab", Category=liqfertcategory, LowerDetectionLimit="0.05", Precision=2, ExponentialFormatPrecision=7).UID()
liqfert_ammonia = api.create(analysisservices, "AnalysisService", title="Ammonia (NH4) as Nitrogen (N)", Keyword="liqfert_ammonia", Methods=sm4500_no3d, Accredited=True, Unit="ppm", PointOfCapture="lab", Category=liqfertcategory, LowerDetectionLimit="0.01", Precision=2, ExponentialFormatPrecision=7).UID()
liqfert_nitrate = api.create(analysisservices, "AnalysisService", title="Nitrate (NO3) as Nitrogen (N)", Keyword="liqfert_nitrate", Methods=sm4500_modnh3, Accredited=True, Unit="ppm", PointOfCapture="lab", Category=liqfertcategory, LowerDetectionLimit="0.01", Precision=2, ExponentialFormatPrecision=7).UID()

#Calculations

sap_nitrate_calc = api.create(calculations, "Calculation", title="Nitrate as N to Nitrate (Sap)", Formula="[sap_nitrogen_as_nitrate]*4.43")
sap_kca_calc = api.create(calculations, "Calculation", title="K/Ca Ratio (Sap)", Formula="[sap_potassium]/[sap_calcium]")
sap_nitrogen_conversion_ratio = api.create(calculations, "Calculation", title="Nitrogen Conversion Ratio", Formula="1 - ( ( [sap_nitrogen_as_nitrate] + [sap_nitrogen_as_ammonium] ) / [sap_total_nitrogen] )")

for i in api.search({'portal_type':'Calculation'}):
    api.get_object(i).reindexObject()

#Finalize AnalysisServices
api.get_object(sap_nno3).Calculation = sap_nitrate_calc
api.get_object(sap_kca).Calculation = sap_kca_calc

for i in api.search({'portal_type':'AnalysisService'}):
    api.get_object(i).reindexObject()

#AnalysisProfiles

profile_lead_copper = api.create(profiles, "AnalysisProfile", title="Lead/Copper - Drinking Water", Service=[drinking_pb,drinking_cu]).UID()
profile_ecoli_coliform_pa = api.create(profiles, "AnalysisProfile", title="E.coli/Coliform PA", Service=[drinking_coliform_pa,drinking_ecoli_pa]).UID()
profile_nitrate = api.create(profiles, "AnalysisProfile", title="Nitrate - Drinking Water", Service=[drinking_no3]).UID()
profile_nitrite = api.create(profiles, "AnalysisProfile", title="Nitrite - Drinking Water", Service=[drinking_no3]).UID()
profile_ecoli_coliform_mpn = api.create(profiles, "AnalysisProfile", title="E.coli/Coliform MPN", Service=[surface_coliform_mpn,surface_ecoli_mpn]).UID()
profile_ecoli_coliform_mpn_FSMA = api.create(profiles, "AnalysisProfile", title="E.coli/Coliform MPN - FSMA", Service=[surface_coliform_mpn_fsma,surface_ecoli_mpn_fsma]).UID()
profile_ecoli_coliform_mpn_10x = api.create(profiles, "AnalysisProfile", title="E.coli/Coliform MPN - 10x", Service=[surface_coliform_mpn_10x,surface_ecoli_mpn_10x]).UID()

profile_sap = api.create(profiles, "AnalysisProfile", title="Sap", Service=[sap_al,sap_b,sap_brix,sap_sugar,sap_ca,sap_cl,sap_co,sap_cu,sap_ec,sap_fe,\
sap_kca,sap_mg,sap_mn,sap_mo,sap_ncr,sap_ni,sap_no3,sap_nnh4,sap_nno3,sap_totaln,sap_ph,sap_p,sap_k,sap_se,sap_si,sap_na,sap_s,sap_zn]).UID()

profile_hp_01 = api.create(profiles, "AnalysisProfile", title="HP-01", Service=[liqfert_ph,liqfert_soluablesalts,liqfert_tds,liqfert_chloride,liqfert_sulfur,\
liqfert_phosphorus,liqfert_calcium,liqfert_potassium,liqfert_magnesium,liqfert_sodium,liqfert_aluminum,liqfert_boron,liqfert_cobalt,liqfert_copper,liqfert_iron,\
liqfert_manganese,liqfert_molybdenum,liqfert_selenium,liqfert_nickel,liqfert_silica,liqfert_zinc,liqfert_ammonia,liqfert_nitrate]).UID()

for i in api.search({'portal_type':'AnalysisProfile'}):
    api.get_object(i).reindexObject()

#SampleTypes
saptype = api.create(sampletypes, "SampleType", title="Sap").UID()
soiltype = api.create(sampletypes, "SampleType", title="Soil").UID()
canntype = api.create(sampletypes, "SampleType", title="Cannabis Flower").UID()
drinkingtype = api.create(sampletypes, "SampleType", title="Water, Drinking").UID()
surfacetype = api.create(sampletypes, "SampleType", title="Water, Surface").UID()
hydrotype = api.create(sampletypes, "SampleType", title="Water, Liquid Fertilizer").UID()
frozentype = api.create(sampletypes, "SampleType", title="Food, Frozen").UID()
rawtype = api.create(sampletypes, "SampleType", title="Food, Raw").UID()
airtype = api.create(sampletypes, "SampleType", title="Compressed Air").UID()
preptype = api.create(sampletypes, "SampleType", title="Prep").UID()
cleantype = api.create(sampletypes, "SampleType", title="Cleanup").UID()

for i in api.search({'portal_type':'SampleType'}):
    api.get_object(i).reindexObject()

#AnalysisSpecifications

##Hemp
rr27 = {"keyword":"sap_total_sugar","uid":sap_sugar,              "min":"2.5",   "max":"4"}
rr3 = {"keyword":"sap_brix","uid":sap_brix,                 "min":"5.6",   "max":"10.3"}
rr19 = {"keyword":"sap_ph","uid":sap_ph,                   "min":"6.6",   "max":"7.3"}
rr8 = {"keyword":"sap_ec","uid":sap_ec,                    "min":"8",     "max":"14"}
rr5 = {"keyword":"sap_chloride","uid":sap_cl,              "min":"770",   "max":"1800"}
rr25 = {"keyword":"sap_sulfur","UID":sap_s,"uid":sap_s,              "min":"180",   "max":"400"}
rr20 = {"keyword":"sap_phosphorous","uid":sap_p,          "min":"125",   "max":"200"}
rr4 = {"keyword":"sap_calcium","uid":sap_ca,              "min":"780",   "max":"1500"}
rr21 = {"keyword":"sap_potassium","uid":sap_k,            "min":"2200",  "max":"4600"}
rr10 = {"keyword":"sap_kcaratio","uid":sap_kca,             "min":"",      "max":""}
rr11 = {"keyword":"sap_magnesium","uid":sap_mg,           "min":"300",   "max":"730"}
rr24 = {"keyword":"sap_sodium","uid":sap_na,               "min":"15",    "max":"50"}
rr1 = {"keyword":"sap_aluminum","uid":sap_al,              "min":"",      "max":""}
rr2 = {"keyword":"sap_boron","uid":sap_b,                 "min":"3.5",   "max":"12"}
rr6 = {"keyword":"sap_cobalt","uid":sap_co,                "min":"0.025", "max":"0.25"}
rr7 = {"keyword":"sap_copper","uid":sap_cu,                "min":"1.5",   "max":"8"}
rr9 = {"keyword":"sap_iron","uid":sap_fe,                  "min":"4",     "max":"15"}
rr12 = {"keyword":"sap_manganese","uid":sap_mn,            "min":"1.5",   "max":"10"}
rr13 = {"keyword":"sap_molybdenum","uid":sap_mo,          "min":"1.3",   "max":"5"}
rr14 = {"keyword":"sap_nickel","uid":sap_ni,               "min":".06",   "max":"0.17"}
rr22 = {"keyword":"sap_selenium","uid":sap_se,             "min":"",      "max":""}
rr23 = {"keyword":"sap_silica","uid":sap_si,               "min":"85",    "max":"130"}
rr26 = {"keyword":"sap_zinc","uid":sap_zn,                "min":"3",     "max":"10"}
rr16 = {"keyword":"sap_nitrogen_as_ammonium","uid":sap_nnh4, "min":"",      "max":""}
rr17 = {"keyword":"sap_nitrogen_as_nitrate","uid":sap_nno3,  "min":"450",   "max":"900"}
rr18 = {"keyword":"sap_total_nitrogen","UID":sap_totaln,"uid":sap_totaln,      "min":"1000",  "max":"2000"}
rr15 = {"keyword":"sap_nitrate","UID":sap_no3,"uid":sap_no3,             "min":"3000",  "max":"7000"}
rr = [rr1,rr2,rr3,rr4,rr5,rr6,rr7,rr8,rr9,rr10,rr11,rr12,rr13,rr14,rr14,rr15,rr16,rr17,rr18,rr19,rr20,rr21,rr22,rr23,rr24,rr25,rr26,rr27]
hemp_spec = api.create(specs, "AnalysisSpec", title="Hemp Sap", SampleType=saptype, ResultsRange=rr).UID()

##Alfalfa
rr27 = {"keyword":"sap_total_sugar","uid":sap_sugar,"min":"",     "max":""}
rr3 = {"keyword":"sap_brix","uid":sap_brix,"min":"5",     "max":"12"}
rr19 = {"keyword":"sap_ph","uid":sap_ph,"min":"6.5",     "max":"7"}
rr8 = {"keyword":"sap_ec","uid":sap_ec,                    "min":"9",     "max":"13"}
rr5 = {"keyword":"sap_chloride","uid":sap_cl,              "min":"1000",     "max":"3000"}
rr25 = {"keyword":"sap_sulfur","UID":sap_s,"uid":sap_s,              "min":"250",     "max":"700"}
rr20 = {"keyword":"sap_phosphorous","uid":sap_p,          "min":"150",     "max":"350"}
rr4 = {"keyword":"sap_calcium","uid":sap_ca,              "min":"400",     "max":"800"}
rr21 = {"keyword":"sap_potassium","uid":sap_k,            "min":"4500",     "max":"6000"}
rr10 = {"keyword":"sap_kcaratio","uid":sap_kca,             "min":"",     "max":""}
rr11 = {"keyword":"sap_magnesium","uid":sap_mg,           "min":"300",     "max":"700"}
rr24 = {"keyword":"sap_sodium","uid":sap_na,               "min":"200",     "max":"500"}
rr1 = {"keyword":"sap_aluminum","uid":sap_al,              "min":"",     "max":""}
rr2 = {"keyword":"sap_boron","uid":sap_b,                 "min":"3",     "max":"15"}
rr6 = {"keyword":"sap_cobalt","uid":sap_co,                "min":"",     "max":""}
rr7 = {"keyword":"sap_copper","uid":sap_cu,                "min":"1.5",     "max":"5"}
rr9 = {"keyword":"sap_iron","uid":sap_fe,                  "min":"3",     "max":"15"}
rr12 = {"keyword":"sap_manganese","uid":sap_mn,            "min":"1.5",     "max":"10"}
rr13 = {"keyword":"sap_molybdenum","uid":sap_mo,          "min":"",     "max":""}
rr14 = {"keyword":"sap_nickel","uid":sap_ni,               "min":"",     "max":""}
rr22 = {"keyword":"sap_selenium","uid":sap_se,             "min":"",     "max":""}
rr23 = {"keyword":"sap_silica","uid":sap_si,               "min":"5",     "max":"30"}
rr26 = {"keyword":"sap_zinc","uid":sap_zn,                "min":"3",     "max":"10"}
rr16 = {"keyword":"sap_nitrogen_as_ammonium","uid":sap_nnh4, "min":"",     "max":""}
rr17 = {"keyword":"sap_nitrogen_as_nitrate","uid":sap_nno3,  "min":"900",     "max":"1130"}
rr18 = {"keyword":"sap_total_nitrogen","UID":sap_totaln,"uid":sap_totaln,      "min":"",     "max":""}
rr15 = {"keyword":"sap_nitrate","UID":sap_no3,"uid":sap_no3,             "min":"4000",     "max":"5000"}
rr = [rr1,rr2,rr3,rr4,rr5,rr6,rr7,rr8,rr9,rr10,rr11,rr12,rr13,rr14,rr14,rr15,rr16,rr17,rr18,rr19,rr20,rr21,rr22,rr23,rr24,rr25,rr26,rr27]
alfalfa_spec = api.create(specs, "AnalysisSpec", title="Alfalfa Sap", SampleType=saptype, ResultsRange=rr).UID()

##Almond
rr27 = {"keyword":"sap_total_sugar","uid":sap_sugar,                "min":"2.5",     "max":"4"}
rr3 = {"keyword":"sap_brix","uid":sap_brix,                 "min":"5.6",     "max":"12"}
rr19 = {"keyword":"sap_ph","uid":sap_ph,                   "min":"5.5",     "max":"6"}
rr8 = {"keyword":"sap_ec","uid":sap_ec,                    "min":"8",     "max":"10"}
rr5 = {"keyword":"sap_chloride","uid":sap_cl,              "min":"350",     "max":"1500"}
rr25 = {"keyword":"sap_sulfur","UID":sap_s,"uid":sap_s,              "min":"60",     "max":"250"}
rr20 = {"keyword":"sap_phosphorous","uid":sap_p,          "min":"150",     "max":"250"}
rr4 = {"keyword":"sap_calcium","uid":sap_ca,              "min":"500",     "max":"1000"}
rr21 = {"keyword":"sap_potassium","uid":sap_k,            "min":"3500",     "max":"5000"}
rr10 = {"keyword":"sap_kcaratio","uid":sap_kca,             "min":"",     "max":""}
rr11 = {"keyword":"sap_magnesium","uid":sap_mg,           "min":"600",     "max":"1200"}
rr24 = {"keyword":"sap_sodium","uid":sap_na,               "min":"25",     "max":"100"}
rr1 = {"keyword":"sap_aluminum","uid":sap_al,              "min":"",     "max":""}
rr2 = {"keyword":"sap_boron","uid":sap_b,                 "min":"3",     "max":"10"}
rr6 = {"keyword":"sap_cobalt","uid":sap_co,                "min":"",     "max":""}
rr7 = {"keyword":"sap_copper","uid":sap_cu,                "min":"0.6",     "max":""}
rr9 = {"keyword":"sap_iron","uid":sap_fe,                  "min":"2",     "max":"10"}
rr12 = {"keyword":"sap_manganese","uid":sap_mn,            "min":"2",     "max":"20"}
rr13 = {"keyword":"sap_molybdenum","uid":sap_mo,          "min":"",     "max":""}
rr14 = {"keyword":"sap_nickel","uid":sap_ni,               "min":"",     "max":""}
rr22 = {"keyword":"sap_selenium","uid":sap_se,             "min":"",     "max":""}
rr23 = {"keyword":"sap_silica","uid":sap_si,               "min":"20",     "max":"60"}
rr26 = {"keyword":"sap_zinc","uid":sap_zn,                "min":"2",     "max":"5"}
rr16 = {"keyword":"sap_nitrogen_as_ammonium","uid":sap_nnh4, "min":"",     "max":""}
rr17 = {"keyword":"sap_nitrogen_as_nitrate","uid":sap_nno3,  "min":"40",     "max":"90"}
rr18 = {"keyword":"sap_total_nitrogen","UID":sap_totaln,"uid":sap_totaln,      "min":"750",     "max":"1500"}
rr15 = {"keyword":"sap_nitrate","UID":sap_no3,"uid":sap_no3,             "min":"180",     "max":"400"}
rr = [rr1,rr2,rr3,rr4,rr5,rr6,rr7,rr8,rr9,rr10,rr11,rr12,rr13,rr14,rr14,rr15,rr16,rr17,rr18,rr19,rr20,rr21,rr22,rr23,rr24,rr25,rr26,rr27]
almond_spec = api.create(specs, "AnalysisSpec", title="Almond Sap", SampleType=saptype, ResultsRange=rr).UID()

##Apple
rr27 = {"keyword":"sap_total_sugar","uid":sap_sugar,                "min":"6",     "max":"7"}
rr3 = {"keyword":"sap_brix","uid":sap_brix,                 "min":"",     "max":""}
rr19 = {"keyword":"sap_ph","uid":sap_ph,                   "min":"5.8",     "max":"6.3"}
rr8 = {"keyword":"sap_ec","uid":sap_ec,                    "min":"10.5",     "max":"11.5"}
rr5 = {"keyword":"sap_chloride","uid":sap_cl,              "min":"500",     "max":"1400"}
rr25 = {"keyword":"sap_sulfur","UID":sap_s,"uid":sap_s,              "min":"120",     "max":"150"}
rr20 = {"keyword":"sap_phosphorous","uid":sap_p,          "min":"200",     "max":"500"}
rr4 = {"keyword":"sap_calcium","uid":sap_ca,              "min":"200",     "max":"500"}
rr21 = {"keyword":"sap_potassium","uid":sap_k,            "min":"3000",     "max":"4000"}
rr10 = {"keyword":"sap_kcaratio","uid":sap_kca,             "min":"",     "max":""}
rr11 = {"keyword":"sap_magnesium","uid":sap_mg,           "min":"200",     "max":"500"}
rr24 = {"keyword":"sap_sodium","uid":sap_na,               "min":"10",     "max":"100"}
rr1 = {"keyword":"sap_aluminum","uid":sap_al,              "min":"",     "max":""}
rr2 = {"keyword":"sap_boron","uid":sap_b,                 "min":"5",     "max":"15"}
rr6 = {"keyword":"sap_cobalt","uid":sap_co,                "min":"",     "max":""}
rr7 = {"keyword":"sap_copper","uid":sap_cu,                "min":"1",     "max":"5"}
rr9 = {"keyword":"sap_iron","uid":sap_fe,                  "min":"2",     "max":"10"}
rr12 = {"keyword":"sap_manganese","uid":sap_mn,            "min":"5",     "max":"30"}
rr13 = {"keyword":"sap_molybdenum","uid":sap_mo,          "min":"0.2",     "max":"0.3"}
rr14 = {"keyword":"sap_nickel","uid":sap_ni,               "min":"",     "max":""}
rr22 = {"keyword":"sap_selenium","uid":sap_se,             "min":"",     "max":""}
rr23 = {"keyword":"sap_silica","uid":sap_si,               "min":"25",     "max":"50"}
rr26 = {"keyword":"sap_zinc","uid":sap_zn,                "min":"5",     "max":"15"}
rr16 = {"keyword":"sap_nitrogen_as_ammonium","uid":sap_nnh4, "min":"",     "max":""}
rr17 = {"keyword":"sap_nitrogen_as_nitrate","uid":sap_nno3,  "min":"7",     "max":"25"}
rr18 = {"keyword":"sap_total_nitrogen","UID":sap_totaln,"uid":sap_totaln,      "min":"100",     "max":"150"}
rr15 = {"keyword":"sap_nitrate","UID":sap_no3,"uid":sap_no3,             "min":"31",     "max":"110"}
rr = [rr1,rr2,rr3,rr4,rr5,rr6,rr7,rr8,rr9,rr10,rr11,rr12,rr13,rr14,rr14,rr15,rr16,rr17,rr18,rr19,rr20,rr21,rr22,rr23,rr24,rr25,rr26,rr27]
apple_spec = api.create(specs, "AnalysisSpec", title="Apple Sap", SampleType=saptype, ResultsRange=rr).UID()

##Apricot
rr27 = {"keyword":"sap_total_sugar","uid":sap_sugar,                "min":"1.5",     "max":"2"}
rr3 = {"keyword":"sap_brix","uid":sap_brix,                 "min":"3.5",     "max":"5"}
rr19 = {"keyword":"sap_ph","uid":sap_ph,                   "min":"5.5",     "max":"6"}
rr8 = {"keyword":"sap_ec","uid":sap_ec,                    "min":"1",     "max":"2.5"}
rr5 = {"keyword":"sap_chloride","uid":sap_cl,              "min":"350",     "max":"1500"}
rr25 = {"keyword":"sap_sulfur","UID":sap_s,"uid":sap_s,              "min":"60",     "max":"200"}
rr20 = {"keyword":"sap_phosphorous","uid":sap_p,          "min":"150",     "max":"350"}
rr4 = {"keyword":"sap_calcium","uid":sap_ca,              "min":"100",     "max":"250"}
rr21 = {"keyword":"sap_potassium","uid":sap_k,            "min":"4000",     "max":"7000"}
rr10 = {"keyword":"sap_kcaratio","uid":sap_kca,             "min":"",     "max":""}
rr11 = {"keyword":"sap_magnesium","uid":sap_mg,           "min":"500",     "max":"1000"}
rr24 = {"keyword":"sap_sodium","uid":sap_na,               "min":"25",     "max":"100"}
rr1 = {"keyword":"sap_aluminum","uid":sap_al,              "min":"",     "max":""}
rr2 = {"keyword":"sap_boron","uid":sap_b,                 "min":"3",     "max":"15"}
rr6 = {"keyword":"sap_cobalt","uid":sap_co,                "min":"",     "max":""}
rr7 = {"keyword":"sap_copper","uid":sap_cu,                "min":"1",     "max":"7"}
rr9 = {"keyword":"sap_iron","uid":sap_fe,                  "min":"4",     "max":"15"}
rr12 = {"keyword":"sap_manganese","uid":sap_mn,            "min":"3",     "max":"20"}
rr13 = {"keyword":"sap_molybdenum","uid":sap_mo,          "min":"0.5",     "max":"2.5"}
rr14 = {"keyword":"sap_nickel","uid":sap_ni,               "min":"",     "max":""}
rr22 = {"keyword":"sap_selenium","uid":sap_se,             "min":"",     "max":""}
rr23 = {"keyword":"sap_silica","uid":sap_si,               "min":"20",     "max":"50"}
rr26 = {"keyword":"sap_zinc","uid":sap_zn,                "min":"5",     "max":"15"}
rr16 = {"keyword":"sap_nitrogen_as_ammonium","uid":sap_nnh4, "min":"",     "max":""}
rr17 = {"keyword":"sap_nitrogen_as_nitrate","uid":sap_nno3,  "min":"23",     "max":"45"}
rr18 = {"keyword":"sap_total_nitrogen","UID":sap_totaln,"uid":sap_totaln,      "min":"",     "max":""}
rr15 = {"keyword":"sap_nitrate","UID":sap_no3,"uid":sap_no3,             "min":"100",     "max":"200"}
rr = [rr1,rr2,rr3,rr4,rr5,rr6,rr7,rr8,rr9,rr10,rr11,rr12,rr13,rr14,rr14,rr15,rr16,rr17,rr18,rr19,rr20,rr21,rr22,rr23,rr24,rr25,rr26,rr27]
apricot_spec = api.create(specs, "AnalysisSpec", title="Apricot Sap", SampleType=saptype, ResultsRange=rr).UID()

##Barley
rr27 = {"keyword":"sap_total_sugar","uid":sap_sugar,"min":"","max":""}
rr3 = {"keyword":"sap_brix","min":"10","max":"15"}
rr19 = {"keyword":"sap_ph","uid":sap_ph,"min":"6.5","max":"6.8"}
rr8 = {"keyword":"sap_ec","uid":sap_ec,"min":"","max":""}
rr5 = {"keyword":"sap_chloride","uid":sap_cl,"min":"","max":""}
rr25 = {"keyword":"sap_sulfur","UID":sap_s,"min":"200","max":"600"}
rr20 = {"keyword":"sap_phosphorous","uid":sap_p,"min":"150","max":"350"}
rr4 = {"keyword":"sap_calcium","min":"350","max":"700"}
rr21 = {"keyword":"sap_potassium","uid":sap_k,"min":"4500","max":"6500"}
rr10 = {"keyword":"sap_kcaratio","uid":sap_kca,"min":"","max":""}
rr11 = {"keyword":"sap_magnesium","min":"250","max":"500"}
rr24 = {"keyword":"sap_sodium","uid":sap_na,"min":"","max":""}
rr1 = {"keyword":"sap_aluminum","uid":sap_al,"min":"","max":""}
rr2 = {"keyword":"sap_boron","uid":sap_b,"min":"5","max":"15"}
rr6 = {"keyword":"sap_cobalt","uid":sap_co,"min":"","max":""}
rr7 = {"keyword":"sap_copper","uid":sap_cu,"min":"2","max":"5"}
rr9 = {"keyword":"sap_iron","uid":sap_fe,"min":"5","max":"15"}
rr12 = {"keyword":"sap_manganese","uid":sap_mn,"min":"5","max":"15"}
rr13 = {"keyword":"sap_molybdenum","min":"","max":""}
rr14 = {"keyword":"sap_nickel","uid":sap_ni,"min":"","max":""}
rr22 = {"keyword":"sap_selenium","uid":sap_se,"min":"","max":""}
rr23 = {"keyword":"sap_silica","uid":sap_si,"min":"25","max":"60"}
rr26 = {"keyword":"sap_zinc","min":"2","max":"5"}
rr16 = {"keyword":"sap_nitrogen_as_ammonium","uid":sap_nnh4,"min":"","max":""}
rr17 = {"keyword":"sap_nitrogen_as_nitrate","uid":sap_nno3,"min":"340","max":"790"}
rr18 = {"keyword":"sap_total_nitrogen","UID":sap_totaln,"min":"","max":""}
rr15 = {"keyword":"sap_nitrate","UID":sap_no3,"min":"1500","max":"3500"}
rr = [rr1,rr2,rr3,rr4,rr5,rr6,rr7,rr8,rr9,rr10,rr11,rr12,rr13,rr14,rr14,rr15,rr16,rr17,rr18,rr19,rr20,rr21,rr22,rr23,rr24,rr25,rr26,rr27]
barley_spec = api.create(specs, "AnalysisSpec", title="Barley Sap", SampleType=saptype, ResultsRange=rr).UID()

##Bean
rr27 = {"keyword":"sap_total_sugar","uid":sap_sugar,"min":"0.5","max":"1.1"}
rr3 = {"keyword":"sap_brix","min":"6","max":"10"}
rr19 = {"keyword":"sap_ph","uid":sap_ph,"min":"5","max":"7"}
rr8 = {"keyword":"sap_ec","uid":sap_ec,"min":"6","max":"10"}
rr5 = {"keyword":"sap_chloride","uid":sap_cl,"min":"750","max":"1500"}
rr25 = {"keyword":"sap_sulfur","UID":sap_s,"min":"100","max":"300"}
rr20 = {"keyword":"sap_phosphorous","uid":sap_p,"min":"175","max":"350"}
rr4 = {"keyword":"sap_calcium","min":"600","max":"1500"}
rr21 = {"keyword":"sap_potassium","uid":sap_k,"min":"2100","max":"4500"}
rr10 = {"keyword":"sap_kcaratio","uid":sap_kca,"min":"","max":""}
rr11 = {"keyword":"sap_magnesium","min":"250","max":"500"}
rr24 = {"keyword":"sap_sodium","uid":sap_na,"min":"5","max":"50"}
rr1 = {"keyword":"sap_aluminum","uid":sap_al,"min":"","max":""}
rr2 = {"keyword":"sap_boron","uid":sap_b,"min":"2","max":"10"}
rr6 = {"keyword":"sap_cobalt","uid":sap_co,"min":"","max":""}
rr7 = {"keyword":"sap_copper","uid":sap_cu,"min":"1","max":"4"}
rr9 = {"keyword":"sap_iron","uid":sap_fe,"min":"1","max":"5"}
rr12 = {"keyword":"sap_manganese","uid":sap_mn,"min":"4","max":"16"}
rr13 = {"keyword":"sap_molybdenum","min":"1","max":"2"}
rr14 = {"keyword":"sap_nickel","uid":sap_ni,"min":"","max":""}
rr22 = {"keyword":"sap_selenium","uid":sap_se,"min":"","max":""}
rr23 = {"keyword":"sap_silica","uid":sap_si,"min":"35","max":"70"}
rr26 = {"keyword":"sap_zinc","min":"3.5","max":"25"}
rr16 = {"keyword":"sap_nitrogen_as_ammonium","uid":sap_nnh4,"min":"","max":""}
rr17 = {"keyword":"sap_nitrogen_as_nitrate","uid":sap_nno3,"min":"125","max":"250"}
rr18 = {"keyword":"sap_total_nitrogen","UID":sap_totaln,"min":"3000","max":"6000"}
rr15 = {"keyword":"sap_nitrate","UID":sap_no3,"min":"553.75","max":"1107.5"}
rr = [rr1,rr2,rr3,rr4,rr5,rr6,rr7,rr8,rr9,rr10,rr11,rr12,rr13,rr14,rr14,rr15,rr16,rr17,rr18,rr19,rr20,rr21,rr22,rr23,rr24,rr25,rr26,rr27]
bean_spec = api.create(specs, "AnalysisSpec", title="Bean Sap", SampleType=saptype, ResultsRange=rr).UID()

##Blackberry
rr27 = {"keyword":"sap_total_sugar","uid":sap_sugar,"min":"5.5","max":"7.5"}
rr3 = {"keyword":"sap_brix","min":"","max":""}
rr19 = {"keyword":"sap_ph","uid":sap_ph,"min":"5.5","max":"7"}
rr8 = {"keyword":"sap_ec","uid":sap_ec,"min":"11","max":"12"}
rr5 = {"keyword":"sap_chloride","uid":sap_cl,"min":"400","max":"700"}
rr25 = {"keyword":"sap_sulfur","UID":sap_s,"min":"50","max":"150"}
rr20 = {"keyword":"sap_phosphorous","uid":sap_p,"min":"100","max":"250"}
rr4 = {"keyword":"sap_calcium","min":"400","max":"600"}
rr21 = {"keyword":"sap_potassium","uid":sap_k,"min":"2000","max":"3000"}
rr10 = {"keyword":"sap_kcaratio","uid":sap_kca,"min":"","max":""}
rr11 = {"keyword":"sap_magnesium","min":"350","max":"500"}
rr24 = {"keyword":"sap_sodium","uid":sap_na,"min":"30","max":"45"}
rr1 = {"keyword":"sap_aluminum","uid":sap_al,"min":"","max":""}
rr2 = {"keyword":"sap_boron","uid":sap_b,"min":"2","max":"10"}
rr6 = {"keyword":"sap_cobalt","uid":sap_co,"min":"0.25","max":"0.75"}
rr7 = {"keyword":"sap_copper","uid":sap_cu,"min":"0.8","max":"5"}
rr9 = {"keyword":"sap_iron","uid":sap_fe,"min":"2","max":"10"}
rr12 = {"keyword":"sap_manganese","uid":sap_mn,"min":"15","max":"50"}
rr13 = {"keyword":"sap_molybdenum","min":"0.75","max":"1"}
rr14 = {"keyword":"sap_nickel","uid":sap_ni,"min":"0.25","max":"1"}
rr22 = {"keyword":"sap_selenium","uid":sap_se,"min":"","max":""}
rr23 = {"keyword":"sap_silica","uid":sap_si,"min":"5","max":"10"}
rr26 = {"keyword":"sap_zinc","min":"2.5","max":"10"}
rr16 = {"keyword":"sap_nitrogen_as_ammonium","uid":sap_nnh4,"min":"","max":""}
rr17 = {"keyword":"sap_nitrogen_as_nitrate","uid":sap_nno3,"min":"35","max":"90"}
rr18 = {"keyword":"sap_total_nitrogen","UID":sap_totaln,"min":"550","max":"650"}
rr15 = {"keyword":"sap_nitrate","UID":sap_no3,"min":"150","max":"400"}
rr = [rr1,rr2,rr3,rr4,rr5,rr6,rr7,rr8,rr9,rr10,rr11,rr12,rr13,rr14,rr14,rr15,rr16,rr17,rr18,rr19,rr20,rr21,rr22,rr23,rr24,rr25,rr26,rr27]
blackberry_spec = api.create(specs, "AnalysisSpec", title="Blackberry Sap", SampleType=saptype, ResultsRange=rr).UID()

##Blackberry Fruitfill
rr27 = {"keyword":"sap_total_sugar","uid":sap_sugar,"min":"5.5","max":"7.5"}
rr3 = {"keyword":"sap_brix","min":"7","max":"12"}
rr19 = {"keyword":"sap_ph","uid":sap_ph,"min":"5.5","max":"7"}
rr8 = {"keyword":"sap_ec","uid":sap_ec,"min":"11","max":"12"}
rr5 = {"keyword":"sap_chloride","uid":sap_cl,"min":"400","max":"700"}
rr25 = {"keyword":"sap_sulfur","UID":sap_s,"min":"50","max":"150"}
rr20 = {"keyword":"sap_phosphorous","uid":sap_p,"min":"100","max":"250"}
rr4 = {"keyword":"sap_calcium","min":"400","max":"600"}
rr21 = {"keyword":"sap_potassium","uid":sap_k,"min":"2000","max":"3000"}
rr10 = {"keyword":"sap_kcaratio","uid":sap_kca,"min":"","max":""}
rr11 = {"keyword":"sap_magnesium","min":"350","max":"500"}
rr24 = {"keyword":"sap_sodium","uid":sap_na,"min":"30","max":"45"}
rr1 = {"keyword":"sap_aluminum","uid":sap_al,"min":"","max":""}
rr2 = {"keyword":"sap_boron","uid":sap_b,"min":"2","max":"10"}
rr6 = {"keyword":"sap_cobalt","uid":sap_co,"min":"0.25","max":"0.75"}
rr7 = {"keyword":"sap_copper","uid":sap_cu,"min":"0.8","max":"5"}
rr9 = {"keyword":"sap_iron","uid":sap_fe,"min":"2","max":"10"}
rr12 = {"keyword":"sap_manganese","uid":sap_mn,"min":"15","max":"50"}
rr13 = {"keyword":"sap_molybdenum","min":"0.75","max":"1"}
rr14 = {"keyword":"sap_nickel","uid":sap_ni,"min":"0.25","max":"1"}
rr22 = {"keyword":"sap_selenium","uid":sap_se,"min":"","max":""}
rr23 = {"keyword":"sap_silica","uid":sap_si,"min":"5","max":"10"}
rr26 = {"keyword":"sap_zinc","min":"2.5","max":"10"}
rr16 = {"keyword":"sap_nitrogen_as_ammonium","uid":sap_nnh4,"min":"","max":""}
rr17 = {"keyword":"sap_nitrogen_as_nitrate","uid":sap_nno3,"min":"225","max":"790"}
rr18 = {"keyword":"sap_total_nitrogen","UID":sap_totaln,"min":"750","max":"2500"}
rr15 = {"keyword":"sap_nitrate","UID":sap_no3,"min":"1000","max":"3500"}
rr = [rr1,rr2,rr3,rr4,rr5,rr6,rr7,rr8,rr9,rr10,rr11,rr12,rr13,rr14,rr14,rr15,rr16,rr17,rr18,rr19,rr20,rr21,rr22,rr23,rr24,rr25,rr26,rr27]
blackberry_fruitfill_spec = api.create(specs, "AnalysisSpec", title="Blackberry Sap, Fruitfill", SampleType=saptype, ResultsRange=rr).UID()

##Blueberry
rr27 = {"keyword":"sap_total_sugar","uid":sap_sugar,"min":"2","max":"5"}
rr3 = {"keyword":"sap_brix","min":"","max":""}
rr19 = {"keyword":"sap_ph","uid":sap_ph,"min":"3.5","max":"3.8"}
rr8 = {"keyword":"sap_ec","uid":sap_ec,"min":"1.5","max":"4"}
rr5 = {"keyword":"sap_chloride","uid":sap_cl,"min":"175","max":"1000"}
rr25 = {"keyword":"sap_sulfur","UID":sap_s,"min":"50","max":"250"}
rr20 = {"keyword":"sap_phosphorous","uid":sap_p,"min":"150","max":"250"}
rr4 = {"keyword":"sap_calcium","min":"350","max":"1100"}
rr21 = {"keyword":"sap_potassium","uid":sap_k,"min":"2000","max":"4500"}
rr10 = {"keyword":"sap_kcaratio","uid":sap_kca,"min":"","max":""}
rr11 = {"keyword":"sap_magnesium","min":"300","max":"550"}
rr24 = {"keyword":"sap_sodium","uid":sap_na,"min":"10","max":"12"}
rr1 = {"keyword":"sap_aluminum","uid":sap_al,"min":"","max":""}
rr2 = {"keyword":"sap_boron","uid":sap_b,"min":"1.5","max":"8"}
rr6 = {"keyword":"sap_cobalt","uid":sap_co,"min":"","max":""}
rr7 = {"keyword":"sap_copper","uid":sap_cu,"min":"1.5","max":"5"}
rr9 = {"keyword":"sap_iron","uid":sap_fe,"min":"15","max":"20"}
rr12 = {"keyword":"sap_manganese","uid":sap_mn,"min":"15","max":"60"}
rr13 = {"keyword":"sap_molybdenum","min":"0.5","max":"1.5"}
rr14 = {"keyword":"sap_nickel","uid":sap_ni,"min":"","max":""}
rr22 = {"keyword":"sap_selenium","uid":sap_se,"min":"","max":""}
rr23 = {"keyword":"sap_silica","uid":sap_si,"min":"20","max":"80"}
rr26 = {"keyword":"sap_zinc","min":"3","max":"10"}
rr16 = {"keyword":"sap_nitrogen_as_ammonium","uid":sap_nnh4,"min":"","max":""}
rr17 = {"keyword":"sap_nitrogen_as_nitrate","uid":sap_nno3,"min":"25","max":"400"}
rr18 = {"keyword":"sap_total_nitrogen","UID":sap_totaln,"min":"300","max":"800"}
rr15 = {"keyword":"sap_nitrate","UID":sap_no3,"min":"110","max":"1200"}
rr = [rr1,rr2,rr3,rr4,rr5,rr6,rr7,rr8,rr9,rr10,rr11,rr12,rr13,rr14,rr14,rr15,rr16,rr17,rr18,rr19,rr20,rr21,rr22,rr23,rr24,rr25,rr26,rr27]
blueberry_spec = api.create(specs, "AnalysisSpec", title="Blueberry Sap", SampleType=saptype, ResultsRange=rr).UID()

##Broccoli
rr27 = {"keyword":"sap_total_sugar","uid":sap_sugar,"min":"1","max":"3"}
rr3 = {"keyword":"sap_brix","min":"4","max":"6"}
rr19 = {"keyword":"sap_ph","uid":sap_ph,"min":"5.5","max":"6.2"}
rr8 = {"keyword":"sap_ec","uid":sap_ec,"min":"8","max":"10"}
rr5 = {"keyword":"sap_chloride","uid":sap_cl,"min":"500","max":"2000"}
rr25 = {"keyword":"sap_sulfur","UID":sap_s,"min":"200","max":"400"}
rr20 = {"keyword":"sap_phosphorous","uid":sap_p,"min":"150","max":"300"}
rr4 = {"keyword":"sap_calcium","min":"300","max":"800"}
rr21 = {"keyword":"sap_potassium","uid":sap_k,"min":"4000","max":"5000"}
rr10 = {"keyword":"sap_kcaratio","uid":sap_kca,"min":"","max":""}
rr11 = {"keyword":"sap_magnesium","min":"250","max":"500"}
rr24 = {"keyword":"sap_sodium","uid":sap_na,"min":"250","max":"1000"}
rr1 = {"keyword":"sap_aluminum","uid":sap_al,"min":"","max":""}
rr2 = {"keyword":"sap_boron","uid":sap_b,"min":"1","max":"5"}
rr6 = {"keyword":"sap_cobalt","uid":sap_co,"min":"","max":""}
rr7 = {"keyword":"sap_copper","uid":sap_cu,"min":"1","max":"5"}
rr9 = {"keyword":"sap_iron","uid":sap_fe,"min":"1.5","max":"5"}
rr12 = {"keyword":"sap_manganese","uid":sap_mn,"min":"1","max":"5"}
rr13 = {"keyword":"sap_molybdenum","min":"0.5","max":"2"}
rr14 = {"keyword":"sap_nickel","uid":sap_ni,"min":"","max":""}
rr22 = {"keyword":"sap_selenium","uid":sap_se,"min":"","max":""}
rr23 = {"keyword":"sap_silica","uid":sap_si,"min":"5","max":"20"}
rr26 = {"keyword":"sap_zinc","min":"2","max":"5"}
rr16 = {"keyword":"sap_nitrogen_as_ammonium","uid":sap_nnh4,"min":"","max":""}
rr17 = {"keyword":"sap_nitrogen_as_nitrate","uid":sap_nno3,"min":"900","max":"1240"}
rr18 = {"keyword":"sap_total_nitrogen","UID":sap_totaln,"min":"2000","max":"3500"}
rr15 = {"keyword":"sap_nitrate","UID":sap_no3,"min":"4000","max":"5500"}
rr = [rr1,rr2,rr3,rr4,rr5,rr6,rr7,rr8,rr9,rr10,rr11,rr12,rr13,rr14,rr14,rr15,rr16,rr17,rr18,rr19,rr20,rr21,rr22,rr23,rr24,rr25,rr26,rr27]
broccoli_spec = api.create(specs, "AnalysisSpec", title="Broccoli Sap", SampleType=saptype, ResultsRange=rr).UID()

##Canola
rr27 = {"keyword":"sap_total_sugar","uid":sap_sugar,"min":"","max":""}
rr3 = {"keyword":"sap_brix","min":"","max":""}
rr19 = {"keyword":"sap_ph","uid":sap_ph,"min":"","max":""}
rr8 = {"keyword":"sap_ec","uid":sap_ec,"min":"","max":""}
rr5 = {"keyword":"sap_chloride","uid":sap_cl,"min":"","max":""}
rr25 = {"keyword":"sap_sulfur","UID":sap_s,"min":"200","max":"500"}
rr20 = {"keyword":"sap_phosphorous","uid":sap_p,"min":"150","max":"300"}
rr4 = {"keyword":"sap_calcium","min":"400","max":"700"}
rr21 = {"keyword":"sap_potassium","uid":sap_k,"min":"2500","max":"5000"}
rr10 = {"keyword":"sap_kcaratio","uid":sap_kca,"min":"","max":""}
rr11 = {"keyword":"sap_magnesium","min":"200","max":"400"}
rr24 = {"keyword":"sap_sodium","uid":sap_na,"min":"","max":""}
rr1 = {"keyword":"sap_aluminum","uid":sap_al,"min":"","max":""}
rr2 = {"keyword":"sap_boron","uid":sap_b,"min":"2","max":"8"}
rr6 = {"keyword":"sap_cobalt","uid":sap_co,"min":"","max":""}
rr7 = {"keyword":"sap_copper","uid":sap_cu,"min":"1","max":"5"}
rr9 = {"keyword":"sap_iron","uid":sap_fe,"min":"2.5","max":"15"}
rr12 = {"keyword":"sap_manganese","uid":sap_mn,"min":"2","max":"10"}
rr13 = {"keyword":"sap_molybdenum","min":"","max":""}
rr14 = {"keyword":"sap_nickel","uid":sap_ni,"min":"","max":""}
rr22 = {"keyword":"sap_selenium","uid":sap_se,"min":"","max":""}
rr23 = {"keyword":"sap_silica","uid":sap_si,"min":"5","max":"15"}
rr26 = {"keyword":"sap_zinc","min":"3","max":"10"}
rr16 = {"keyword":"sap_nitrogen_as_ammonium","uid":sap_nnh4,"min":"","max":""}
rr17 = {"keyword":"sap_nitrogen_as_nitrate","uid":sap_nno3,"min":"340","max":"790"}
rr18 = {"keyword":"sap_total_nitrogen","UID":sap_totaln,"min":"","max":""}
rr15 = {"keyword":"sap_nitrate","UID":sap_no3,"min":"1500","max":"3500"}
rr = [rr1,rr2,rr3,rr4,rr5,rr6,rr7,rr8,rr9,rr10,rr11,rr12,rr13,rr14,rr14,rr15,rr16,rr17,rr18,rr19,rr20,rr21,rr22,rr23,rr24,rr25,rr26,rr27]
canola_spec = api.create(specs, "AnalysisSpec", title="Canola Sap", SampleType=saptype, ResultsRange=rr).UID()

##Cauliflower
rr27 = {"keyword":"sap_total_sugar","uid":sap_sugar,"min":"1","max":"3"}
rr3 = {"keyword":"sap_brix","min":"4","max":"6"}
rr19 = {"keyword":"sap_ph","uid":sap_ph,"min":"5.5","max":"6.2"}
rr8 = {"keyword":"sap_ec","uid":sap_ec,"min":"8","max":"10"}
rr5 = {"keyword":"sap_chloride","uid":sap_cl,"min":"500","max":"2000"}
rr25 = {"keyword":"sap_sulfur","UID":sap_s,"min":"200","max":"350"}
rr20 = {"keyword":"sap_phosphorous","uid":sap_p,"min":"200","max":"400"}
rr4 = {"keyword":"sap_calcium","min":"300","max":"600"}
rr21 = {"keyword":"sap_potassium","uid":sap_k,"min":"4000","max":"5000"}
rr10 = {"keyword":"sap_kcaratio","uid":sap_kca,"min":"","max":""}
rr11 = {"keyword":"sap_magnesium","min":"180","max":"350"}
rr24 = {"keyword":"sap_sodium","uid":sap_na,"min":"250","max":"1000"}
rr1 = {"keyword":"sap_aluminum","uid":sap_al,"min":"","max":""}
rr2 = {"keyword":"sap_boron","uid":sap_b,"min":"4","max":"15"}
rr6 = {"keyword":"sap_cobalt","uid":sap_co,"min":"","max":""}
rr7 = {"keyword":"sap_copper","uid":sap_cu,"min":"1","max":"5"}
rr9 = {"keyword":"sap_iron","uid":sap_fe,"min":"1.5","max":"5"}
rr12 = {"keyword":"sap_manganese","uid":sap_mn,"min":"1","max":"5"}
rr13 = {"keyword":"sap_molybdenum","min":"0.5","max":"2"}
rr14 = {"keyword":"sap_nickel","uid":sap_ni,"min":"","max":""}
rr22 = {"keyword":"sap_selenium","uid":sap_se,"min":"","max":""}
rr23 = {"keyword":"sap_silica","uid":sap_si,"min":"5","max":"20"}
rr26 = {"keyword":"sap_zinc","min":"2","max":"5"}
rr16 = {"keyword":"sap_nitrogen_as_ammonium","uid":sap_nnh4,"min":"","max":""}
rr17 = {"keyword":"sap_nitrogen_as_nitrate","uid":sap_nno3,"min":"225","max":"900"}
rr18 = {"keyword":"sap_total_nitrogen","UID":sap_totaln,"min":"750","max":"2500"}
rr15 = {"keyword":"sap_nitrate","UID":sap_no3,"min":"1000","max":"4000"}
rr = [rr1,rr2,rr3,rr4,rr5,rr6,rr7,rr8,rr9,rr10,rr11,rr12,rr13,rr14,rr14,rr15,rr16,rr17,rr18,rr19,rr20,rr21,rr22,rr23,rr24,rr25,rr26,rr27]
cauliflower_spec = api.create(specs, "AnalysisSpec", title="Cauliflower Sap", SampleType=saptype, ResultsRange=rr).UID()

##Cherry
rr27 = {"keyword":"sap_total_sugar","uid":sap_sugar,"min":"1.5","max":"3"}
rr3 = {"keyword":"sap_brix","min":"5","max":"8"}
rr19 = {"keyword":"sap_ph","uid":sap_ph,"min":"5.8","max":"6.5"}
rr8 = {"keyword":"sap_ec","uid":sap_ec,"min":"3","max":"6"}
rr5 = {"keyword":"sap_chloride","uid":sap_cl,"min":"500","max":"1000"}
rr25 = {"keyword":"sap_sulfur","UID":sap_s,"min":"60","max":"200"}
rr20 = {"keyword":"sap_phosphorous","uid":sap_p,"min":"200","max":"300"}
rr4 = {"keyword":"sap_calcium","min":"250","max":"600"}
rr21 = {"keyword":"sap_potassium","uid":sap_k,"min":"2500","max":"3500"}
rr10 = {"keyword":"sap_kcaratio","uid":sap_kca,"min":"","max":""}
rr11 = {"keyword":"sap_magnesium","min":"150","max":"350"}
rr24 = {"keyword":"sap_sodium","uid":sap_na,"min":"25","max":"100"}
rr1 = {"keyword":"sap_aluminum","uid":sap_al,"min":"","max":""}
rr2 = {"keyword":"sap_boron","uid":sap_b,"min":"3","max":"10"}
rr6 = {"keyword":"sap_cobalt","uid":sap_co,"min":"","max":""}
rr7 = {"keyword":"sap_copper","uid":sap_cu,"min":"1","max":"5"}
rr9 = {"keyword":"sap_iron","uid":sap_fe,"min":"2","max":"10"}
rr12 = {"keyword":"sap_manganese","uid":sap_mn,"min":"1","max":"10"}
rr13 = {"keyword":"sap_molybdenum","min":"","max":""}
rr14 = {"keyword":"sap_nickel","uid":sap_ni,"min":"","max":""}
rr22 = {"keyword":"sap_selenium","uid":sap_se,"min":"","max":""}
rr23 = {"keyword":"sap_silica","uid":sap_si,"min":"20","max":"50"}
rr26 = {"keyword":"sap_zinc","min":"2","max":"10"}
rr16 = {"keyword":"sap_nitrogen_as_ammonium","uid":sap_nnh4,"min":"","max":""}
rr17 = {"keyword":"sap_nitrogen_as_nitrate","uid":sap_nno3,"min":"25","max":"55"}
rr18 = {"keyword":"sap_total_nitrogen","UID":sap_totaln,"min":"1000","max":"2500"}
rr15 = {"keyword":"sap_nitrate","UID":sap_no3,"min":"100","max":"250"}
rr = [rr1,rr2,rr3,rr4,rr5,rr6,rr7,rr8,rr9,rr10,rr11,rr12,rr13,rr14,rr14,rr15,rr16,rr17,rr18,rr19,rr20,rr21,rr22,rr23,rr24,rr25,rr26,rr27]
cherry_spec = api.create(specs, "AnalysisSpec", title="Cherry Sap", SampleType=saptype, ResultsRange=rr).UID()

##Onion
rr27 = {"keyword":"sap_total_sugar","uid":sap_sugar,"min":"1","max":"3"}
rr3 = {"keyword":"sap_brix","min":"4","max":"6"}
rr19 = {"keyword":"sap_ph","uid":sap_ph,"min":"6","max":"7"}
rr8 = {"keyword":"sap_ec","uid":sap_ec,"min":"12","max":"15"}
rr5 = {"keyword":"sap_chloride","uid":sap_cl,"min":"1000","max":"3000"}
rr25 = {"keyword":"sap_sulfur","UID":sap_s,"min":"100","max":"500"}
rr20 = {"keyword":"sap_phosphorous","uid":sap_p,"min":"60","max":"200"}
rr4 = {"keyword":"sap_calcium","min":"120","max":"350"}
rr21 = {"keyword":"sap_potassium","uid":sap_k,"min":"2000","max":"3500"}
rr10 = {"keyword":"sap_kcaratio","uid":sap_kca,"min":"","max":""}
rr11 = {"keyword":"sap_magnesium","min":"80","max":"250"}
rr24 = {"keyword":"sap_sodium","uid":sap_na,"min":"10","max":"50"}
rr1 = {"keyword":"sap_aluminum","uid":sap_al,"min":"","max":""}
rr2 = {"keyword":"sap_boron","uid":sap_b,"min":"1","max":"7"}
rr6 = {"keyword":"sap_cobalt","uid":sap_co,"min":"","max":""}
rr7 = {"keyword":"sap_copper","uid":sap_cu,"min":"1","max":"5"}
rr9 = {"keyword":"sap_iron","uid":sap_fe,"min":"2","max":"10"}
rr12 = {"keyword":"sap_manganese","uid":sap_mn,"min":"2","max":"10"}
rr13 = {"keyword":"sap_molybdenum","min":"","max":""}
rr14 = {"keyword":"sap_nickel","uid":sap_ni,"min":"","max":""}
rr22 = {"keyword":"sap_selenium","uid":sap_se,"min":"","max":""}
rr23 = {"keyword":"sap_silica","uid":sap_si,"min":"5","max":"20"}
rr26 = {"keyword":"sap_zinc","min":"1","max":"5"}
rr16 = {"keyword":"sap_nitrogen_as_ammonium","uid":sap_nnh4,"min":"","max":""}
rr17 = {"keyword":"sap_nitrogen_as_nitrate","uid":sap_nno3,"min":"70","max":"225"}
rr18 = {"keyword":"sap_total_nitrogen","UID":sap_totaln,"min":"250","max":"1000"}
rr15 = {"keyword":"sap_nitrate","UID":sap_no3,"min":"300","max":"1000"}
rr = [rr1,rr2,rr3,rr4,rr5,rr6,rr7,rr8,rr9,rr10,rr11,rr12,rr13,rr14,rr14,rr15,rr16,rr17,rr18,rr19,rr20,rr21,rr22,rr23,rr24,rr25,rr26,rr27]
onion_spec = api.create(specs, "AnalysisSpec", title="Onion Sap", SampleType=saptype, ResultsRange=rr).UID()

##Carrot
rr27 = {"keyword":"sap_total_sugar","uid":sap_sugar,"min":"1","max":"3"}
rr3 = {"keyword":"sap_brix","min":"4","max":"6"}
rr19 = {"keyword":"sap_ph","uid":sap_ph,"min":"5.5","max":"5.8"}
rr8 = {"keyword":"sap_ec","uid":sap_ec,"min":"12","max":"15"}
rr5 = {"keyword":"sap_chloride","uid":sap_cl,"min":"1000","max":"3000"}
rr25 = {"keyword":"sap_sulfur","UID":sap_s,"min":"100","max":"500"}
rr20 = {"keyword":"sap_phosphorous","uid":sap_p,"min":"100","max":"400"}
rr4 = {"keyword":"sap_calcium","min":"500","max":"1200"}
rr21 = {"keyword":"sap_potassium","uid":sap_k,"min":"5500","max":"8000"}
rr10 = {"keyword":"sap_kcaratio","uid":sap_kca,"min":"","max":""}
rr11 = {"keyword":"sap_magnesium","min":"250","max":"450"}
rr24 = {"keyword":"sap_sodium","uid":sap_na,"min":"100","max":"500"}
rr1 = {"keyword":"sap_aluminum","uid":sap_al,"min":"","max":""}
rr2 = {"keyword":"sap_boron","uid":sap_b,"min":"2","max":"10"}
rr6 = {"keyword":"sap_cobalt","uid":sap_co,"min":"","max":""}
rr7 = {"keyword":"sap_copper","uid":sap_cu,"min":"2","max":"20"}
rr9 = {"keyword":"sap_iron","uid":sap_fe,"min":"2","max":"10"}
rr12 = {"keyword":"sap_manganese","uid":sap_mn,"min":"1","max":"7"}
rr13 = {"keyword":"sap_molybdenum","min":"1.3","max":"5"}
rr14 = {"keyword":"sap_nickel","uid":sap_ni,"min":"","max":""}
rr22 = {"keyword":"sap_selenium","uid":sap_se,"min":"","max":""}
rr23 = {"keyword":"sap_silica","uid":sap_si,"min":"5","max":"20"}
rr26 = {"keyword":"sap_zinc","min":"1.5","max":"7"}
rr16 = {"keyword":"sap_nitrogen_as_ammonium","uid":sap_nnh4,"min":"","max":""}
rr17 = {"keyword":"sap_nitrogen_as_nitrate","uid":sap_nno3,"min":"340","max":"790"}
rr18 = {"keyword":"sap_total_nitrogen","UID":sap_totaln,"min":"1000","max":"2000"}
rr15 = {"keyword":"sap_nitrate","UID":sap_no3,"min":"1500","max":"3500"}
rr = [rr1,rr2,rr3,rr4,rr5,rr6,rr7,rr8,rr9,rr10,rr11,rr12,rr13,rr14,rr14,rr15,rr16,rr17,rr18,rr19,rr20,rr21,rr22,rr23,rr24,rr25,rr26,rr27]
carrot_spec = api.create(specs, "AnalysisSpec", title="Carrot Sap", SampleType=saptype, ResultsRange=rr).UID()

##Chard
rr27 = {"keyword":"sap_total_sugar","uid":sap_sugar,"min":"1","max":"3"}
rr3 = {"keyword":"sap_brix","min":"4","max":"6"}
rr19 = {"keyword":"sap_ph","uid":sap_ph,"min":"5.5","max":"6.2"}
rr8 = {"keyword":"sap_ec","uid":sap_ec,"min":"8","max":"10"}
rr5 = {"keyword":"sap_chloride","uid":sap_cl,"min":"500","max":"2000"}
rr25 = {"keyword":"sap_sulfur","UID":sap_s,"min":"200","max":"400"}
rr20 = {"keyword":"sap_phosphorous","uid":sap_p,"min":"150","max":"300"}
rr4 = {"keyword":"sap_calcium","min":"300","max":"800"}
rr21 = {"keyword":"sap_potassium","uid":sap_k,"min":"4000","max":"5000"}
rr10 = {"keyword":"sap_kcaratio","uid":sap_kca,"min":"","max":""}
rr11 = {"keyword":"sap_magnesium","min":"250","max":"500"}
rr24 = {"keyword":"sap_sodium","uid":sap_na,"min":"250","max":"1000"}
rr1 = {"keyword":"sap_aluminum","uid":sap_al,"min":"","max":""}
rr2 = {"keyword":"sap_boron","uid":sap_b,"min":"1","max":"5"}
rr6 = {"keyword":"sap_cobalt","uid":sap_co,"min":"","max":""}
rr7 = {"keyword":"sap_copper","uid":sap_cu,"min":"1","max":"5"}
rr9 = {"keyword":"sap_iron","uid":sap_fe,"min":"1.5","max":"5"}
rr12 = {"keyword":"sap_manganese","uid":sap_mn,"min":"1","max":"5"}
rr13 = {"keyword":"sap_molybdenum","min":"0.5","max":"2"}
rr14 = {"keyword":"sap_nickel","uid":sap_ni,"min":"","max":""}
rr22 = {"keyword":"sap_selenium","uid":sap_se,"min":"","max":""}
rr23 = {"keyword":"sap_silica","uid":sap_si,"min":"5","max":"20"}
rr26 = {"keyword":"sap_zinc","min":"2","max":"5"}
rr16 = {"keyword":"sap_nitrogen_as_ammonium","uid":sap_nnh4,"min":"","max":""}
rr17 = {"keyword":"sap_nitrogen_as_nitrate","uid":sap_nno3,"min":"900","max":"1240"}
rr18 = {"keyword":"sap_total_nitrogen","UID":sap_totaln,"min":"2000","max":"3500"}
rr15 = {"keyword":"sap_nitrate","UID":sap_no3,"min":"4000","max":"5500"}
rr = [rr1,rr2,rr3,rr4,rr5,rr6,rr7,rr8,rr9,rr10,rr11,rr12,rr13,rr14,rr14,rr15,rr16,rr17,rr18,rr19,rr20,rr21,rr22,rr23,rr24,rr25,rr26,rr27]
chard_spec = api.create(specs, "AnalysisSpec", title="Chard Sap", SampleType=saptype, ResultsRange=rr).UID()

##Sugarbeet
rr27 = {"keyword":"sap_total_sugar","uid":sap_sugar,"min":"2","max":"5"}
rr3 = {"keyword":"sap_brix","min":"6","max":"8"}
rr19 = {"keyword":"sap_ph","uid":sap_ph,"min":"6","max":"7"}
rr8 = {"keyword":"sap_ec","uid":sap_ec,"min":"12","max":"15"}
rr5 = {"keyword":"sap_chloride","uid":sap_cl,"min":"1000","max":"3000"}
rr25 = {"keyword":"sap_sulfur","UID":sap_s,"min":"75","max":"250"}
rr20 = {"keyword":"sap_phosphorous","uid":sap_p,"min":"100","max":"350"}
rr4 = {"keyword":"sap_calcium","min":"25","max":"75"}
rr21 = {"keyword":"sap_potassium","uid":sap_k,"min":"3500","max":"4500"}
rr10 = {"keyword":"sap_kcaratio","uid":sap_kca,"min":"","max":""}
rr11 = {"keyword":"sap_magnesium","min":"350","max":"500"}
rr24 = {"keyword":"sap_sodium","uid":sap_na,"min":"100","max":"500"}
rr1 = {"keyword":"sap_aluminum","uid":sap_al,"min":"","max":""}
rr2 = {"keyword":"sap_boron","uid":sap_b,"min":"2","max":"5"}
rr6 = {"keyword":"sap_cobalt","uid":sap_co,"min":"","max":""}
rr7 = {"keyword":"sap_copper","uid":sap_cu,"min":"1.5","max":"5"}
rr9 = {"keyword":"sap_iron","uid":sap_fe,"min":"2","max":"10"}
rr12 = {"keyword":"sap_manganese","uid":sap_mn,"min":"2","max":"10"}
rr13 = {"keyword":"sap_molybdenum","min":"","max":""}
rr14 = {"keyword":"sap_nickel","uid":sap_ni,"min":"","max":""}
rr22 = {"keyword":"sap_selenium","uid":sap_se,"min":"","max":""}
rr23 = {"keyword":"sap_silica","uid":sap_si,"min":"25","max":"75"}
rr26 = {"keyword":"sap_zinc","min":"3","max":"15"}
rr16 = {"keyword":"sap_nitrogen_as_ammonium","uid":sap_nnh4,"min":"","max":""}
rr17 = {"keyword":"sap_nitrogen_as_nitrate","uid":sap_nno3,"min":"900","max":"1130"}
rr18 = {"keyword":"sap_total_nitrogen","UID":sap_totaln,"min":"2500","max":"3500"}
rr15 = {"keyword":"sap_nitrate","UID":sap_no3,"min":"4000","max":"5000"}
rr = [rr1,rr2,rr3,rr4,rr5,rr6,rr7,rr8,rr9,rr10,rr11,rr12,rr13,rr14,rr14,rr15,rr16,rr17,rr18,rr19,rr20,rr21,rr22,rr23,rr24,rr25,rr26,rr27]
sugarbeet_spec = api.create(specs, "AnalysisSpec", title="Sugarbeet Sap", SampleType=saptype, ResultsRange=rr).UID()

##Sorghum - Milo
rr27 = {"keyword":"sap_total_sugar","uid":sap_sugar,"min":"1.5","max":"2"}
rr3 = {"keyword":"sap_brix","min":"4.5","max":"6.5"}
rr19 = {"keyword":"sap_ph","uid":sap_ph,"min":"5.8","max":"6.5"}
rr8 = {"keyword":"sap_ec","uid":sap_ec,"min":"15","max":"18"}
rr5 = {"keyword":"sap_chloride","uid":sap_cl,"min":"1000","max":"2500"}
rr25 = {"keyword":"sap_sulfur","UID":sap_s,"min":"100","max":"200"}
rr20 = {"keyword":"sap_phosphorous","uid":sap_p,"min":"150","max":"250"}
rr4 = {"keyword":"sap_calcium","min":"220","max":"450"}
rr21 = {"keyword":"sap_potassium","uid":sap_k,"min":"4275","max":"5650"}
rr10 = {"keyword":"sap_kcaratio","uid":sap_kca,"min":"","max":""}
rr11 = {"keyword":"sap_magnesium","min":"240","max":"480"}
rr24 = {"keyword":"sap_sodium","uid":sap_na,"min":"10","max":"75"}
rr1 = {"keyword":"sap_aluminum","uid":sap_al,"min":"","max":""}
rr2 = {"keyword":"sap_boron","uid":sap_b,"min":"2.5","max":"9"}
rr6 = {"keyword":"sap_cobalt","uid":sap_co,"min":"","max":""}
rr7 = {"keyword":"sap_copper","uid":sap_cu,"min":"2","max":"10"}
rr9 = {"keyword":"sap_iron","uid":sap_fe,"min":"3","max":"10"}
rr12 = {"keyword":"sap_manganese","uid":sap_mn,"min":"1","max":"5"}
rr13 = {"keyword":"sap_molybdenum","min":"","max":""}
rr14 = {"keyword":"sap_nickel","uid":sap_ni,"min":"","max":""}
rr22 = {"keyword":"sap_selenium","uid":sap_se,"min":"","max":""}
rr23 = {"keyword":"sap_silica","uid":sap_si,"min":"25","max":"100"}
rr26 = {"keyword":"sap_zinc","min":"3","max":"11"}
rr16 = {"keyword":"sap_nitrogen_as_ammonium","uid":sap_nnh4,"min":"","max":""}
rr17 = {"keyword":"sap_nitrogen_as_nitrate","uid":sap_nno3,"min":"270","max":"565"}
rr18 = {"keyword":"sap_total_nitrogen","UID":sap_totaln,"min":"1000","max":"2000"}
rr15 = {"keyword":"sap_nitrate","UID":sap_no3,"min":"1200","max":"2500"}
rr = [rr1,rr2,rr3,rr4,rr5,rr6,rr7,rr8,rr9,rr10,rr11,rr12,rr13,rr14,rr14,rr15,rr16,rr17,rr18,rr19,rr20,rr21,rr22,rr23,rr24,rr25,rr26,rr27]
sorghum_spec = api.create(specs, "AnalysisSpec", title="Sorghum Sap", SampleType=saptype, ResultsRange=rr).UID()

##Cotton
rr27 = {"keyword":"sap_total_sugar","uid":sap_sugar,"min":"1","max":"3"}
rr3 = {"keyword":"sap_brix","min":"7","max":"11"}
rr19 = {"keyword":"sap_ph","uid":sap_ph,"min":"6","max":"6.5"}
rr8 = {"keyword":"sap_ec","uid":sap_ec,"min":"13.5","max":"16.2"}
rr5 = {"keyword":"sap_chloride","uid":sap_cl,"min":"1000","max":"2500"}
rr25 = {"keyword":"sap_sulfur","UID":sap_s,"min":"100","max":"400"}
rr20 = {"keyword":"sap_phosphorous","uid":sap_p,"min":"125","max":"250"}
rr4 = {"keyword":"sap_calcium","min":"1750","max":"3500"}
rr21 = {"keyword":"sap_potassium","uid":sap_k,"min":"4500","max":"7500"}
rr10 = {"keyword":"sap_kcaratio","uid":sap_kca,"min":"","max":""}
rr11 = {"keyword":"sap_magnesium","min":"900","max":"1750"}
rr24 = {"keyword":"sap_sodium","uid":sap_na,"min":"10","max":"75"}
rr1 = {"keyword":"sap_aluminum","uid":sap_al,"min":"","max":""}
rr2 = {"keyword":"sap_boron","uid":sap_b,"min":"1.5","max":"7.5"}
rr6 = {"keyword":"sap_cobalt","uid":sap_co,"min":"","max":""}
rr7 = {"keyword":"sap_copper","uid":sap_cu,"min":"0.8","max":"5"}
rr9 = {"keyword":"sap_iron","uid":sap_fe,"min":"1.5","max":"10"}
rr12 = {"keyword":"sap_manganese","uid":sap_mn,"min":"2","max":"5"}
rr13 = {"keyword":"sap_molybdenum","min":"","max":""}
rr14 = {"keyword":"sap_nickel","uid":sap_ni,"min":"","max":""}
rr22 = {"keyword":"sap_selenium","uid":sap_se,"min":"","max":""}
rr23 = {"keyword":"sap_silica","uid":sap_si,"min":"70","max":"90"}
rr26 = {"keyword":"sap_zinc","min":"1.5","max":"5"}
rr16 = {"keyword":"sap_nitrogen_as_ammonium","uid":sap_nnh4,"min":"","max":""}
rr17 = {"keyword":"sap_nitrogen_as_nitrate","uid":sap_nno3,"min":"2145","max":"2935"}
rr18 = {"keyword":"sap_total_nitrogen","UID":sap_totaln,"min":"3000","max":"6000"}
rr15 = {"keyword":"sap_nitrate","UID":sap_no3,"min":"9500","max":"13000"}
rr = [rr1,rr2,rr3,rr4,rr5,rr6,rr7,rr8,rr9,rr10,rr11,rr12,rr13,rr14,rr14,rr15,rr16,rr17,rr18,rr19,rr20,rr21,rr22,rr23,rr24,rr25,rr26,rr27]
cotton_spec = api.create(specs, "AnalysisSpec", title="Cotton Sap", SampleType=saptype, ResultsRange=rr).UID()

##Cowpeas
rr27 = {"keyword":"sap_total_sugar","uid":sap_sugar,"min":"0.5","max":"1.1"}
rr3 = {"keyword":"sap_brix","min":"6","max":"10"}
rr19 = {"keyword":"sap_ph","uid":sap_ph,"min":"5","max":"7"}
rr8 = {"keyword":"sap_ec","uid":sap_ec,"min":"6","max":"10"}
rr5 = {"keyword":"sap_chloride","uid":sap_cl,"min":"750","max":"1500"}
rr25 = {"keyword":"sap_sulfur","UID":sap_s,"min":"100","max":"300"}
rr20 = {"keyword":"sap_phosphorous","uid":sap_p,"min":"175","max":"350"}
rr4 = {"keyword":"sap_calcium","min":"600","max":"1500"}
rr21 = {"keyword":"sap_potassium","uid":sap_k,"min":"2100","max":"4500"}
rr10 = {"keyword":"sap_kcaratio","uid":sap_kca,"min":"","max":""}
rr11 = {"keyword":"sap_magnesium","min":"250","max":"500"}
rr24 = {"keyword":"sap_sodium","uid":sap_na,"min":"5","max":"50"}
rr1 = {"keyword":"sap_aluminum","uid":sap_al,"min":"","max":""}
rr2 = {"keyword":"sap_boron","uid":sap_b,"min":"2","max":"10"}
rr6 = {"keyword":"sap_cobalt","uid":sap_co,"min":"","max":""}
rr7 = {"keyword":"sap_copper","uid":sap_cu,"min":"1","max":"4"}
rr9 = {"keyword":"sap_iron","uid":sap_fe,"min":"1","max":"5"}
rr12 = {"keyword":"sap_manganese","uid":sap_mn,"min":"4","max":"16"}
rr13 = {"keyword":"sap_molybdenum","min":"1","max":"2"}
rr14 = {"keyword":"sap_nickel","uid":sap_ni,"min":"","max":""}
rr22 = {"keyword":"sap_selenium","uid":sap_se,"min":"","max":""}
rr23 = {"keyword":"sap_silica","uid":sap_si,"min":"35","max":"70"}
rr26 = {"keyword":"sap_zinc","min":"3.5","max":"25"}
rr16 = {"keyword":"sap_nitrogen_as_ammonium","uid":sap_nnh4,"min":"","max":""}
rr17 = {"keyword":"sap_nitrogen_as_nitrate","uid":sap_nno3,"min":"125","max":"250"}
rr18 = {"keyword":"sap_total_nitrogen","UID":sap_totaln,"min":"3000","max":"6000"}
rr15 = {"keyword":"sap_nitrate","UID":sap_no3,"min":"553.75","max":"1107.5"}
rr = [rr1,rr2,rr3,rr4,rr5,rr6,rr7,rr8,rr9,rr10,rr11,rr12,rr13,rr14,rr14,rr15,rr16,rr17,rr18,rr19,rr20,rr21,rr22,rr23,rr24,rr25,rr26,rr27]
cowpeas_spec = api.create(specs, "AnalysisSpec", title="Cowpea Sap", SampleType=saptype, ResultsRange=rr).UID()

##Citrus (Grapefruit)
rr27 = {"keyword":"sap_total_sugar","uid":sap_sugar,"min":"1.5","max":"2"}
rr3 = {"keyword":"sap_brix","min":"2","max":"5"}
rr19 = {"keyword":"sap_ph","uid":sap_ph,"min":"5.8","max":"6.2"}
rr8 = {"keyword":"sap_ec","uid":sap_ec,"min":"2","max":"5"}
rr5 = {"keyword":"sap_chloride","uid":sap_cl,"min":"150","max":"750"}
rr25 = {"keyword":"sap_sulfur","UID":sap_s,"min":"100","max":"500"}
rr20 = {"keyword":"sap_phosphorous","uid":sap_p,"min":"120","max":"300"}
rr4 = {"keyword":"sap_calcium","min":"400","max":"1200"}
rr21 = {"keyword":"sap_potassium","uid":sap_k,"min":"2500","max":"4500"}
rr10 = {"keyword":"sap_kcaratio","uid":sap_kca,"min":"","max":""}
rr11 = {"keyword":"sap_magnesium","min":"250","max":"700"}
rr24 = {"keyword":"sap_sodium","uid":sap_na,"min":"10","max":"75"}
rr1 = {"keyword":"sap_aluminum","uid":sap_al,"min":"","max":""}
rr2 = {"keyword":"sap_boron","uid":sap_b,"min":"2.5","max":"10"}
rr6 = {"keyword":"sap_cobalt","uid":sap_co,"min":"","max":""}
rr7 = {"keyword":"sap_copper","uid":sap_cu,"min":"2","max":"10"}
rr9 = {"keyword":"sap_iron","uid":sap_fe,"min":"2.5","max":"10"}
rr12 = {"keyword":"sap_manganese","uid":sap_mn,"min":"2","max":"10"}
rr13 = {"keyword":"sap_molybdenum","min":"","max":""}
rr14 = {"keyword":"sap_nickel","uid":sap_ni,"min":"","max":""}
rr22 = {"keyword":"sap_selenium","uid":sap_se,"min":"","max":""}
rr23 = {"keyword":"sap_silica","uid":sap_si,"min":"25","max":"75"}
rr26 = {"keyword":"sap_zinc","min":"2.5","max":"10"}
rr16 = {"keyword":"sap_nitrogen_as_ammonium","uid":sap_nnh4,"min":"","max":""}
rr17 = {"keyword":"sap_nitrogen_as_nitrate","uid":sap_nno3,"min":"90","max":"170"}
rr18 = {"keyword":"sap_total_nitrogen","UID":sap_totaln,"min":"500","max":"1500"}
rr15 = {"keyword":"sap_nitrate","UID":sap_no3,"min":"400","max":"750"}
rr = [rr1,rr2,rr3,rr4,rr5,rr6,rr7,rr8,rr9,rr10,rr11,rr12,rr13,rr14,rr14,rr15,rr16,rr17,rr18,rr19,rr20,rr21,rr22,rr23,rr24,rr25,rr26,rr27]
citrus_grapefruit_spec = api.create(specs, "AnalysisSpec", title="Citrus Sap, Grapefruit", SampleType=saptype, ResultsRange=rr).UID()

##Citrus (Lemon)
rr27 = {"keyword":"sap_total_sugar","uid":sap_sugar,"min":"1.5","max":"2"}
rr3 = {"keyword":"sap_brix","min":"2","max":"5"}
rr19 = {"keyword":"sap_ph","uid":sap_ph,"min":"5.8","max":"6.2"}
rr8 = {"keyword":"sap_ec","uid":sap_ec,"min":"2","max":"5"}
rr5 = {"keyword":"sap_chloride","uid":sap_cl,"min":"150","max":"750"}
rr25 = {"keyword":"sap_sulfur","UID":sap_s,"min":"100","max":"500"}
rr20 = {"keyword":"sap_phosphorous","uid":sap_p,"min":"150","max":"300"}
rr4 = {"keyword":"sap_calcium","min":"400","max":"1100"}
rr21 = {"keyword":"sap_potassium","uid":sap_k,"min":"2500","max":"4500"}
rr10 = {"keyword":"sap_kcaratio","uid":sap_kca,"min":"","max":""}
rr11 = {"keyword":"sap_magnesium","min":"250","max":"700"}
rr24 = {"keyword":"sap_sodium","uid":sap_na,"min":"10","max":"75"}
rr1 = {"keyword":"sap_aluminum","uid":sap_al,"min":"","max":""}
rr2 = {"keyword":"sap_boron","uid":sap_b,"min":"5","max":"15"}
rr6 = {"keyword":"sap_cobalt","uid":sap_co,"min":"","max":""}
rr7 = {"keyword":"sap_copper","uid":sap_cu,"min":"5","max":"20"}
rr9 = {"keyword":"sap_iron","uid":sap_fe,"min":"3","max":"15"}
rr12 = {"keyword":"sap_manganese","uid":sap_mn,"min":"2.5","max":"10"}
rr13 = {"keyword":"sap_molybdenum","min":"","max":""}
rr14 = {"keyword":"sap_nickel","uid":sap_ni,"min":"","max":""}
rr22 = {"keyword":"sap_selenium","uid":sap_se,"min":"","max":""}
rr23 = {"keyword":"sap_silica","uid":sap_si,"min":"25","max":"75"}
rr26 = {"keyword":"sap_zinc","min":"3","max":"12"}
rr16 = {"keyword":"sap_nitrogen_as_ammonium","uid":sap_nnh4,"min":"","max":""}
rr17 = {"keyword":"sap_nitrogen_as_nitrate","uid":sap_nno3,"min":"90","max":"170"}
rr18 = {"keyword":"sap_total_nitrogen","UID":sap_totaln,"min":"500","max":"1500"}
rr15 = {"keyword":"sap_nitrate","UID":sap_no3,"min":"400","max":"750"}
rr = [rr1,rr2,rr3,rr4,rr5,rr6,rr7,rr8,rr9,rr10,rr11,rr12,rr13,rr14,rr14,rr15,rr16,rr17,rr18,rr19,rr20,rr21,rr22,rr23,rr24,rr25,rr26,rr27]
citrus_lemon_spec = api.create(specs, "AnalysisSpec", title="Citrus Sap, Lemon", SampleType=saptype, ResultsRange=rr).UID()

##Citrus (Mandarin)
rr27 = {"keyword":"sap_total_sugar","uid":sap_sugar,"min":"1.2","max":"2"}
rr3 = {"keyword":"sap_brix","min":"2","max":"5"}
rr19 = {"keyword":"sap_ph","uid":sap_ph,"min":"5.8","max":"6.2"}
rr8 = {"keyword":"sap_ec","uid":sap_ec,"min":"2","max":"5"}
rr5 = {"keyword":"sap_chloride","uid":sap_cl,"min":"150","max":"750"}
rr25 = {"keyword":"sap_sulfur","UID":sap_s,"min":"100","max":"500"}
rr20 = {"keyword":"sap_phosphorous","uid":sap_p,"min":"150","max":"250"}
rr4 = {"keyword":"sap_calcium","min":"1200","max":"2500"}
rr21 = {"keyword":"sap_potassium","uid":sap_k,"min":"3000","max":"4800"}
rr10 = {"keyword":"sap_kcaratio","uid":sap_kca,"min":"","max":""}
rr11 = {"keyword":"sap_magnesium","min":"450","max":"1200"}
rr24 = {"keyword":"sap_sodium","uid":sap_na,"min":"10","max":"75"}
rr1 = {"keyword":"sap_aluminum","uid":sap_al,"min":"0.1","max":"0.2"}
rr2 = {"keyword":"sap_boron","uid":sap_b,"min":"8","max":"20"}
rr6 = {"keyword":"sap_cobalt","uid":sap_co,"min":"0.1","max":"0.15"}
rr7 = {"keyword":"sap_copper","uid":sap_cu,"min":"2","max":"20"}
rr9 = {"keyword":"sap_iron","uid":sap_fe,"min":"2.5","max":"10"}
rr12 = {"keyword":"sap_manganese","uid":sap_mn,"min":"3","max":"15"}
rr13 = {"keyword":"sap_molybdenum","min":"0.03","max":"0.05"}
rr14 = {"keyword":"sap_nickel","uid":sap_ni,"min":"","max":""}
rr22 = {"keyword":"sap_selenium","uid":sap_se,"min":"","max":""}
rr23 = {"keyword":"sap_silica","uid":sap_si,"min":"25","max":"75"}
rr26 = {"keyword":"sap_zinc","min":"5","max":"15"}
rr16 = {"keyword":"sap_nitrogen_as_ammonium","uid":sap_nnh4,"min":"12","max":"15"}
rr17 = {"keyword":"sap_nitrogen_as_nitrate","uid":sap_nno3,"min":"90","max":"180"}
rr18 = {"keyword":"sap_total_nitrogen","UID":sap_totaln,"min":"500","max":"1500"}
rr15 = {"keyword":"sap_nitrate","UID":sap_no3,"min":"400","max":"800"}
rr = [rr1,rr2,rr3,rr4,rr5,rr6,rr7,rr8,rr9,rr10,rr11,rr12,rr13,rr14,rr14,rr15,rr16,rr17,rr18,rr19,rr20,rr21,rr22,rr23,rr24,rr25,rr26,rr27]
citrus_mandarin_spec = api.create(specs, "AnalysisSpec", title="Citrus Sap, Mandarin", SampleType=saptype, ResultsRange=rr).UID()

##Citrus (Navel)
rr27 = {"keyword":"sap_total_sugar","uid":sap_sugar,"min":"1.5","max":"2"}
rr3 = {"keyword":"sap_brix","min":"1.5","max":"5"}
rr19 = {"keyword":"sap_ph","uid":sap_ph,"min":"6","max":"6.5"}
rr8 = {"keyword":"sap_ec","uid":sap_ec,"min":"1.3","max":"1.8"}
rr5 = {"keyword":"sap_chloride","uid":sap_cl,"min":"500","max":"1000"}
rr25 = {"keyword":"sap_sulfur","UID":sap_s,"min":"100","max":"500"}
rr20 = {"keyword":"sap_phosphorous","uid":sap_p,"min":"120","max":"300"}
rr4 = {"keyword":"sap_calcium","min":"1000","max":"3000"}
rr21 = {"keyword":"sap_potassium","uid":sap_k,"min":"3000","max":"5000"}
rr10 = {"keyword":"sap_kcaratio","uid":sap_kca,"min":"","max":""}
rr11 = {"keyword":"sap_magnesium","min":"300","max":"800"}
rr24 = {"keyword":"sap_sodium","uid":sap_na,"min":"50","max":"250"}
rr1 = {"keyword":"sap_aluminum","uid":sap_al,"min":"","max":""}
rr2 = {"keyword":"sap_boron","uid":sap_b,"min":"7","max":"15"}
rr6 = {"keyword":"sap_cobalt","uid":sap_co,"min":"","max":""}
rr7 = {"keyword":"sap_copper","uid":sap_cu,"min":"4","max":"25"}
rr9 = {"keyword":"sap_iron","uid":sap_fe,"min":"5","max":"12"}
rr12 = {"keyword":"sap_manganese","uid":sap_mn,"min":"3","max":"10"}
rr13 = {"keyword":"sap_molybdenum","min":"","max":""}
rr14 = {"keyword":"sap_nickel","uid":sap_ni,"min":"","max":""}
rr22 = {"keyword":"sap_selenium","uid":sap_se,"min":"","max":""}
rr23 = {"keyword":"sap_silica","uid":sap_si,"min":"25","max":"50"}
rr26 = {"keyword":"sap_zinc","min":"3","max":"10"}
rr16 = {"keyword":"sap_nitrogen_as_ammonium","uid":sap_nnh4,"min":"","max":""}
rr17 = {"keyword":"sap_nitrogen_as_nitrate","uid":sap_nno3,"min":"70","max":"135"}
rr18 = {"keyword":"sap_total_nitrogen","UID":sap_totaln,"min":"500","max":"1500"}
rr15 = {"keyword":"sap_nitrate","UID":sap_no3,"min":"300","max":"600"}
rr = [rr1,rr2,rr3,rr4,rr5,rr6,rr7,rr8,rr9,rr10,rr11,rr12,rr13,rr14,rr14,rr15,rr16,rr17,rr18,rr19,rr20,rr21,rr22,rr23,rr24,rr25,rr26,rr27]
citrus_navel_spec = api.create(specs, "AnalysisSpec", title="Citrus Sap, Navel", SampleType=saptype, ResultsRange=rr).UID()

##Corn V3
rr27 = {"keyword":"sap_total_sugar","uid":sap_sugar,"min":"1.5","max":"2"}
rr3 = {"keyword":"sap_brix","min":"4.5","max":"6.5"}
rr19 = {"keyword":"sap_ph","uid":sap_ph,"min":"5.8","max":"6.5"}
rr8 = {"keyword":"sap_ec","uid":sap_ec,"min":"15","max":"18"}
rr5 = {"keyword":"sap_chloride","uid":sap_cl,"min":"1000","max":"2500"}
rr25 = {"keyword":"sap_sulfur","UID":sap_s,"min":"100","max":"400"}
rr20 = {"keyword":"sap_phosphorous","uid":sap_p,"min":"170","max":"370"}
rr4 = {"keyword":"sap_calcium","min":"220","max":"450"}
rr21 = {"keyword":"sap_potassium","uid":sap_k,"min":"4275","max":"5650"}
rr10 = {"keyword":"sap_kcaratio","uid":sap_kca,"min":"","max":""}
rr11 = {"keyword":"sap_magnesium","min":"240","max":"480"}
rr24 = {"keyword":"sap_sodium","uid":sap_na,"min":"10","max":"75"}
rr1 = {"keyword":"sap_aluminum","uid":sap_al,"min":"","max":""}
rr2 = {"keyword":"sap_boron","uid":sap_b,"min":"2.5","max":"9"}
rr6 = {"keyword":"sap_cobalt","uid":sap_co,"min":"","max":""}
rr7 = {"keyword":"sap_copper","uid":sap_cu,"min":"2","max":"10"}
rr9 = {"keyword":"sap_iron","uid":sap_fe,"min":"3","max":"10"}
rr12 = {"keyword":"sap_manganese","uid":sap_mn,"min":"1","max":"5"}
rr13 = {"keyword":"sap_molybdenum","min":"","max":""}
rr14 = {"keyword":"sap_nickel","uid":sap_ni,"min":"","max":""}
rr22 = {"keyword":"sap_selenium","uid":sap_se,"min":"","max":""}
rr23 = {"keyword":"sap_silica","uid":sap_si,"min":"25","max":"100"}
rr26 = {"keyword":"sap_zinc","min":"3","max":"11"}
rr16 = {"keyword":"sap_nitrogen_as_ammonium","uid":sap_nnh4,"min":"","max":""}
rr17 = {"keyword":"sap_nitrogen_as_nitrate","uid":sap_nno3,"min":"810","max":"1470"}
rr18 = {"keyword":"sap_total_nitrogen","UID":sap_totaln,"min":"2000","max":"4000"}
rr15 = {"keyword":"sap_nitrate","UID":sap_no3,"min":"3600","max":"6500"}
rr = [rr1,rr2,rr3,rr4,rr5,rr6,rr7,rr8,rr9,rr10,rr11,rr12,rr13,rr14,rr14,rr15,rr16,rr17,rr18,rr19,rr20,rr21,rr22,rr23,rr24,rr25,rr26,rr27]
corn_v3_spec = api.create(specs, "AnalysisSpec", title="Corn Sap, V3", SampleType=saptype, ResultsRange=rr).UID()

##Corn V6
rr27 = {"keyword":"sap_total_sugar","uid":sap_sugar,"min":"1.5","max":"2"}
rr3 = {"keyword":"sap_brix","min":"4.5","max":"6.5"}
rr19 = {"keyword":"sap_ph","uid":sap_ph,"min":"5.8","max":"6.5"}
rr8 = {"keyword":"sap_ec","uid":sap_ec,"min":"15","max":"18"}
rr5 = {"keyword":"sap_chloride","uid":sap_cl,"min":"1000","max":"2500"}
rr25 = {"keyword":"sap_sulfur","UID":sap_s,"min":"100","max":"400"}
rr20 = {"keyword":"sap_phosphorous","uid":sap_p,"min":"170","max":"370"}
rr4 = {"keyword":"sap_calcium","min":"220","max":"450"}
rr21 = {"keyword":"sap_potassium","uid":sap_k,"min":"4275","max":"5650"}
rr10 = {"keyword":"sap_kcaratio","uid":sap_kca,"min":"","max":""}
rr11 = {"keyword":"sap_magnesium","min":"240","max":"480"}
rr24 = {"keyword":"sap_sodium","uid":sap_na,"min":"10","max":"75"}
rr1 = {"keyword":"sap_aluminum","uid":sap_al,"min":"","max":""}
rr2 = {"keyword":"sap_boron","uid":sap_b,"min":"2.5","max":"9"}
rr6 = {"keyword":"sap_cobalt","uid":sap_co,"min":"","max":""}
rr7 = {"keyword":"sap_copper","uid":sap_cu,"min":"2","max":"10"}
rr9 = {"keyword":"sap_iron","uid":sap_fe,"min":"3","max":"10"}
rr12 = {"keyword":"sap_manganese","uid":sap_mn,"min":"1","max":"5"}
rr13 = {"keyword":"sap_molybdenum","min":"","max":""}
rr14 = {"keyword":"sap_nickel","uid":sap_ni,"min":"","max":""}
rr22 = {"keyword":"sap_selenium","uid":sap_se,"min":"","max":""}
rr23 = {"keyword":"sap_silica","uid":sap_si,"min":"25","max":"100"}
rr26 = {"keyword":"sap_zinc","min":"3","max":"11"}
rr16 = {"keyword":"sap_nitrogen_as_ammonium","uid":sap_nnh4,"min":"","max":""}
rr17 = {"keyword":"sap_nitrogen_as_nitrate","uid":sap_nno3,"min":"810","max":"1470"}
rr18 = {"keyword":"sap_total_nitrogen","UID":sap_totaln,"min":"2000","max":"4000"}
rr15 = {"keyword":"sap_nitrate","UID":sap_no3,"min":"3600","max":"6500"}
rr = [rr1,rr2,rr3,rr4,rr5,rr6,rr7,rr8,rr9,rr10,rr11,rr12,rr13,rr14,rr14,rr15,rr16,rr17,rr18,rr19,rr20,rr21,rr22,rr23,rr24,rr25,rr26,rr27]
corn_v6_spec = api.create(specs, "AnalysisSpec", title="Corn Sap, V6", SampleType=saptype, ResultsRange=rr).UID()

##Eggplant
rr27 = {"keyword":"sap_total_sugar","uid":sap_sugar,"min":"1","max":"3"}
rr3 = {"keyword":"sap_brix","min":"5","max":"8"}
rr19 = {"keyword":"sap_ph","uid":sap_ph,"min":"5.5","max":"6"}
rr8 = {"keyword":"sap_ec","uid":sap_ec,"min":"15","max":"18"}
rr5 = {"keyword":"sap_chloride","uid":sap_cl,"min":"1000","max":"4000"}
rr25 = {"keyword":"sap_sulfur","UID":sap_s,"min":"100","max":"400"}
rr20 = {"keyword":"sap_phosphorous","uid":sap_p,"min":"100","max":"300"}
rr4 = {"keyword":"sap_calcium","min":"350","max":"750"}
rr21 = {"keyword":"sap_potassium","uid":sap_k,"min":"5000","max":"7500"}
rr10 = {"keyword":"sap_kcaratio","uid":sap_kca,"min":"","max":""}
rr11 = {"keyword":"sap_magnesium","min":"350","max":"700"}
rr24 = {"keyword":"sap_sodium","uid":sap_na,"min":"50","max":"300"}
rr1 = {"keyword":"sap_aluminum","uid":sap_al,"min":"","max":""}
rr2 = {"keyword":"sap_boron","uid":sap_b,"min":"3","max":"10"}
rr6 = {"keyword":"sap_cobalt","uid":sap_co,"min":"","max":""}
rr7 = {"keyword":"sap_copper","uid":sap_cu,"min":"1.3","max":"10"}
rr9 = {"keyword":"sap_iron","uid":sap_fe,"min":"2","max":"10"}
rr12 = {"keyword":"sap_manganese","uid":sap_mn,"min":"2","max":"15"}
rr13 = {"keyword":"sap_molybdenum","min":"","max":""}
rr14 = {"keyword":"sap_nickel","uid":sap_ni,"min":"","max":""}
rr22 = {"keyword":"sap_selenium","uid":sap_se,"min":"","max":""}
rr23 = {"keyword":"sap_silica","uid":sap_si,"min":"5","max":"35"}
rr26 = {"keyword":"sap_zinc","min":"2.5","max":"7.5"}
rr16 = {"keyword":"sap_nitrogen_as_ammonium","uid":sap_nnh4,"min":"","max":""}
rr17 = {"keyword":"sap_nitrogen_as_nitrate","uid":sap_nno3,"min":"670","max":"1130"}
rr18 = {"keyword":"sap_total_nitrogen","UID":sap_totaln,"min":"2000","max":"3500"}
rr15 = {"keyword":"sap_nitrate","UID":sap_no3,"min":"3000","max":"5000"}
rr = [rr1,rr2,rr3,rr4,rr5,rr6,rr7,rr8,rr9,rr10,rr11,rr12,rr13,rr14,rr14,rr15,rr16,rr17,rr18,rr19,rr20,rr21,rr22,rr23,rr24,rr25,rr26,rr27]
eggplant_spec = api.create(specs, "AnalysisSpec", title="Eggplant Sap", SampleType=saptype, ResultsRange=rr).UID()

##Grape (Table)
rr27 = {"keyword":"sap_total_sugar","uid":sap_sugar,"min":"6","max":"15"}
rr3 = {"keyword":"sap_brix","min":"","max":""}
rr19 = {"keyword":"sap_ph","uid":sap_ph,"min":"4","max":"4.5"}
rr8 = {"keyword":"sap_ec","uid":sap_ec,"min":"2","max":"4"}
rr5 = {"keyword":"sap_chloride","uid":sap_cl,"min":"100","max":"650"}
rr25 = {"keyword":"sap_sulfur","UID":sap_s,"min":"80","max":"300"}
rr20 = {"keyword":"sap_phosphorous","uid":sap_p,"min":"200","max":"500"}
rr4 = {"keyword":"sap_calcium","min":"450","max":"900"}
rr21 = {"keyword":"sap_potassium","uid":sap_k,"min":"3000","max":"5000"}
rr10 = {"keyword":"sap_kcaratio","uid":sap_kca,"min":"","max":""}
rr11 = {"keyword":"sap_magnesium","min":"250","max":"600"}
rr24 = {"keyword":"sap_sodium","uid":sap_na,"min":"15","max":"150"}
rr1 = {"keyword":"sap_aluminum","uid":sap_al,"min":"","max":""}
rr2 = {"keyword":"sap_boron","uid":sap_b,"min":"2","max":"10"}
rr6 = {"keyword":"sap_cobalt","uid":sap_co,"min":"","max":""}
rr7 = {"keyword":"sap_copper","uid":sap_cu,"min":"2","max":"10"}
rr9 = {"keyword":"sap_iron","uid":sap_fe,"min":"2","max":"10"}
rr12 = {"keyword":"sap_manganese","uid":sap_mn,"min":"5","max":"20"}
rr13 = {"keyword":"sap_molybdenum","min":"0.2","max":"0.3"}
rr14 = {"keyword":"sap_nickel","uid":sap_ni,"min":"","max":""}
rr22 = {"keyword":"sap_selenium","uid":sap_se,"min":"","max":""}
rr23 = {"keyword":"sap_silica","uid":sap_si,"min":"10","max":"40"}
rr26 = {"keyword":"sap_zinc","min":"5","max":"15"}
rr16 = {"keyword":"sap_nitrogen_as_ammonium","uid":sap_nnh4,"min":"","max":""}
rr17 = {"keyword":"sap_nitrogen_as_nitrate","uid":sap_nno3,"min":"135","max":"340"}
rr18 = {"keyword":"sap_total_nitrogen","UID":sap_totaln,"min":"48","max":"142"}
rr15 = {"keyword":"sap_nitrate","UID":sap_no3,"min":"600","max":"1500"}
rr = [rr1,rr2,rr3,rr4,rr5,rr6,rr7,rr8,rr9,rr10,rr11,rr12,rr13,rr14,rr14,rr15,rr16,rr17,rr18,rr19,rr20,rr21,rr22,rr23,rr24,rr25,rr26,rr27]
grape_table_spec = api.create(specs, "AnalysisSpec", title="Grape (Table) Sap", SampleType=saptype, ResultsRange=rr).UID()

##Grape (Wine) Post-Harvest
rr27 = {"keyword":"sap_total_sugar","uid":sap_sugar,"min":"6","max":"15"}
rr3 = {"keyword":"sap_brix","min":"4","max":"12"}
rr19 = {"keyword":"sap_ph","uid":sap_ph,"min":"4","max":"4.5"}
rr8 = {"keyword":"sap_ec","uid":sap_ec,"min":"2.5","max":"4.5"}
rr5 = {"keyword":"sap_chloride","uid":sap_cl,"min":"100","max":"650"}
rr25 = {"keyword":"sap_sulfur","UID":sap_s,"min":"100","max":"300"}
rr20 = {"keyword":"sap_phosphorous","uid":sap_p,"min":"100","max":"250"}
rr4 = {"keyword":"sap_calcium","min":"700","max":"2000"}
rr21 = {"keyword":"sap_potassium","uid":sap_k,"min":"2500","max":"4000"}
rr10 = {"keyword":"sap_kcaratio","uid":sap_kca,"min":"","max":""}
rr11 = {"keyword":"sap_magnesium","min":"700","max":"2000"}
rr24 = {"keyword":"sap_sodium","uid":sap_na,"min":"15","max":"150"}
rr1 = {"keyword":"sap_aluminum","uid":sap_al,"min":"","max":""}
rr2 = {"keyword":"sap_boron","uid":sap_b,"min":"3","max":"10"}
rr6 = {"keyword":"sap_cobalt","uid":sap_co,"min":"","max":""}
rr7 = {"keyword":"sap_copper","uid":sap_cu,"min":"2","max":"20"}
rr9 = {"keyword":"sap_iron","uid":sap_fe,"min":"3","max":"10"}
rr12 = {"keyword":"sap_manganese","uid":sap_mn,"min":"10","max":"50"}
rr13 = {"keyword":"sap_molybdenum","min":"0.2","max":"0.3"}
rr14 = {"keyword":"sap_nickel","uid":sap_ni,"min":"","max":""}
rr22 = {"keyword":"sap_selenium","uid":sap_se,"min":"","max":""}
rr23 = {"keyword":"sap_silica","uid":sap_si,"min":"10","max":"40"}
rr26 = {"keyword":"sap_zinc","min":"10","max":"20"}
rr16 = {"keyword":"sap_nitrogen_as_ammonium","uid":sap_nnh4,"min":"","max":""}
rr17 = {"keyword":"sap_nitrogen_as_nitrate","uid":sap_nno3,"min":"45","max":"135"}
rr18 = {"keyword":"sap_total_nitrogen","UID":sap_totaln,"min":"300","max":"900"}
rr15 = {"keyword":"sap_nitrate","UID":sap_no3,"min":"200","max":"600"}
rr = [rr1,rr2,rr3,rr4,rr5,rr6,rr7,rr8,rr9,rr10,rr11,rr12,rr13,rr14,rr14,rr15,rr16,rr17,rr18,rr19,rr20,rr21,rr22,rr23,rr24,rr25,rr26,rr27]
grape_wine_postharvest_spec = api.create(specs, "AnalysisSpec", title="Grape (Wine) Sap, Post-Harvest", SampleType=saptype, ResultsRange=rr).UID()

##Grape (Wine)
rr27 = {"keyword":"sap_total_sugar","uid":sap_sugar,"min":"6","max":"15"}
rr3 = {"keyword":"sap_brix","min":"","max":""}
rr19 = {"keyword":"sap_ph","uid":sap_ph,"min":"4","max":"4.5"}
rr8 = {"keyword":"sap_ec","uid":sap_ec,"min":"2.5","max":"4.5"}
rr5 = {"keyword":"sap_chloride","uid":sap_cl,"min":"100","max":"650"}
rr25 = {"keyword":"sap_sulfur","UID":sap_s,"min":"100","max":"300"}
rr20 = {"keyword":"sap_phosphorous","uid":sap_p,"min":"200","max":"500"}
rr4 = {"keyword":"sap_calcium","min":"300","max":"500"}
rr21 = {"keyword":"sap_potassium","uid":sap_k,"min":"1900","max":"2100"}
rr10 = {"keyword":"sap_kcaratio","uid":sap_kca,"min":"","max":""}
rr11 = {"keyword":"sap_magnesium","min":"250","max":"500"}
rr24 = {"keyword":"sap_sodium","uid":sap_na,"min":"15","max":"150"}
rr1 = {"keyword":"sap_aluminum","uid":sap_al,"min":"","max":""}
rr2 = {"keyword":"sap_boron","uid":sap_b,"min":"3","max":"10"}
rr6 = {"keyword":"sap_cobalt","uid":sap_co,"min":"","max":""}
rr7 = {"keyword":"sap_copper","uid":sap_cu,"min":"2","max":"20"}
rr9 = {"keyword":"sap_iron","uid":sap_fe,"min":"3","max":"10"}
rr12 = {"keyword":"sap_manganese","uid":sap_mn,"min":"5","max":"15"}
rr13 = {"keyword":"sap_molybdenum","min":"0.2","max":"0.3"}
rr14 = {"keyword":"sap_nickel","uid":sap_ni,"min":"","max":""}
rr22 = {"keyword":"sap_selenium","uid":sap_se,"min":"","max":""}
rr23 = {"keyword":"sap_silica","uid":sap_si,"min":"10","max":"40"}
rr26 = {"keyword":"sap_zinc","min":"5","max":"10"}
rr16 = {"keyword":"sap_nitrogen_as_ammonium","uid":sap_nnh4,"min":"","max":""}
rr17 = {"keyword":"sap_nitrogen_as_nitrate","uid":sap_nno3,"min":"70","max":"300"}
rr18 = {"keyword":"sap_total_nitrogen","UID":sap_totaln,"min":"48","max":"142"}
rr15 = {"keyword":"sap_nitrate","UID":sap_no3,"min":"300","max":"1350"}
rr = [rr1,rr2,rr3,rr4,rr5,rr6,rr7,rr8,rr9,rr10,rr11,rr12,rr13,rr14,rr14,rr15,rr16,rr17,rr18,rr19,rr20,rr21,rr22,rr23,rr24,rr25,rr26,rr27]
grape_wine_spec = api.create(specs, "AnalysisSpec", title="Grape (Wine) Sap", SampleType=saptype, ResultsRange=rr).UID()

##Lettuce Pre-Early Harvest
rr27 = {"keyword":"sap_total_sugar","uid":sap_sugar,"min":"1","max":"3"}
rr3 = {"keyword":"sap_brix","min":"4","max":"6"}
rr19 = {"keyword":"sap_ph","uid":sap_ph,"min":"5.5","max":"6.5"}
rr8 = {"keyword":"sap_ec","uid":sap_ec,"min":"8","max":"10"}
rr5 = {"keyword":"sap_chloride","uid":sap_cl,"min":"500","max":"2000"}
rr25 = {"keyword":"sap_sulfur","UID":sap_s,"min":"50","max":"200"}
rr20 = {"keyword":"sap_phosphorous","uid":sap_p,"min":"100","max":"200"}
rr4 = {"keyword":"sap_calcium","min":"150","max":"400"}
rr21 = {"keyword":"sap_potassium","uid":sap_k,"min":"2300","max":"4500"}
rr10 = {"keyword":"sap_kcaratio","uid":sap_kca,"min":"","max":""}
rr11 = {"keyword":"sap_magnesium","min":"120","max":"300"}
rr24 = {"keyword":"sap_sodium","uid":sap_na,"min":"20","max":"120"}
rr1 = {"keyword":"sap_aluminum","uid":sap_al,"min":"","max":""}
rr2 = {"keyword":"sap_boron","uid":sap_b,"min":"0.8","max":"5"}
rr6 = {"keyword":"sap_cobalt","uid":sap_co,"min":"","max":""}
rr7 = {"keyword":"sap_copper","uid":sap_cu,"min":"1","max":"8"}
rr9 = {"keyword":"sap_iron","uid":sap_fe,"min":"1","max":"8"}
rr12 = {"keyword":"sap_manganese","uid":sap_mn,"min":"0.8","max":"5"}
rr13 = {"keyword":"sap_molybdenum","min":"","max":""}
rr14 = {"keyword":"sap_nickel","uid":sap_ni,"min":"","max":""}
rr22 = {"keyword":"sap_selenium","uid":sap_se,"min":"","max":""}
rr23 = {"keyword":"sap_silica","uid":sap_si,"min":"5","max":"25"}
rr26 = {"keyword":"sap_zinc","min":"1.2","max":"8"}
rr16 = {"keyword":"sap_nitrogen_as_ammonium","uid":sap_nnh4,"min":"","max":""}
rr17 = {"keyword":"sap_nitrogen_as_nitrate","uid":sap_nno3,"min":"340","max":"565"}
rr18 = {"keyword":"sap_total_nitrogen","UID":sap_totaln,"min":"1000","max":"2500"}
rr15 = {"keyword":"sap_nitrate","UID":sap_no3,"min":"1500","max":"2500"}
rr = [rr1,rr2,rr3,rr4,rr5,rr6,rr7,rr8,rr9,rr10,rr11,rr12,rr13,rr14,rr14,rr15,rr16,rr17,rr18,rr19,rr20,rr21,rr22,rr23,rr24,rr25,rr26,rr27]
lettuce_preearly_harvest_spec = api.create(specs, "AnalysisSpec", title="Lettuce Sap, Pre-Early Harvest", SampleType=saptype, ResultsRange=rr).UID()

##Nectarine
rr27 = {"keyword":"sap_total_sugar","uid":sap_sugar,"min":"1.5","max":"2"}
rr3 = {"keyword":"sap_brix","min":"3.5","max":"5"}
rr19 = {"keyword":"sap_ph","uid":sap_ph,"min":"5.5","max":"6"}
rr8 = {"keyword":"sap_ec","uid":sap_ec,"min":"1","max":"2.5"}
rr5 = {"keyword":"sap_chloride","uid":sap_cl,"min":"350","max":"1500"}
rr25 = {"keyword":"sap_sulfur","UID":sap_s,"min":"100","max":"300"}
rr20 = {"keyword":"sap_phosphorous","uid":sap_p,"min":"120","max":"300"}
rr4 = {"keyword":"sap_calcium","min":"100","max":"150"}
rr21 = {"keyword":"sap_potassium","uid":sap_k,"min":"3800","max":"5000"}
rr10 = {"keyword":"sap_kcaratio","uid":sap_kca,"min":"","max":""}
rr11 = {"keyword":"sap_magnesium","min":"500","max":"650"}
rr24 = {"keyword":"sap_sodium","uid":sap_na,"min":"25","max":"100"}
rr1 = {"keyword":"sap_aluminum","uid":sap_al,"min":"","max":""}
rr2 = {"keyword":"sap_boron","uid":sap_b,"min":"4","max":"10"}
rr6 = {"keyword":"sap_cobalt","uid":sap_co,"min":"","max":""}
rr7 = {"keyword":"sap_copper","uid":sap_cu,"min":"2","max":"10"}
rr9 = {"keyword":"sap_iron","uid":sap_fe,"min":"4","max":"10"}
rr12 = {"keyword":"sap_manganese","uid":sap_mn,"min":"10","max":"25"}
rr13 = {"keyword":"sap_molybdenum","min":"0.5","max":"2.5"}
rr14 = {"keyword":"sap_nickel","uid":sap_ni,"min":"","max":""}
rr22 = {"keyword":"sap_selenium","uid":sap_se,"min":"","max":""}
rr23 = {"keyword":"sap_silica","uid":sap_si,"min":"20","max":"60"}
rr26 = {"keyword":"sap_zinc","min":"3","max":"10"}
rr16 = {"keyword":"sap_nitrogen_as_ammonium","uid":sap_nnh4,"min":"","max":""}
rr17 = {"keyword":"sap_nitrogen_as_nitrate","uid":sap_nno3,"min":"56","max":"80"}
rr18 = {"keyword":"sap_total_nitrogen","UID":sap_totaln,"min":"","max":""}
rr15 = {"keyword":"sap_nitrate","UID":sap_no3,"min":"250","max":"350"}
rr = [rr1,rr2,rr3,rr4,rr5,rr6,rr7,rr8,rr9,rr10,rr11,rr12,rr13,rr14,rr14,rr15,rr16,rr17,rr18,rr19,rr20,rr21,rr22,rr23,rr24,rr25,rr26,rr27]
nectarine_spec = api.create(specs, "AnalysisSpec", title="Nectarine Sap", SampleType=saptype, ResultsRange=rr).UID()

##Oat
rr27 = {"keyword":"sap_total_sugar","uid":sap_sugar,"min":"1.5","max":"2"}
rr3 = {"keyword":"sap_brix","min":"7","max":"10"}
rr19 = {"keyword":"sap_ph","uid":sap_ph,"min":"5.3","max":"6.3"}
rr8 = {"keyword":"sap_ec","uid":sap_ec,"min":"10.5","max":"14"}
rr5 = {"keyword":"sap_chloride","uid":sap_cl,"min":"1000","max":"6000"}
rr25 = {"keyword":"sap_sulfur","UID":sap_s,"min":"200","max":"600"}
rr20 = {"keyword":"sap_phosphorous","uid":sap_p,"min":"200","max":"400"}
rr4 = {"keyword":"sap_calcium","min":"200","max":"650"}
rr21 = {"keyword":"sap_potassium","uid":sap_k,"min":"4500","max":"6500"}
rr10 = {"keyword":"sap_kcaratio","uid":sap_kca,"min":"","max":""}
rr11 = {"keyword":"sap_magnesium","min":"200","max":"450"}
rr24 = {"keyword":"sap_sodium","uid":sap_na,"min":"25","max":"100"}
rr1 = {"keyword":"sap_aluminum","uid":sap_al,"min":"","max":""}
rr2 = {"keyword":"sap_boron","uid":sap_b,"min":"2","max":"10"}
rr6 = {"keyword":"sap_cobalt","uid":sap_co,"min":"","max":""}
rr7 = {"keyword":"sap_copper","uid":sap_cu,"min":"2","max":"10"}
rr9 = {"keyword":"sap_iron","uid":sap_fe,"min":"5","max":"15"}
rr12 = {"keyword":"sap_manganese","uid":sap_mn,"min":"5","max":"15"}
rr13 = {"keyword":"sap_molybdenum","min":"","max":""}
rr14 = {"keyword":"sap_nickel","uid":sap_ni,"min":"","max":""}
rr22 = {"keyword":"sap_selenium","uid":sap_se,"min":"","max":""}
rr23 = {"keyword":"sap_silica","uid":sap_si,"min":"20","max":"60"}
rr26 = {"keyword":"sap_zinc","min":"2","max":"10"}
rr16 = {"keyword":"sap_nitrogen_as_ammonium","uid":sap_nnh4,"min":"","max":""}
rr17 = {"keyword":"sap_nitrogen_as_nitrate","uid":sap_nno3,"min":"180","max":"450"}
rr18 = {"keyword":"sap_total_nitrogen","UID":sap_totaln,"min":"","max":""}
rr15 = {"keyword":"sap_nitrate","UID":sap_no3,"min":"800","max":"2000"}
rr = [rr1,rr2,rr3,rr4,rr5,rr6,rr7,rr8,rr9,rr10,rr11,rr12,rr13,rr14,rr14,rr15,rr16,rr17,rr18,rr19,rr20,rr21,rr22,rr23,rr24,rr25,rr26,rr27]
oat_spec = api.create(specs, "AnalysisSpec", title="Oat Sap", SampleType=saptype, ResultsRange=rr).UID()

##Olive
rr27 = {"keyword":"sap_total_sugar","uid":sap_sugar,"min":"0.5","max":"2"}
rr3 = {"keyword":"sap_brix","min":"1.5","max":"3"}
rr19 = {"keyword":"sap_ph","uid":sap_ph,"min":"5.5","max":"6"}
rr8 = {"keyword":"sap_ec","uid":sap_ec,"min":"3","max":"6"}
rr5 = {"keyword":"sap_chloride","uid":sap_cl,"min":"100","max":"700"}
rr25 = {"keyword":"sap_sulfur","UID":sap_s,"min":"100","max":"300"}
rr20 = {"keyword":"sap_phosphorous","uid":sap_p,"min":"200","max":"400"}
rr4 = {"keyword":"sap_calcium","min":"300","max":"800"}
rr21 = {"keyword":"sap_potassium","uid":sap_k,"min":"4000","max":"6000"}
rr10 = {"keyword":"sap_kcaratio","uid":sap_kca,"min":"","max":""}
rr11 = {"keyword":"sap_magnesium","min":"200","max":"600"}
rr24 = {"keyword":"sap_sodium","uid":sap_na,"min":"100","max":"300"}
rr1 = {"keyword":"sap_aluminum","uid":sap_al,"min":"5","max":"15"}
rr2 = {"keyword":"sap_boron","uid":sap_b,"min":"8","max":"20"}
rr6 = {"keyword":"sap_cobalt","uid":sap_co,"min":"","max":""}
rr7 = {"keyword":"sap_copper","uid":sap_cu,"min":"1","max":"5"}
rr9 = {"keyword":"sap_iron","uid":sap_fe,"min":"1.5","max":"5"}
rr12 = {"keyword":"sap_manganese","uid":sap_mn,"min":"1","max":"5"}
rr13 = {"keyword":"sap_molybdenum","min":"","max":""}
rr14 = {"keyword":"sap_nickel","uid":sap_ni,"min":"","max":""}
rr22 = {"keyword":"sap_selenium","uid":sap_se,"min":"","max":""}
rr23 = {"keyword":"sap_silica","uid":sap_si,"min":"15","max":"50"}
rr26 = {"keyword":"sap_zinc","min":"1","max":"5"}
rr16 = {"keyword":"sap_nitrogen_as_ammonium","uid":sap_nnh4,"min":"10","max":"50"}
rr17 = {"keyword":"sap_nitrogen_as_nitrate","uid":sap_nno3,"min":"35","max":"80"}
rr18 = {"keyword":"sap_total_nitrogen","UID":sap_totaln,"min":"500","max":"1500"}
rr15 = {"keyword":"sap_nitrate","UID":sap_no3,"min":"150","max":"350"}
rr = [rr1,rr2,rr3,rr4,rr5,rr6,rr7,rr8,rr9,rr10,rr11,rr12,rr13,rr14,rr14,rr15,rr16,rr17,rr18,rr19,rr20,rr21,rr22,rr23,rr24,rr25,rr26,rr27]
olive_spec = api.create(specs, "AnalysisSpec", title="Olive Sap", SampleType=saptype, ResultsRange=rr).UID()

##Peach
rr27 = {"keyword":"sap_total_sugar","uid":sap_sugar,"min":"1.5","max":"2"}
rr3 = {"keyword":"sap_brix","min":"3.5","max":"5"}
rr19 = {"keyword":"sap_ph","uid":sap_ph,"min":"5.5","max":"6"}
rr8 = {"keyword":"sap_ec","uid":sap_ec,"min":"1","max":"2.5"}
rr5 = {"keyword":"sap_chloride","uid":sap_cl,"min":"350","max":"1500"}
rr25 = {"keyword":"sap_sulfur","UID":sap_s,"min":"60","max":"120"}
rr20 = {"keyword":"sap_phosphorous","uid":sap_p,"min":"120","max":"300"}
rr4 = {"keyword":"sap_calcium","min":"100","max":"200"}
rr21 = {"keyword":"sap_potassium","uid":sap_k,"min":"3800","max":"5000"}
rr10 = {"keyword":"sap_kcaratio","uid":sap_kca,"min":"","max":""}
rr11 = {"keyword":"sap_magnesium","min":"500","max":"650"}
rr24 = {"keyword":"sap_sodium","uid":sap_na,"min":"25","max":"100"}
rr1 = {"keyword":"sap_aluminum","uid":sap_al,"min":"","max":""}
rr2 = {"keyword":"sap_boron","uid":sap_b,"min":"5","max":"10"}
rr6 = {"keyword":"sap_cobalt","uid":sap_co,"min":"","max":""}
rr7 = {"keyword":"sap_copper","uid":sap_cu,"min":"2","max":"7"}
rr9 = {"keyword":"sap_iron","uid":sap_fe,"min":"4","max":"10"}
rr12 = {"keyword":"sap_manganese","uid":sap_mn,"min":"10","max":"25"}
rr13 = {"keyword":"sap_molybdenum","min":"0.5","max":"2.5"}
rr14 = {"keyword":"sap_nickel","uid":sap_ni,"min":"","max":""}
rr22 = {"keyword":"sap_selenium","uid":sap_se,"min":"","max":""}
rr23 = {"keyword":"sap_silica","uid":sap_si,"min":"20","max":"50"}
rr26 = {"keyword":"sap_zinc","min":"3","max":"6"}
rr16 = {"keyword":"sap_nitrogen_as_ammonium","uid":sap_nnh4,"min":"","max":""}
rr17 = {"keyword":"sap_nitrogen_as_nitrate","uid":sap_nno3,"min":"35","max":"80"}
rr18 = {"keyword":"sap_total_nitrogen","UID":sap_totaln,"min":"","max":""}
rr15 = {"keyword":"sap_nitrate","UID":sap_no3,"min":"150","max":"350"}
rr = [rr1,rr2,rr3,rr4,rr5,rr6,rr7,rr8,rr9,rr10,rr11,rr12,rr13,rr14,rr14,rr15,rr16,rr17,rr18,rr19,rr20,rr21,rr22,rr23,rr24,rr25,rr26,rr27]
peach_spec = api.create(specs, "AnalysisSpec", title="Peach Sap", SampleType=saptype, ResultsRange=rr).UID()

##Peanut
rr27 = {"keyword":"sap_total_sugar","uid":sap_sugar,"min":"1.5","max":"2.5"}
rr3 = {"keyword":"sap_brix","min":"5","max":"7"}
rr19 = {"keyword":"sap_ph","uid":sap_ph,"min":"6","max":"7"}
rr8 = {"keyword":"sap_ec","uid":sap_ec,"min":"9.5","max":"15"}
rr5 = {"keyword":"sap_chloride","uid":sap_cl,"min":"1000","max":"2000"}
rr25 = {"keyword":"sap_sulfur","UID":sap_s,"min":"100","max":"400"}
rr20 = {"keyword":"sap_phosphorous","uid":sap_p,"min":"175","max":"550"}
rr4 = {"keyword":"sap_calcium","min":"1000","max":"5000"}
rr21 = {"keyword":"sap_potassium","uid":sap_k,"min":"3500","max":"5500"}
rr10 = {"keyword":"sap_kcaratio","uid":sap_kca,"min":"","max":""}
rr11 = {"keyword":"sap_magnesium","min":"1000","max":"1800"}
rr24 = {"keyword":"sap_sodium","uid":sap_na,"min":"20","max":"50"}
rr1 = {"keyword":"sap_aluminum","uid":sap_al,"min":"","max":""}
rr2 = {"keyword":"sap_boron","uid":sap_b,"min":"2","max":"10"}
rr6 = {"keyword":"sap_cobalt","uid":sap_co,"min":"","max":""}
rr7 = {"keyword":"sap_copper","uid":sap_cu,"min":"1.5","max":"5"}
rr9 = {"keyword":"sap_iron","uid":sap_fe,"min":"5","max":"20"}
rr12 = {"keyword":"sap_manganese","uid":sap_mn,"min":"5","max":"20"}
rr13 = {"keyword":"sap_molybdenum","min":"","max":""}
rr14 = {"keyword":"sap_nickel","uid":sap_ni,"min":"","max":""}
rr22 = {"keyword":"sap_selenium","uid":sap_se,"min":"","max":""}
rr23 = {"keyword":"sap_silica","uid":sap_si,"min":"35","max":"70"}
rr26 = {"keyword":"sap_zinc","min":"5","max":"10"}
rr16 = {"keyword":"sap_nitrogen_as_ammonium","uid":sap_nnh4,"min":"","max":""}
rr17 = {"keyword":"sap_nitrogen_as_nitrate","uid":sap_nno3,"min":"1015","max":"1580"}
rr18 = {"keyword":"sap_total_nitrogen","UID":sap_totaln,"min":"3000","max":"4500"}
rr15 = {"keyword":"sap_nitrate","UID":sap_no3,"min":"4500","max":"7000"}
rr = [rr1,rr2,rr3,rr4,rr5,rr6,rr7,rr8,rr9,rr10,rr11,rr12,rr13,rr14,rr14,rr15,rr16,rr17,rr18,rr19,rr20,rr21,rr22,rr23,rr24,rr25,rr26,rr27]
peanut_spec = api.create(specs, "AnalysisSpec", title="Peanut Sap", SampleType=saptype, ResultsRange=rr).UID()

##Pear
rr27 = {"keyword":"sap_total_sugar","uid":sap_sugar,"min":"6","max":"7"}
rr3 = {"keyword":"sap_brix","min":"","max":""}
rr19 = {"keyword":"sap_ph","uid":sap_ph,"min":"5.8","max":"6.3"}
rr8 = {"keyword":"sap_ec","uid":sap_ec,"min":"10.5","max":"11.5"}
rr5 = {"keyword":"sap_chloride","uid":sap_cl,"min":"500","max":"1400"}
rr25 = {"keyword":"sap_sulfur","UID":sap_s,"min":"70","max":"200"}
rr20 = {"keyword":"sap_phosphorous","uid":sap_p,"min":"120","max":"250"}
rr4 = {"keyword":"sap_calcium","min":"400","max":"600"}
rr21 = {"keyword":"sap_potassium","uid":sap_k,"min":"3500","max":"5000"}
rr10 = {"keyword":"sap_kcaratio","uid":sap_kca,"min":"","max":""}
rr11 = {"keyword":"sap_magnesium","min":"400","max":"600"}
rr24 = {"keyword":"sap_sodium","uid":sap_na,"min":"10","max":"100"}
rr1 = {"keyword":"sap_aluminum","uid":sap_al,"min":"","max":""}
rr2 = {"keyword":"sap_boron","uid":sap_b,"min":"2","max":"10"}
rr6 = {"keyword":"sap_cobalt","uid":sap_co,"min":"","max":""}
rr7 = {"keyword":"sap_copper","uid":sap_cu,"min":"1","max":"5"}
rr9 = {"keyword":"sap_iron","uid":sap_fe,"min":"2","max":"10"}
rr12 = {"keyword":"sap_manganese","uid":sap_mn,"min":"4","max":"15"}
rr13 = {"keyword":"sap_molybdenum","min":"0.2","max":"0.3"}
rr14 = {"keyword":"sap_nickel","uid":sap_ni,"min":"","max":""}
rr22 = {"keyword":"sap_selenium","uid":sap_se,"min":"","max":""}
rr23 = {"keyword":"sap_silica","uid":sap_si,"min":"25","max":"50"}
rr26 = {"keyword":"sap_zinc","min":"3","max":"10"}
rr16 = {"keyword":"sap_nitrogen_as_ammonium","uid":sap_nnh4,"min":"","max":""}
rr17 = {"keyword":"sap_nitrogen_as_nitrate","uid":sap_nno3,"min":"7","max":"25"}
rr18 = {"keyword":"sap_total_nitrogen","UID":sap_totaln,"min":"100","max":"150"}
rr15 = {"keyword":"sap_nitrate","UID":sap_no3,"min":"31.01","max":"110.75"}
rr = [rr1,rr2,rr3,rr4,rr5,rr6,rr7,rr8,rr9,rr10,rr11,rr12,rr13,rr14,rr14,rr15,rr16,rr17,rr18,rr19,rr20,rr21,rr22,rr23,rr24,rr25,rr26,rr27]
pear_spec = api.create(specs, "AnalysisSpec", title="Pear Sap", SampleType=saptype, ResultsRange=rr).UID()

##Pepper (Determinate)
rr27 = {"keyword":"sap_total_sugar","uid":sap_sugar,"min":"1","max":"3"}
rr3 = {"keyword":"sap_brix","min":"4","max":"8"}
rr19 = {"keyword":"sap_ph","uid":sap_ph,"min":"5.8","max":"6.2"}
rr8 = {"keyword":"sap_ec","uid":sap_ec,"min":"15","max":"18"}
rr5 = {"keyword":"sap_chloride","uid":sap_cl,"min":"500","max":"2000"}
rr25 = {"keyword":"sap_sulfur","UID":sap_s,"min":"300","max":"700"}
rr20 = {"keyword":"sap_phosphorous","uid":sap_p,"min":"100","max":"250"}
rr4 = {"keyword":"sap_calcium","min":"150","max":"400"}
rr21 = {"keyword":"sap_potassium","uid":sap_k,"min":"5000","max":"7500"}
rr10 = {"keyword":"sap_kcaratio","uid":sap_kca,"min":"","max":""}
rr11 = {"keyword":"sap_magnesium","min":"700","max":"1000"}
rr24 = {"keyword":"sap_sodium","uid":sap_na,"min":"15","max":"100"}
rr1 = {"keyword":"sap_aluminum","uid":sap_al,"min":"","max":""}
rr2 = {"keyword":"sap_boron","uid":sap_b,"min":"7","max":"20"}
rr6 = {"keyword":"sap_cobalt","uid":sap_co,"min":"","max":""}
rr7 = {"keyword":"sap_copper","uid":sap_cu,"min":"3","max":"20"}
rr9 = {"keyword":"sap_iron","uid":sap_fe,"min":"2","max":"20"}
rr12 = {"keyword":"sap_manganese","uid":sap_mn,"min":"3","max":"20"}
rr13 = {"keyword":"sap_molybdenum","min":"","max":""}
rr14 = {"keyword":"sap_nickel","uid":sap_ni,"min":"","max":""}
rr22 = {"keyword":"sap_selenium","uid":sap_se,"min":"","max":""}
rr23 = {"keyword":"sap_silica","uid":sap_si,"min":"10","max":"30"}
rr26 = {"keyword":"sap_zinc","min":"5","max":"20"}
rr16 = {"keyword":"sap_nitrogen_as_ammonium","uid":sap_nnh4,"min":"","max":""}
rr17 = {"keyword":"sap_nitrogen_as_nitrate","uid":sap_nno3,"min":"675","max":"1130"}
rr18 = {"keyword":"sap_total_nitrogen","UID":sap_totaln,"min":"2000","max":"3500"}
rr15 = {"keyword":"sap_nitrate","UID":sap_no3,"min":"3000","max":"5000"}
rr = [rr1,rr2,rr3,rr4,rr5,rr6,rr7,rr8,rr9,rr10,rr11,rr12,rr13,rr14,rr14,rr15,rr16,rr17,rr18,rr19,rr20,rr21,rr22,rr23,rr24,rr25,rr26,rr27]
pepper_determinate_spec = api.create(specs, "AnalysisSpec", title="Pepper (Determinate) Sap", SampleType=saptype, ResultsRange=rr).UID()

##Pistachio
rr27 = {"keyword":"sap_total_sugar","uid":sap_sugar,"min":"2.5","max":"4"}
rr3 = {"keyword":"sap_brix","min":"5.6","max":"12"}
rr19 = {"keyword":"sap_ph","uid":sap_ph,"min":"5.5","max":"6"}
rr8 = {"keyword":"sap_ec","uid":sap_ec,"min":"8","max":"10"}
rr5 = {"keyword":"sap_chloride","uid":sap_cl,"min":"350","max":"1500"}
rr25 = {"keyword":"sap_sulfur","UID":sap_s,"min":"50","max":"150"}
rr20 = {"keyword":"sap_phosphorous","uid":sap_p,"min":"125","max":"300"}
rr4 = {"keyword":"sap_calcium","min":"80","max":"200"}
rr21 = {"keyword":"sap_potassium","uid":sap_k,"min":"3500","max":"5000"}
rr10 = {"keyword":"sap_kcaratio","uid":sap_kca,"min":"","max":""}
rr11 = {"keyword":"sap_magnesium","min":"400","max":"1000"}
rr24 = {"keyword":"sap_sodium","uid":sap_na,"min":"25","max":"100"}
rr1 = {"keyword":"sap_aluminum","uid":sap_al,"min":"","max":""}
rr2 = {"keyword":"sap_boron","uid":sap_b,"min":"3","max":"40"}
rr6 = {"keyword":"sap_cobalt","uid":sap_co,"min":"","max":""}
rr7 = {"keyword":"sap_copper","uid":sap_cu,"min":"1","max":"10"}
rr9 = {"keyword":"sap_iron","uid":sap_fe,"min":"2","max":"20"}
rr12 = {"keyword":"sap_manganese","uid":sap_mn,"min":"2.5","max":"20"}
rr13 = {"keyword":"sap_molybdenum","min":"","max":""}
rr14 = {"keyword":"sap_nickel","uid":sap_ni,"min":"","max":""}
rr22 = {"keyword":"sap_selenium","uid":sap_se,"min":"","max":""}
rr23 = {"keyword":"sap_silica","uid":sap_si,"min":"20","max":"60"}
rr26 = {"keyword":"sap_zinc","min":"2","max":"10"}
rr16 = {"keyword":"sap_nitrogen_as_ammonium","uid":sap_nnh4,"min":"","max":""}
rr17 = {"keyword":"sap_nitrogen_as_nitrate","uid":sap_nno3,"min":"11","max":"55"}
rr18 = {"keyword":"sap_total_nitrogen","UID":sap_totaln,"min":"750","max":"1500"}
rr15 = {"keyword":"sap_nitrate","UID":sap_no3,"min":"50","max":"250"}
rr = [rr1,rr2,rr3,rr4,rr5,rr6,rr7,rr8,rr9,rr10,rr11,rr12,rr13,rr14,rr14,rr15,rr16,rr17,rr18,rr19,rr20,rr21,rr22,rr23,rr24,rr25,rr26,rr27]
pistachio_spec = api.create(specs, "AnalysisSpec", title="Pistachio Sap", SampleType=saptype, ResultsRange=rr).UID()

##Plum
rr27 = {"keyword":"sap_total_sugar","uid":sap_sugar,"min":"1.5","max":"2"}
rr3 = {"keyword":"sap_brix","min":"3.5","max":"5"}
rr19 = {"keyword":"sap_ph","uid":sap_ph,"min":"5.5","max":"6"}
rr8 = {"keyword":"sap_ec","uid":sap_ec,"min":"1","max":"2.5"}
rr5 = {"keyword":"sap_chloride","uid":sap_cl,"min":"350","max":"1500"}
rr25 = {"keyword":"sap_sulfur","UID":sap_s,"min":"50","max":"150"}
rr20 = {"keyword":"sap_phosphorous","uid":sap_p,"min":"200","max":"300"}
rr4 = {"keyword":"sap_calcium","min":"30","max":"100"}
rr21 = {"keyword":"sap_potassium","uid":sap_k,"min":"4500","max":"6000"}
rr10 = {"keyword":"sap_kcaratio","uid":sap_kca,"min":"","max":""}
rr11 = {"keyword":"sap_magnesium","min":"300","max":"750"}
rr24 = {"keyword":"sap_sodium","uid":sap_na,"min":"25","max":"100"}
rr1 = {"keyword":"sap_aluminum","uid":sap_al,"min":"","max":""}
rr2 = {"keyword":"sap_boron","uid":sap_b,"min":"3","max":"10"}
rr6 = {"keyword":"sap_cobalt","uid":sap_co,"min":"","max":""}
rr7 = {"keyword":"sap_copper","uid":sap_cu,"min":"1","max":"7"}
rr9 = {"keyword":"sap_iron","uid":sap_fe,"min":"1","max":"10"}
rr12 = {"keyword":"sap_manganese","uid":sap_mn,"min":"3","max":"10"}
rr13 = {"keyword":"sap_molybdenum","min":"0.5","max":"2.5"}
rr14 = {"keyword":"sap_nickel","uid":sap_ni,"min":"","max":""}
rr22 = {"keyword":"sap_selenium","uid":sap_se,"min":"","max":""}
rr23 = {"keyword":"sap_silica","uid":sap_si,"min":"20","max":"50"}
rr26 = {"keyword":"sap_zinc","min":"3","max":"10"}
rr16 = {"keyword":"sap_nitrogen_as_ammonium","uid":sap_nnh4,"min":"","max":""}
rr17 = {"keyword":"sap_nitrogen_as_nitrate","uid":sap_nno3,"min":"35","max":"80"}
rr18 = {"keyword":"sap_total_nitrogen","UID":sap_totaln,"min":"","max":""}
rr15 = {"keyword":"sap_nitrate","UID":sap_no3,"min":"150","max":"350"}
rr = [rr1,rr2,rr3,rr4,rr5,rr6,rr7,rr8,rr9,rr10,rr11,rr12,rr13,rr14,rr14,rr15,rr16,rr17,rr18,rr19,rr20,rr21,rr22,rr23,rr24,rr25,rr26,rr27]
plum_spec = api.create(specs, "AnalysisSpec", title="Plum Sap", SampleType=saptype, ResultsRange=rr).UID()

##Potato
rr27 = {"keyword":"sap_total_sugar","uid":sap_sugar,"min":"1","max":"2.5"}
rr3 = {"keyword":"sap_brix","min":"4.5","max":"7"}
rr19 = {"keyword":"sap_ph","uid":sap_ph,"min":"4.5","max":"6.5"}
rr8 = {"keyword":"sap_ec","uid":sap_ec,"min":"12.5","max":"15"}
rr5 = {"keyword":"sap_chloride","uid":sap_cl,"min":"500","max":"2000"}
rr25 = {"keyword":"sap_sulfur","UID":sap_s,"min":"80","max":"350"}
rr20 = {"keyword":"sap_phosphorous","uid":sap_p,"min":"90","max":"200"}
rr4 = {"keyword":"sap_calcium","min":"300","max":"700"}
rr21 = {"keyword":"sap_potassium","uid":sap_k,"min":"3500","max":"5000"}
rr10 = {"keyword":"sap_kcaratio","uid":sap_kca,"min":"","max":""}
rr11 = {"keyword":"sap_magnesium","min":"250","max":"700"}
rr24 = {"keyword":"sap_sodium","uid":sap_na,"min":"15","max":"50"}
rr1 = {"keyword":"sap_aluminum","uid":sap_al,"min":"","max":""}
rr2 = {"keyword":"sap_boron","uid":sap_b,"min":"1","max":"5"}
rr6 = {"keyword":"sap_cobalt","uid":sap_co,"min":"","max":""}
rr7 = {"keyword":"sap_copper","uid":sap_cu,"min":"1","max":"5"}
rr9 = {"keyword":"sap_iron","uid":sap_fe,"min":"1.5","max":"10"}
rr12 = {"keyword":"sap_manganese","uid":sap_mn,"min":"2","max":"10"}
rr13 = {"keyword":"sap_molybdenum","min":"","max":""}
rr14 = {"keyword":"sap_nickel","uid":sap_ni,"min":"","max":""}
rr22 = {"keyword":"sap_selenium","uid":sap_se,"min":"","max":""}
rr23 = {"keyword":"sap_silica","uid":sap_si,"min":"15","max":"35"}
rr26 = {"keyword":"sap_zinc","min":"2","max":"10"}
rr16 = {"keyword":"sap_nitrogen_as_ammonium","uid":sap_nnh4,"min":"","max":""}
rr17 = {"keyword":"sap_nitrogen_as_nitrate","uid":sap_nno3,"min":"340","max":"790"}
rr18 = {"keyword":"sap_total_nitrogen","UID":sap_totaln,"min":"1000","max":"2500"}
rr15 = {"keyword":"sap_nitrate","UID":sap_no3,"min":"1500","max":"3500"}
rr = [rr1,rr2,rr3,rr4,rr5,rr6,rr7,rr8,rr9,rr10,rr11,rr12,rr13,rr14,rr14,rr15,rr16,rr17,rr18,rr19,rr20,rr21,rr22,rr23,rr24,rr25,rr26,rr27]
potato_spec = api.create(specs, "AnalysisSpec", title="Potato Sap", SampleType=saptype, ResultsRange=rr).UID()

##Pumpkin
rr27 = {"keyword":"sap_total_sugar","uid":sap_sugar,"min":"","max":""}
rr3 = {"keyword":"sap_brix","min":"8","max":"12"}
rr19 = {"keyword":"sap_ph","uid":sap_ph,"min":"5.8","max":"6.5"}
rr8 = {"keyword":"sap_ec","uid":sap_ec,"min":"10","max":"12"}
rr5 = {"keyword":"sap_chloride","uid":sap_cl,"min":"1400","max":"2500"}
rr25 = {"keyword":"sap_sulfur","UID":sap_s,"min":"80","max":"200"}
rr20 = {"keyword":"sap_phosphorous","uid":sap_p,"min":"80","max":"250"}
rr4 = {"keyword":"sap_calcium","min":"250","max":"350"}
rr21 = {"keyword":"sap_potassium","uid":sap_k,"min":"4500","max":"6000"}
rr10 = {"keyword":"sap_kcaratio","uid":sap_kca,"min":"","max":""}
rr11 = {"keyword":"sap_magnesium","min":"200","max":"300"}
rr24 = {"keyword":"sap_sodium","uid":sap_na,"min":"50","max":"100"}
rr1 = {"keyword":"sap_aluminum","uid":sap_al,"min":"","max":""}
rr2 = {"keyword":"sap_boron","uid":sap_b,"min":"2.5","max":"5"}
rr6 = {"keyword":"sap_cobalt","uid":sap_co,"min":"","max":""}
rr7 = {"keyword":"sap_copper","uid":sap_cu,"min":"1","max":"5"}
rr9 = {"keyword":"sap_iron","uid":sap_fe,"min":"1","max":"5"}
rr12 = {"keyword":"sap_manganese","uid":sap_mn,"min":"1","max":"5"}
rr13 = {"keyword":"sap_molybdenum","min":"","max":""}
rr14 = {"keyword":"sap_nickel","uid":sap_ni,"min":"","max":""}
rr22 = {"keyword":"sap_selenium","uid":sap_se,"min":"","max":""}
rr23 = {"keyword":"sap_silica","uid":sap_si,"min":"30","max":"60"}
rr26 = {"keyword":"sap_zinc","min":"1.5","max":"5"}
rr16 = {"keyword":"sap_nitrogen_as_ammonium","uid":sap_nnh4,"min":"","max":""}
rr17 = {"keyword":"sap_nitrogen_as_nitrate","uid":sap_nno3,"min":"1130","max":"1355"}
rr18 = {"keyword":"sap_total_nitrogen","UID":sap_totaln,"min":"","max":""}
rr15 = {"keyword":"sap_nitrate","UID":sap_no3,"min":"5000","max":"6000"}
rr = [rr1,rr2,rr3,rr4,rr5,rr6,rr7,rr8,rr9,rr10,rr11,rr12,rr13,rr14,rr14,rr15,rr16,rr17,rr18,rr19,rr20,rr21,rr22,rr23,rr24,rr25,rr26,rr27]
pumpkin_spec = api.create(specs, "AnalysisSpec", title="Pumpkin Sap", SampleType=saptype, ResultsRange=rr).UID()

##Soybean
rr27 = {"keyword":"sap_total_sugar","uid":sap_sugar,"min":"0.5","max":"1.1"}
rr3 = {"keyword":"sap_brix","min":"","max":""}
rr19 = {"keyword":"sap_ph","uid":sap_ph,"min":"4","max":"8"}
rr8 = {"keyword":"sap_ec","uid":sap_ec,"min":"9.5","max":"19"}
rr5 = {"keyword":"sap_chloride","uid":sap_cl,"min":"100","max":"200"}
rr25 = {"keyword":"sap_sulfur","UID":sap_s,"min":"150","max":"300"}
rr20 = {"keyword":"sap_phosphorous","uid":sap_p,"min":"175","max":"350"}
rr4 = {"keyword":"sap_calcium","min":"1500","max":"3200"}
rr21 = {"keyword":"sap_potassium","uid":sap_k,"min":"3150","max":"6300"}
rr10 = {"keyword":"sap_kcaratio","uid":sap_kca,"min":"","max":""}
rr11 = {"keyword":"sap_magnesium","min":"1000","max":"2000"}
rr24 = {"keyword":"sap_sodium","uid":sap_na,"min":"8","max":"16"}
rr1 = {"keyword":"sap_aluminum","uid":sap_al,"min":"","max":""}
rr2 = {"keyword":"sap_boron","uid":sap_b,"min":"4.25","max":"8.5"}
rr6 = {"keyword":"sap_cobalt","uid":sap_co,"min":"","max":""}
rr7 = {"keyword":"sap_copper","uid":sap_cu,"min":"0.75","max":"1.5"}
rr9 = {"keyword":"sap_iron","uid":sap_fe,"min":"2","max":"4"}
rr12 = {"keyword":"sap_manganese","uid":sap_mn,"min":"8","max":"16"}
rr13 = {"keyword":"sap_molybdenum","min":"1","max":"2"}
rr14 = {"keyword":"sap_nickel","uid":sap_ni,"min":"","max":""}
rr22 = {"keyword":"sap_selenium","uid":sap_se,"min":"","max":""}
rr23 = {"keyword":"sap_silica","uid":sap_si,"min":"35","max":"70"}
rr26 = {"keyword":"sap_zinc","min":"3.5","max":"70"}
rr16 = {"keyword":"sap_nitrogen_as_ammonium","uid":sap_nnh4,"min":"","max":""}
rr17 = {"keyword":"sap_nitrogen_as_nitrate","uid":sap_nno3,"min":"125","max":"250"}
rr18 = {"keyword":"sap_total_nitrogen","UID":sap_totaln,"min":"1250","max":"2500"}
rr15 = {"keyword":"sap_nitrate","UID":sap_no3,"min":"550","max":"1100"}
rr = [rr1,rr2,rr3,rr4,rr5,rr6,rr7,rr8,rr9,rr10,rr11,rr12,rr13,rr14,rr14,rr15,rr16,rr17,rr18,rr19,rr20,rr21,rr22,rr23,rr24,rr25,rr26,rr27]
soybean_spec = api.create(specs, "AnalysisSpec", title="Soybean Sap", SampleType=saptype, ResultsRange=rr).UID()

##Squash, Winter
rr27 = {"keyword":"sap_total_sugar","uid":sap_sugar,"min":"","max":""}
rr3 = {"keyword":"sap_brix","min":"8","max":"12"}
rr19 = {"keyword":"sap_ph","uid":sap_ph,"min":"5.8","max":"6.5"}
rr8 = {"keyword":"sap_ec","uid":sap_ec,"min":"10","max":"12"}
rr5 = {"keyword":"sap_chloride","uid":sap_cl,"min":"1400","max":"2500"}
rr25 = {"keyword":"sap_sulfur","UID":sap_s,"min":"80","max":"200"}
rr20 = {"keyword":"sap_phosphorous","uid":sap_p,"min":"80","max":"250"}
rr4 = {"keyword":"sap_calcium","min":"250","max":"350"}
rr21 = {"keyword":"sap_potassium","uid":sap_k,"min":"4500","max":"6000"}
rr10 = {"keyword":"sap_kcaratio","uid":sap_kca,"min":"","max":""}
rr11 = {"keyword":"sap_magnesium","min":"200","max":"300"}
rr24 = {"keyword":"sap_sodium","uid":sap_na,"min":"50","max":"100"}
rr1 = {"keyword":"sap_aluminum","uid":sap_al,"min":"","max":""}
rr2 = {"keyword":"sap_boron","uid":sap_b,"min":"2.5","max":"5"}
rr6 = {"keyword":"sap_cobalt","uid":sap_co,"min":"","max":""}
rr7 = {"keyword":"sap_copper","uid":sap_cu,"min":"1","max":"5"}
rr9 = {"keyword":"sap_iron","uid":sap_fe,"min":"1","max":"5"}
rr12 = {"keyword":"sap_manganese","uid":sap_mn,"min":"1","max":"5"}
rr13 = {"keyword":"sap_molybdenum","min":"","max":""}
rr14 = {"keyword":"sap_nickel","uid":sap_ni,"min":"","max":""}
rr22 = {"keyword":"sap_selenium","uid":sap_se,"min":"","max":""}
rr23 = {"keyword":"sap_silica","uid":sap_si,"min":"30","max":"60"}
rr26 = {"keyword":"sap_zinc","min":"1.5","max":"5"}
rr16 = {"keyword":"sap_nitrogen_as_ammonium","uid":sap_nnh4,"min":"","max":""}
rr17 = {"keyword":"sap_nitrogen_as_nitrate","uid":sap_nno3,"min":"1130","max":"1355"}
rr18 = {"keyword":"sap_total_nitrogen","UID":sap_totaln,"min":"","max":""}
rr15 = {"keyword":"sap_nitrate","UID":sap_no3,"min":"5000","max":"6000"}
rr = [rr1,rr2,rr3,rr4,rr5,rr6,rr7,rr8,rr9,rr10,rr11,rr12,rr13,rr14,rr14,rr15,rr16,rr17,rr18,rr19,rr20,rr21,rr22,rr23,rr24,rr25,rr26,rr27]
squash_winter_spec = api.create(specs, "AnalysisSpec", title="Squash (Winter) Sap", SampleType=saptype, ResultsRange=rr)

##Strawberry
rr27 = {"keyword":"sap_total_sugar","uid":sap_sugar,"min":"1","max":"3"}
rr3 = {"keyword":"sap_brix","min":"4","max":"6"}
rr19 = {"keyword":"sap_ph","uid":sap_ph,"min":"5.5","max":"5.8"}
rr8 = {"keyword":"sap_ec","uid":sap_ec,"min":"12","max":"15"}
rr5 = {"keyword":"sap_chloride","uid":sap_cl,"min":"1000","max":"3000"}
rr25 = {"keyword":"sap_sulfur","UID":sap_s,"min":"100","max":"500"}
rr20 = {"keyword":"sap_phosphorous","uid":sap_p,"min":"120","max":"250"}
rr4 = {"keyword":"sap_calcium","min":"300","max":"500"}
rr21 = {"keyword":"sap_potassium","uid":sap_k,"min":"4000","max":"5500"}
rr10 = {"keyword":"sap_kcaratio","uid":sap_kca,"min":"","max":""}
rr11 = {"keyword":"sap_magnesium","min":"300","max":"600"}
rr24 = {"keyword":"sap_sodium","uid":sap_na,"min":"100","max":"500"}
rr1 = {"keyword":"sap_aluminum","uid":sap_al,"min":"","max":""}
rr2 = {"keyword":"sap_boron","uid":sap_b,"min":"2","max":"10"}
rr6 = {"keyword":"sap_cobalt","uid":sap_co,"min":"","max":""}
rr7 = {"keyword":"sap_copper","uid":sap_cu,"min":"2","max":"20"}
rr9 = {"keyword":"sap_iron","uid":sap_fe,"min":"2","max":"10"}
rr12 = {"keyword":"sap_manganese","uid":sap_mn,"min":"2","max":"10"}
rr13 = {"keyword":"sap_molybdenum","min":"1.3","max":"5"}
rr14 = {"keyword":"sap_nickel","uid":sap_ni,"min":"","max":""}
rr22 = {"keyword":"sap_selenium","uid":sap_se,"min":"","max":""}
rr23 = {"keyword":"sap_silica","uid":sap_si,"min":"5","max":"20"}
rr26 = {"keyword":"sap_zinc","min":"2","max":"10"}
rr16 = {"keyword":"sap_nitrogen_as_ammonium","uid":sap_nnh4,"min":"","max":""}
rr17 = {"keyword":"sap_nitrogen_as_nitrate","uid":sap_nno3,"min":"1015","max":"1470"}
rr18 = {"keyword":"sap_total_nitrogen","UID":sap_totaln,"min":"1000","max":"2000"}
rr15 = {"keyword":"sap_nitrate","UID":sap_no3,"min":"4500","max":"6500"}
rr = [rr1,rr2,rr3,rr4,rr5,rr6,rr7,rr8,rr9,rr10,rr11,rr12,rr13,rr14,rr14,rr15,rr16,rr17,rr18,rr19,rr20,rr21,rr22,rr23,rr24,rr25,rr26,rr27]
strawberry_spec = api.create(specs, "AnalysisSpec", title="Strawberry Sap", SampleType=saptype, ResultsRange=rr).UID()

##Strawberry Fruitset
rr27 = {"keyword":"sap_total_sugar","uid":sap_sugar,"min":"","max":"3"}
rr3 = {"keyword":"sap_brix","min":"10","max":"14"}
rr19 = {"keyword":"sap_ph","uid":sap_ph,"min":"5.5","max":"5.8"}
rr8 = {"keyword":"sap_ec","uid":sap_ec,"min":"12","max":"15"}
rr5 = {"keyword":"sap_chloride","uid":sap_cl,"min":"1000","max":"3000"}
rr25 = {"keyword":"sap_sulfur","UID":sap_s,"min":"40","max":"150"}
rr20 = {"keyword":"sap_phosphorous","uid":sap_p,"min":"150","max":"350"}
rr4 = {"keyword":"sap_calcium","min":"500","max":"800"}
rr21 = {"keyword":"sap_potassium","uid":sap_k,"min":"4500","max":"6000"}
rr10 = {"keyword":"sap_kcaratio","uid":sap_kca,"min":"","max":""}
rr11 = {"keyword":"sap_magnesium","min":"500","max":"800"}
rr24 = {"keyword":"sap_sodium","uid":sap_na,"min":"100","max":"500"}
rr1 = {"keyword":"sap_aluminum","uid":sap_al,"min":"","max":""}
rr2 = {"keyword":"sap_boron","uid":sap_b,"min":"2","max":"10"}
rr6 = {"keyword":"sap_cobalt","uid":sap_co,"min":"","max":""}
rr7 = {"keyword":"sap_copper","uid":sap_cu,"min":"1","max":"10"}
rr9 = {"keyword":"sap_iron","uid":sap_fe,"min":"2","max":"10"}
rr12 = {"keyword":"sap_manganese","uid":sap_mn,"min":"2","max":"10"}
rr13 = {"keyword":"sap_molybdenum","min":"1.3","max":"5"}
rr14 = {"keyword":"sap_nickel","uid":sap_ni,"min":"","max":""}
rr22 = {"keyword":"sap_selenium","uid":sap_se,"min":"","max":""}
rr23 = {"keyword":"sap_silica","uid":sap_si,"min":"5","max":"20"}
rr26 = {"keyword":"sap_zinc","min":"2","max":"10"}
rr16 = {"keyword":"sap_nitrogen_as_ammonium","uid":sap_nnh4,"min":"","max":""}
rr17 = {"keyword":"sap_nitrogen_as_nitrate","uid":sap_nno3,"min":"340,"max":"565"}
rr18 = {"keyword":"sap_total_nitrogen","UID":sap_totaln,"min":"1000","max":"2500"}
rr15 = {"keyword":"sap_nitrate","UID":sap_no3,"min":"1500","max":"2500"}
rr = [rr1,rr2,rr3,rr4,rr5,rr6,rr7,rr8,rr9,rr10,rr11,rr12,rr13,rr14,rr14,rr15,rr16,rr17,rr18,rr19,rr20,rr21,rr22,rr23,rr24,rr25,rr26,rr27]
strawberry_fruitset_spec = api.create(specs, "AnalysisSpec", title="Strawberry Sap, Fruitset", SampleType=saptype, ResultsRange=rr).UID()

##Strawberry Fruitfill
rr27 = {"keyword":"sap_total_sugar","uid":sap_sugar,"min":"1","max":"3"}
rr3 = {"keyword":"sap_brix","min":"10","max":"14"}
rr19 = {"keyword":"sap_ph","uid":sap_ph,"min":"5.5","max":"5.8"}
rr8 = {"keyword":"sap_ec","uid":sap_ec,"min":"12","max":"15"}
rr5 = {"keyword":"sap_chloride","uid":sap_cl,"min":"1000","max":"3000"}
rr25 = {"keyword":"sap_sulfur","UID":sap_s,"min":"40","max":"150"}
rr20 = {"keyword":"sap_phosphorous","uid":sap_p,"min":"150","max":"350"}
rr4 = {"keyword":"sap_calcium","min":"500","max":"800"}
rr21 = {"keyword":"sap_potassium","uid":sap_k,"min":"4500","max":"6000"}
rr10 = {"keyword":"sap_kcaratio","uid":sap_kca,"min":"","max":""}
rr11 = {"keyword":"sap_magnesium","min":"500","max":"800"}
rr24 = {"keyword":"sap_sodium","uid":sap_na,"min":"100","max":"500"}
rr1 = {"keyword":"sap_aluminum","uid":sap_al,"min":"","max":""}
rr2 = {"keyword":"sap_boron","uid":sap_b,"min":"2","max":"10"}
rr6 = {"keyword":"sap_cobalt","uid":sap_co,"min":"","max":""}
rr7 = {"keyword":"sap_copper","uid":sap_cu,"min":"1","max":"10"}
rr9 = {"keyword":"sap_iron","uid":sap_fe,"min":"2","max":"10"}
rr12 = {"keyword":"sap_manganese","uid":sap_mn,"min":"2","max":"10"}
rr13 = {"keyword":"sap_molybdenum","min":"1.3","max":"5"}
rr14 = {"keyword":"sap_nickel","uid":sap_ni,"min":"","max":""}
rr22 = {"keyword":"sap_selenium","uid":sap_se,"min":"","max":""}
rr23 = {"keyword":"sap_silica","uid":sap_si,"min":"5","max":"20"}
rr26 = {"keyword":"sap_zinc","min":"2","max":"10"}
rr16 = {"keyword":"sap_nitrogen_as_ammonium","uid":sap_nnh4,"min":"","max":""}
rr17 = {"keyword":"sap_nitrogen_as_nitrate","uid":sap_nno3,"min":"340","max":"565"}
rr18 = {"keyword":"sap_total_nitrogen","UID":sap_totaln,"min":"1000","max":"2500"}
rr15 = {"keyword":"sap_nitrate","UID":sap_no3,"min":"1500","max":"2500"}
rr = [rr1,rr2,rr3,rr4,rr5,rr6,rr7,rr8,rr9,rr10,rr11,rr12,rr13,rr14,rr14,rr15,rr16,rr17,rr18,rr19,rr20,rr21,rr22,rr23,rr24,rr25,rr26,rr27]
strawberry_fruitfill_spec = api.create(specs, "AnalysisSpec", title="Strawberry Sap, Fruitfill", SampleType=saptype, ResultsRange=rr).UID()

##Sweet Potato
rr27 = {"keyword":"sap_total_sugar","uid":sap_sugar,"min":"1","max":"2.5"}
rr3 = {"keyword":"sap_brix","min":"4.5","max":"7"}
rr19 = {"keyword":"sap_ph","uid":sap_ph,"min":"4.5","max":"6.5"}
rr8 = {"keyword":"sap_ec","uid":sap_ec,"min":"12.5","max":"15"}
rr5 = {"keyword":"sap_chloride","uid":sap_cl,"min":"500","max":"2000"}
rr25 = {"keyword":"sap_sulfur","UID":sap_s,"min":"80","max":"350"}
rr20 = {"keyword":"sap_phosphorous","uid":sap_p,"min":"90","max":"200"}
rr4 = {"keyword":"sap_calcium","min":"300","max":"700"}
rr21 = {"keyword":"sap_potassium","uid":sap_k,"min":"3500","max":"5000"}
rr10 = {"keyword":"sap_kcaratio","uid":sap_kca,"min":"","max":""}
rr11 = {"keyword":"sap_magnesium","min":"250","max":"700"}
rr24 = {"keyword":"sap_sodium","uid":sap_na,"min":"15","max":"50"}
rr1 = {"keyword":"sap_aluminum","uid":sap_al,"min":"","max":""}
rr2 = {"keyword":"sap_boron","uid":sap_b,"min":"1","max":"5"}
rr6 = {"keyword":"sap_cobalt","uid":sap_co,"min":"","max":""}
rr7 = {"keyword":"sap_copper","uid":sap_cu,"min":"1","max":"5"}
rr9 = {"keyword":"sap_iron","uid":sap_fe,"min":"1.5","max":"10"}
rr12 = {"keyword":"sap_manganese","uid":sap_mn,"min":"2","max":"10"}
rr13 = {"keyword":"sap_molybdenum","min":"","max":""}
rr14 = {"keyword":"sap_nickel","uid":sap_ni,"min":"","max":""}
rr22 = {"keyword":"sap_selenium","uid":sap_se,"min":"","max":""}
rr23 = {"keyword":"sap_silica","uid":sap_si,"min":"15","max":"35"}
rr26 = {"keyword":"sap_zinc","min":"2","max":"10"}
rr16 = {"keyword":"sap_nitrogen_as_ammonium","uid":sap_nnh4,"min":"","max":""}
rr17 = {"keyword":"sap_nitrogen_as_nitrate","uid":sap_nno3,"min":"340","max":"790"}
rr18 = {"keyword":"sap_total_nitrogen","UID":sap_totaln,"min":"1000","max":"2500"}
rr15 = {"keyword":"sap_nitrate","UID":sap_no3,"min":"1500","max":"3500"}
rr = [rr1,rr2,rr3,rr4,rr5,rr6,rr7,rr8,rr9,rr10,rr11,rr12,rr13,rr14,rr14,rr15,rr16,rr17,rr18,rr19,rr20,rr21,rr22,rr23,rr24,rr25,rr26,rr27]
sweet_potato_spec = api.create(specs, "AnalysisSpec", title="Sweet Potato Sap", SampleType=saptype, ResultsRange=rr).UID()

##Tangerine
rr27 = {"keyword":"sap_total_sugar","uid":sap_sugar,"min":"1.5","max":"2"}
rr3 = {"keyword":"sap_brix","min":"2","max":"5"}
rr19 = {"keyword":"sap_ph","uid":sap_ph,"min":"5.8","max":"6.2"}
rr8 = {"keyword":"sap_ec","uid":sap_ec,"min":"2","max":"5"}
rr5 = {"keyword":"sap_chloride","uid":sap_cl,"min":"150","max":"1500"}
rr25 = {"keyword":"sap_sulfur","UID":sap_s,"min":"100","max":"500"}
rr20 = {"keyword":"sap_phosphorous","uid":sap_p,"min":"150","max":"250"}
rr4 = {"keyword":"sap_calcium","min":"1200","max":"2500"}
rr21 = {"keyword":"sap_potassium","uid":sap_k,"min":"3000","max":"4800"}
rr10 = {"keyword":"sap_kcaratio","uid":sap_kca,"min":"","max":""}
rr11 = {"keyword":"sap_magnesium","min":"450","max":"1200"}
rr24 = {"keyword":"sap_sodium","uid":sap_na,"min":"10","max":"75"}
rr1 = {"keyword":"sap_aluminum","uid":sap_al,"min":"","max":""}
rr2 = {"keyword":"sap_boron","uid":sap_b,"min":"8","max":"20"}
rr6 = {"keyword":"sap_cobalt","uid":sap_co,"min":"","max":""}
rr7 = {"keyword":"sap_copper","uid":sap_cu,"min":"2","max":"20"}
rr9 = {"keyword":"sap_iron","uid":sap_fe,"min":"2.5","max":"10"}
rr12 = {"keyword":"sap_manganese","uid":sap_mn,"min":"3","max":"15"}
rr13 = {"keyword":"sap_molybdenum","min":"0.5","max":"2.5"}
rr14 = {"keyword":"sap_nickel","uid":sap_ni,"min":"","max":""}
rr22 = {"keyword":"sap_selenium","uid":sap_se,"min":"","max":""}
rr23 = {"keyword":"sap_silica","uid":sap_si,"min":"25","max":"75"}
rr26 = {"keyword":"sap_zinc","min":"5","max":"15"}
rr16 = {"keyword":"sap_nitrogen_as_ammonium","uid":sap_nnh4,"min":"","max":""}
rr17 = {"keyword":"sap_nitrogen_as_nitrate","uid":sap_nno3,"min":"90","max":"180"}
rr18 = {"keyword":"sap_total_nitrogen","UID":sap_totaln,"min":"500","max":"2000"}
rr15 = {"keyword":"sap_nitrate","UID":sap_no3,"min":"400","max":"800"}
rr = [rr1,rr2,rr3,rr4,rr5,rr6,rr7,rr8,rr9,rr10,rr11,rr12,rr13,rr14,rr14,rr15,rr16,rr17,rr18,rr19,rr20,rr21,rr22,rr23,rr24,rr25,rr26,rr27]
tangerine_spec = api.create(specs, "AnalysisSpec", title="Tangerine Sap", SampleType=saptype, ResultsRange=rr).UID()

##Tomato (Cherry)
rr27 = {"keyword":"sap_total_sugar","uid":sap_sugar,"min":"1","max":"3"}
rr3 = {"keyword":"sap_brix","min":"4","max":"6"}
rr19 = {"keyword":"sap_ph","uid":sap_ph,"min":"5.5","max":"5.8"}
rr8 = {"keyword":"sap_ec","uid":sap_ec,"min":"12","max":"15"}
rr5 = {"keyword":"sap_chloride","uid":sap_cl,"min":"1000","max":"3000"}
rr25 = {"keyword":"sap_sulfur","UID":sap_s,"min":"100","max":"300"}
rr20 = {"keyword":"sap_phosphorous","uid":sap_p,"min":"90","max":"190"}
rr4 = {"keyword":"sap_calcium","min":"400","max":"800"}
rr21 = {"keyword":"sap_potassium","uid":sap_k,"min":"4500","max":"6000"}
rr10 = {"keyword":"sap_kcaratio","uid":sap_kca,"min":"","max":""}
rr11 = {"keyword":"sap_magnesium","min":"300","max":"600"}
rr24 = {"keyword":"sap_sodium","uid":sap_na,"min":"100","max":"500"}
rr1 = {"keyword":"sap_aluminum","uid":sap_al,"min":"","max":""}
rr2 = {"keyword":"sap_boron","uid":sap_b,"min":"2","max":"10"}
rr6 = {"keyword":"sap_cobalt","uid":sap_co,"min":"","max":""}
rr7 = {"keyword":"sap_copper","uid":sap_cu,"min":"1.5","max":"20"}
rr9 = {"keyword":"sap_iron","uid":sap_fe,"min":"1.5","max":"10"}
rr12 = {"keyword":"sap_manganese","uid":sap_mn,"min":"1.5","max":"10"}
rr13 = {"keyword":"sap_molybdenum","min":"1.3","max":"5"}
rr14 = {"keyword":"sap_nickel","uid":sap_ni,"min":"","max":""}
rr22 = {"keyword":"sap_selenium","uid":sap_se,"min":"","max":""}
rr23 = {"keyword":"sap_silica","uid":sap_si,"min":"5","max":"20"}
rr26 = {"keyword":"sap_zinc","min":"2.5","max":"10"}
rr16 = {"keyword":"sap_nitrogen_as_ammonium","uid":sap_nnh4,"min":"","max":""}
rr17 = {"keyword":"sap_nitrogen_as_nitrate","uid":sap_nno3,"min":"790","max":"1130"}
rr18 = {"keyword":"sap_total_nitrogen","UID":sap_totaln,"min":"1000","max":"2000"}
rr15 = {"keyword":"sap_nitrate","UID":sap_no3,"min":"3500","max":"5000"}
rr = [rr1,rr2,rr3,rr4,rr5,rr6,rr7,rr8,rr9,rr10,rr11,rr12,rr13,rr14,rr14,rr15,rr16,rr17,rr18,rr19,rr20,rr21,rr22,rr23,rr24,rr25,rr26,rr27]
tomato_cherry_spec = api.create(specs, "AnalysisSpec", title="Tomato (Cherry) Sap", SampleType=saptype, ResultsRange=rr).UID()

##Tomato (Determinate)
rr27 = {"keyword":"sap_total_sugar","uid":sap_sugar,"min":"1","max":"3"}
rr3 = {"keyword":"sap_brix","min":"4","max":"6"}
rr19 = {"keyword":"sap_ph","uid":sap_ph,"min":"5.5","max":"5.8"}
rr8 = {"keyword":"sap_ec","uid":sap_ec,"min":"12","max":"15"}
rr5 = {"keyword":"sap_chloride","uid":sap_cl,"min":"1000","max":"3000"}
rr25 = {"keyword":"sap_sulfur","UID":sap_s,"min":"100","max":"500"}
rr20 = {"keyword":"sap_phosphorous","uid":sap_p,"min":"120","max":"250"}
rr4 = {"keyword":"sap_calcium","min":"300","max":"500"}
rr21 = {"keyword":"sap_potassium","uid":sap_k,"min":"4000","max":"5500"}
rr10 = {"keyword":"sap_kcaratio","uid":sap_kca,"min":"","max":""}
rr11 = {"keyword":"sap_magnesium","min":"300","max":"600"}
rr24 = {"keyword":"sap_sodium","uid":sap_na,"min":"100","max":"500"}
rr1 = {"keyword":"sap_aluminum","uid":sap_al,"min":"","max":""}
rr2 = {"keyword":"sap_boron","uid":sap_b,"min":"2","max":"10"}
rr6 = {"keyword":"sap_cobalt","uid":sap_co,"min":"","max":""}
rr7 = {"keyword":"sap_copper","uid":sap_cu,"min":"2","max":"20"}
rr9 = {"keyword":"sap_iron","uid":sap_fe,"min":"2","max":"10"}
rr12 = {"keyword":"sap_manganese","uid":sap_mn,"min":"2","max":"10"}
rr13 = {"keyword":"sap_molybdenum","min":"1.3","max":"5"}
rr14 = {"keyword":"sap_nickel","uid":sap_ni,"min":"","max":""}
rr22 = {"keyword":"sap_selenium","uid":sap_se,"min":"","max":""}
rr23 = {"keyword":"sap_silica","uid":sap_si,"min":"5","max":"20"}
rr26 = {"keyword":"sap_zinc","min":"2","max":"10"}
rr16 = {"keyword":"sap_nitrogen_as_ammonium","uid":sap_nnh4,"min":"","max":""}
rr17 = {"keyword":"sap_nitrogen_as_nitrate","uid":sap_nno3,"min":"1015","max":"1470"}
rr18 = {"keyword":"sap_total_nitrogen","UID":sap_totaln,"min":"1000","max":"2000"}
rr15 = {"keyword":"sap_nitrate","UID":sap_no3,"min":"4500","max":"6500"}
rr = [rr1,rr2,rr3,rr4,rr5,rr6,rr7,rr8,rr9,rr10,rr11,rr12,rr13,rr14,rr14,rr15,rr16,rr17,rr18,rr19,rr20,rr21,rr22,rr23,rr24,rr25,rr26,rr27]
tomato_determinate_spec = api.create(specs, "AnalysisSpec", title="Tomato (Determinate) Sap", SampleType=saptype, ResultsRange=rr).UID()

##Tomato
rr27 = {"keyword":"sap_total_sugar","uid":sap_sugar,"min":"1","max":"3"}
rr3 = {"keyword":"sap_brix","min":"","max":""}
rr19 = {"keyword":"sap_ph","uid":sap_ph,"min":"5.5","max":"6.5"}
rr8 = {"keyword":"sap_ec","uid":sap_ec,"min":"9","max":"18"}
rr5 = {"keyword":"sap_chloride","uid":sap_cl,"min":"450","max":"900"}
rr25 = {"keyword":"sap_sulfur","UID":sap_s,"min":"1250","max":"2500"}
rr20 = {"keyword":"sap_phosphorous","uid":sap_p,"min":"300","max":"600"}
rr4 = {"keyword":"sap_calcium","min":"2000","max":"6000"}
rr21 = {"keyword":"sap_potassium","uid":sap_k,"min":"3000","max":"6000"}
rr10 = {"keyword":"sap_kcaratio","uid":sap_kca,"min":"","max":""}
rr11 = {"keyword":"sap_magnesium","min":"400","max":"800"}
rr24 = {"keyword":"sap_sodium","uid":sap_na,"min":"33","max":"66"}
rr1 = {"keyword":"sap_aluminum","uid":sap_al,"min":"","max":""}
rr2 = {"keyword":"sap_boron","uid":sap_b,"min":"2.5","max":"5"}
rr6 = {"keyword":"sap_cobalt","uid":sap_co,"min":"","max":""}
rr7 = {"keyword":"sap_copper","uid":sap_cu,"min":"1.3","max":"3.6"}
rr9 = {"keyword":"sap_iron","uid":sap_fe,"min":"2.5","max":"5"}
rr12 = {"keyword":"sap_manganese","uid":sap_mn,"min":"15","max":"30"}
rr13 = {"keyword":"sap_molybdenum","min":"1.3","max":"5"}
rr14 = {"keyword":"sap_nickel","uid":sap_ni,"min":"","max":""}
rr22 = {"keyword":"sap_selenium","uid":sap_se,"min":"","max":""}
rr23 = {"keyword":"sap_silica","uid":sap_si,"min":"7","max":"14"}
rr26 = {"keyword":"sap_zinc","min":"1.3","max":"27"}
rr16 = {"keyword":"sap_nitrogen_as_ammonium","uid":sap_nnh4,"min":"","max":""}
rr17 = {"keyword":"sap_nitrogen_as_nitrate","uid":sap_nno3,"min":"450","max":"900"}
rr18 = {"keyword":"sap_total_nitrogen","UID":sap_totaln,"min":"1000","max":"2000"}
rr15 = {"keyword":"sap_nitrate","UID":sap_no3,"min":"1000","max":"4000"}
rr = [rr1,rr2,rr3,rr4,rr5,rr6,rr7,rr8,rr9,rr10,rr11,rr12,rr13,rr14,rr14,rr15,rr16,rr17,rr18,rr19,rr20,rr21,rr22,rr23,rr24,rr25,rr26,rr27]
tomato_spec = api.create(specs, "AnalysisSpec", title="Tomato Sap", SampleType=saptype, ResultsRange=rr).UID()

##Wheat
rr27 = {"keyword":"sap_total_sugar","uid":sap_sugar,"min":"1.5","max":"2"}
rr3 = {"keyword":"sap_brix","min":"7","max":"10"}
rr19 = {"keyword":"sap_ph","uid":sap_ph,"min":"5.3","max":"6.3"}
rr8 = {"keyword":"sap_ec","uid":sap_ec,"min":"10.5","max":"14"}
rr5 = {"keyword":"sap_chloride","uid":sap_cl,"min":"1000","max":"6000"}
rr25 = {"keyword":"sap_sulfur","UID":sap_s,"min":"200","max":"800"}
rr20 = {"keyword":"sap_phosphorous","uid":sap_p,"min":"150","max":"250"}
rr4 = {"keyword":"sap_calcium","min":"250","max":"800"}
rr21 = {"keyword":"sap_potassium","uid":sap_k,"min":"4000","max":"8000"}
rr10 = {"keyword":"sap_kcaratio","uid":sap_kca,"min":"","max":""}
rr11 = {"keyword":"sap_magnesium","min":"200","max":"400"}
rr24 = {"keyword":"sap_sodium","uid":sap_na,"min":"25","max":"100"}
rr1 = {"keyword":"sap_aluminum","uid":sap_al,"min":"","max":""}
rr2 = {"keyword":"sap_boron","uid":sap_b,"min":"8","max":"15"}
rr6 = {"keyword":"sap_cobalt","uid":sap_co,"min":"","max":""}
rr7 = {"keyword":"sap_copper","uid":sap_cu,"min":"1","max":"10"}
rr9 = {"keyword":"sap_iron","uid":sap_fe,"min":"8","max":"25"}
rr12 = {"keyword":"sap_manganese","uid":sap_mn,"min":"5","max":"20"}
rr13 = {"keyword":"sap_molybdenum","min":"","max":""}
rr14 = {"keyword":"sap_nickel","uid":sap_ni,"min":"","max":""}
rr22 = {"keyword":"sap_selenium","uid":sap_se,"min":"","max":""}
rr23 = {"keyword":"sap_silica","uid":sap_si,"min":"20","max":"75"}
rr26 = {"keyword":"sap_zinc","min":"2.5","max":"10"}
rr16 = {"keyword":"sap_nitrogen_as_ammonium","uid":sap_nnh4,"min":"","max":""}
rr17 = {"keyword":"sap_nitrogen_as_nitrate","uid":sap_nno3,"min":"180","max":"450"}
rr18 = {"keyword":"sap_total_nitrogen","UID":sap_totaln,"min":"","max":""}
rr15 = {"keyword":"sap_nitrate","UID":sap_no3,"min":"800","max":"2000"}
rr = [rr1,rr2,rr3,rr4,rr5,rr6,rr7,rr8,rr9,rr10,rr11,rr12,rr13,rr14,rr14,rr15,rr16,rr17,rr18,rr19,rr20,rr21,rr22,rr23,rr24,rr25,rr26,rr27]
wheat_spec = api.create(specs, "AnalysisSpec", title="Wheat Sap", SampleType=saptype, ResultsRange=rr).UID()

for i in api.search({'portal_type':'AnalysisSpec'}):
    api.get_object(i).reindexObject()

#SampleMatrices

#SubGroups

pair1 = api.create(subgroups, "SubGroup", title="Pair 1")
pair2 = api.create(subgroups, "SubGroup", title="Pair 2")
pair3 = api.create(subgroups, "SubGroup", title="Pair 3")
pair4 = api.create(subgroups, "SubGroup", title="Pair 4")
pair5 = api.create(subgroups, "SubGroup", title="Pair 5")
pair6 = api.create(subgroups, "SubGroup", title="Pair 6")
pair7 = api.create(subgroups, "SubGroup", title="Pair 7")
pair8 = api.create(subgroups, "SubGroup", title="Pair 8")
pair9 = api.create(subgroups, "SubGroup", title="Pair 9")
pair10 = api.create(subgroups, "SubGroup", title="Pair 10")
pair11 = api.create(subgroups, "SubGroup", title="Pair 11")
pair12 = api.create(subgroups, "SubGroup", title="Pair 12")
pair13 = api.create(subgroups, "SubGroup", title="Pair 13")
pair14 = api.create(subgroups, "SubGroup", title="Pair 14")
pair15 = api.create(subgroups, "SubGroup", title="Pair 15")
pair16 = api.create(subgroups, "SubGroup", title="Pair 16")
pair17 = api.create(subgroups, "SubGroup", title="Pair 17")
pair18 = api.create(subgroups, "SubGroup", title="Pair 18")
pair19 = api.create(subgroups, "SubGroup", title="Pair 19")
pair20 = api.create(subgroups, "SubGroup", title="Pair 20")

for i in api.search({'portal_type':'SubGroup'}):
    api.get_object(i).reindexObject()

#Labels

mbg = api.create(labels, "BatchLabel", title="Send to MBG")

for i in api.search({'portal_type':'BatchLabel'}):
    api.get_object(i).reindexObject()

#Clients

##Import from CSV

#Contacts

##Import from CSV

#SamplePoints

##Import from CSV

#SDG and Sample Data

##Import from CSV

import transaction
transaction.get().commit()
