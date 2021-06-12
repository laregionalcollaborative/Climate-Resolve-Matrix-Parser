VERSION: '1.0'

# Dictionary of useful regex strings for finding specific excerpts from longer phrases
REGEX_MATCHING_FNS = {
    "url" : r"(?i)\b((?:https?:(?:\/{1,3}|[a-z0-9%])|[a-z0-9.\-]+[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)\/)(?:[^\s()<>{}\[\]]+|\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\))+(?:\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\)|[^\s`!()\[\]{};:.,<>?«»])|(?:(?<!@)[a-z0-9]+(?:[.\-][a-z0-9]+)*[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)\b\/?(?!@)))",
    "document" : r"(.*) \((\d+|N\/A)\)",
    "phone_number" : r"(?:\(| |-|x|\n)(\d+)",
    "email" : r"([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)",
    "contact_name_position" : r"([a-zA-Z. ]+) ([a-zA-Z]+), ([a-zA-Z &,]*?)(?:\n| *\n)"
}

# Mapping of plan type (abbreviation) to a list of possible words used to describe it
PLAN_TYPE_MAP = {
    "cap": ["cap", "climate action plan", "caap", "climate action and adaptation plan", "climate and energy plan", "climate plan"],
    "sust": ["sustainability", "sustainable"],
    "lhmp": ["lhmp", "mjhmp", "hmp", "hazard"]
}

# Dictionary of useful metadata about the Climate Resolve spreadsheet
CLIMATE_RESOLVE_META = {
    "excel_fname": "Matrix 1.1 - Status of Municipal Climate Preparedness.xlsx",
    "excel_tabname": "1. Summary"
}

# Dictionary of useful metadata about the FEMA spreadsheet
FEMA_META = {
    "excel_fname": "FEMA_bay_area_so_cal_LHMP_plan_status_10-26-20.xlsx",
    "excel_tabname": "Sheet1"
}

# Mapping of column names from the Climate Resolve matrix to the output excel file
CLIMATE_RESOLVE_COLUMN_TO_OUTPUT_COLUMN_MAP = {
    "County": "county",
    "Municipality": "mun_name", 
    "Name, title, affiliation, contact information of key staff": "staff_info",
    "Municipality has a standalone climate, sustainability, and/or resilience plan?": "mun_plan",
    "Plan that includes climate action (mitigation)? ": "cap_status", # extra space is intentional
    "Plan that includes climate adaptation?": "plan_adapt",
    "Municipality has a Local Hazard Mitigation Plan (LHMP) either created by City or from the County?": "lhmp_cr",
    "Updated General Plan per SB 379 & SB1035?": "sb379_1035",
    "SB379 integration -- by direct reference to LHMP or within General Plan safety element?": "sb379_int",
    "URL's to relevant documents": "documents",
    "Does LHMP account for climate change?": "lhmp_clim",
    "Notes": "notes"
}

# Mapping of column names from the FEMA data to the output excel file
FEMA_COLUMN_TO_OUTPUT_COLUMN_MAP = {
    "County Name": "countyfema",
    "Community Name": "mun_name_f", 
    "Plan Status": "lhmp_fema",
    "Plan Type": "lhmp_type",
    "Plan is an Update (Flag)": "lhmp_rev",
    "Plan Update Number": "lhmp_rev_n",
    "Plan Approval Date": "lhmp_appr",
    "Expiration Date": "lhmp_expir"
}

# Mapping of Climate Resolve municipality names to corresponding FEMA names if not matched
CLIMATE_RESOLVE_TO_FEMA_MUNICIPALITY_MAPPING = {
    "County of Imperial": "Imperial County",
    "County of Los Angeles": "Los Angeles County",
    "County of Orange": "Orange County",
    "County of Riverside": "Riverside County",
    "County of San Bernardino": "San Bernardino County",
    "County of Ventura": "Ventura County",
    "Filmore": "Fillmore",
    "Jurupa Valley": "Jurupa Valley City",
    "La Canada Flintridge": "La Cañada Flintridge",
    "La Habra Heights": "La Habra",
    "Rolling HIlls": "Rolling Hills",
    "Yucca Valley": "Yucca Valley town",
    "Ventura": "San Buenaventura (Ventura)"
}

WINNOW_DEFAULT_DICT = {
    "no": ["no"],
    "yes": ["yes"],
    "in progress": ["in process"],
}

# Metadata about the final output file
OUTPUT_FILE_META = {
    "excel_fname": "cleaned_data.xlsx",
    "columns_to_exclude": [
        'documents',
        'staff_info',
        'notes',
        'mun_name_f',
        'countyfema',
        'lhmp_fema',
        'lhmp_cr',
        'sb379_1035'
    ]
}