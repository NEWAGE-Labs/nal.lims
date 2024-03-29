from Products.Archetypes.utils import DisplayList

WaterSourceTypes = DisplayList((
    ('', ('None')),
    ('Drinking Water Well','Drinking Water Well'),
    ('Irrigation Well','Irrigation Well'),
    ('Pond','Pond'),
    ('River','River'),
    ('Sock Well','Sock Well'),
    ('Lake','Lake'),
    ('Creek','Creek'),

))

units_vocabulary = DisplayList((
    ('P|A','Presence|Absence'),
    ('%','Percent'),
    # ('pp1000','Parts-Per-Thousand'),
    ('ppm','Parts-Per-Million'),
    ('ppb','Parts-Per-Billion'),
    # ('ppt','Parts-Per-Trillion'),
    # ('ppq','Parts-Per-Quadrillion'),
    # ('kg/L','Kilograms per Liter'),
    ('g/L','Grams per Liter'),
    ('mg/L','Milligrams per Liter'),
    ('ug/L','Micrograms per Liter'),
    ('ng/L','Nanograms per Liter'),
    # ('kg/mL','Kilograms per Microliter'),
    ('g/mL','Grams per Microliter'),
    ('mg/mL','Milligrams per Microliter'),
    ('ug/mL','Micrograms per Microliter'),
    ('ng/mL','Nanograms per Microliter'),
    # ('kg/uL','Kilograms per Nanoliter'),
    # ('g/uL','Grams per Nanoliter'),
    # ('mg/uL','Milligrams per Nanoliter'),
    # ('ug/uL','Micrograms per Nanoliter'),
    # ('ng/uL','Nanograms per Nanoliter'),
    ('mS/cm','MilliSiemens per Centimeter'),
    ('uS/cm', 'MicroSiemens per Centimeter'),
    ('umho/cm','Micromhos per Centimeter'),
    # ('kg','Kilogram'),
    ('g','Gram'),
    ('mg','Milligram'),
    ('ug','Microgram'),
    # ('ng','Nanogram'),
    ('L','Liter'),
    ('mL','Milliliter'),
    ('uL','Microliter'),
    # ('nL','Nanoliter'),
    ('count','Count'),
    ('mpn','Most Probable Number (MPN)'),
    ('mpn/10mL','MPN per 10mL'),
    ('mpn/100mL','MPN per 100mL'),
    ('mpn/1000mL','MPN per 1000mL'),
    # ('',''),
    # ('',''),
    # ('',''),
))
