import pandas as pd
from dataclasses import dataclass
import re
import constants
import numpy as np

@dataclass
class DocumentURL:
    '''Represents a Document with a type, year, and url link'''
    type: str
    year: str
    link: str

def load_climate_resolve_data():
    '''Loads the climate resolve data and returns it as a pandas dataframe'''
    fname = constants.CLIMATE_RESOLVE_META["excel_fname"]
    sheet_name = constants.CLIMATE_RESOLVE_META["excel_tabname"]
    usecols = list(constants.CLIMATE_RESOLVE_COLUMN_TO_OUTPUT_COLUMN_MAP.keys())
    return pd.read_excel(fname, sheet_name=sheet_name, usecols=usecols)

def load_fema_data():
    '''Loads the fema data and returns it as a pandas dataframe'''
    fname = constants.FEMA_META["excel_fname"]
    sheet_name = constants.FEMA_META["excel_tabname"]
    usecols = list(constants.FEMA_COLUMN_TO_OUTPUT_COLUMN_MAP.keys())
    return pd.read_excel(fname, sheet_name=sheet_name, usecols=usecols)

def load_scag_data():
    '''Loads the scag map data and returns it as a pandas dataframe'''
    fname = constants.SCAG_MAP_META["excel_fname"]
    sheet_name = constants.SCAG_MAP_META["excel_tabname"]
    usecols = list(constants.SCAG_COLUMN_TO_OUTPUT_COLUMN_MAP.keys())
    return pd.read_excel(fname, sheet_name=sheet_name, usecols=usecols)

def parse_scag_data(data):
    '''Extract additional information from the data'''
    data["mun_scag_temp"] = data.apply(lambda row: FixSCAGMunicipalities(row["mun_scag"], row["countyscag"]), axis=1)

def FixSCAGMunicipalities(mun_scag, countyscag):
    '''Fixes some county names that don't map 1:1, and also the case in which Unincorporated is provided, in which
    it needs to add "County" to the end of the county name, which maps nicely later on'''
    if mun_scag in constants.SCAG_TO_OUTPUT_MUNICIPALITY_MAPPING.keys():
        print(f"Changing {mun_scag} to {constants.SCAG_TO_OUTPUT_MUNICIPALITY_MAPPING[mun_scag]}")
        return constants.SCAG_TO_OUTPUT_MUNICIPALITY_MAPPING[mun_scag]
    elif mun_scag == "Unincorporated":
        print(f"Changing {mun_scag} to {countyscag} County")
        return countyscag + " County"
    else:
        return mun_scag

def FixMunicipalities(name: str):
    '''Applies a dictionary mapping for municipality names that don't match exactly'''
    if name in constants.CLIMATE_RESOLVE_TO_FEMA_MUNICIPALITY_MAPPING.keys():
        return constants.CLIMATE_RESOLVE_TO_FEMA_MUNICIPALITY_MAPPING[name]
    return name

def parse_climate_resolve_data(data):
    '''Extract additional information from the data'''
    data["phone"] = data["staff_info"].apply(lambda x: GetPhoneFromStaffInfo(x))
    data["email"] = data["staff_info"].apply(lambda x: GetEmailFromStaffInfo(x))
    data["first_name"], data["last_name"], data["position"] = zip(*data["staff_info"].apply(lambda x: GetContactNamePositionFromStaffInfo(x)))
    data["name"] = data["first_name"] + " " + data["last_name"]
    data["documents"] = data["URL's to relevant documents"].apply(lambda x: GetDocumentsFromURLs(x))
    data["cap_link"] = data["documents"].apply(lambda x: GetSpecificURL(x, constants.PLAN_TYPE_MAP["cap"]))
    data["sust_link"] = data["documents"].apply(lambda x: GetSpecificURL(x, constants.PLAN_TYPE_MAP["sust"]))
    data["lhmp_link"] = data["documents"].apply(lambda x: GetSpecificURL(x, constants.PLAN_TYPE_MAP["lhmp"]))
    data["mun_name"] = data["mun_name"].apply(lambda x: FixMunicipalities(x))

def remove_ending_city_from_word(word):
    '''Removes 'city' from the end of a word, if it exists, and returns the result'''
    pattern = re.compile(r"([a-zA-Z ().ñ]*?) city")
    res = pattern.findall(word)
    if len(res) == 1:
        return res[0]
    return word

def parse_fema_data(data):
    '''Extract additional information from the data'''
    data["mun_name_f"] = data["mun_name_f"].apply(lambda x: remove_ending_city_from_word(x))

def combine_lhmp_status_columns(data):
    '''Combine information from the FEMA and Climate Resolve data into the lhmp_stat final column'''
    data["lhmp_stat"] = data["lhmp_fema"].where(data["lhmp_fema"].notnull(), data["lhmp_cr"]) # Use FEMA data where available, otherwise default to climate resolve data
    winnow_dict = {
        "unaccounted for": ["no"],
        "in progress": ["in process", "awaiting revisions", "approvable pending adoption"],
        "approved": ["yes", "approved"]
    }
    data["lhmp_stat"] = data["lhmp_stat"].apply(lambda x: winnow_value(x, **winnow_dict))

def winnow_value(x, blank="unaccounted for", default="unaccounted for", **kwargs):
    '''Checks the provided string based on the kwargs values, and returns the associated key if found.'''
    if type(x) is not str:
        return blank
    x = x.lower()
    if len(kwargs) == 0:
        kwargs = constants.WINNOW_DEFAULT_DICT # use the default dictionary if none is provided
    for key, values in kwargs.items():
        if any([value in x for value in values]):
            return key
    return default

def parse_combined_data(data):
    '''Extract additional information from the data'''
    combine_lhmp_status_columns(data)
    data["sb379_int"] = data["sb379_int"].apply(lambda x: winnow_value(x))
    data["sb379_1035"] = data["sb379_1035"].apply(lambda x: winnow_value(x))
    data["lhmp_clim"] = data["lhmp_clim"].apply(lambda x: winnow_value(x))

    winnow_dict = {"unaccounted for": ["no"], "yes": ["yes"], "in progress": ["in process"]} # return 'unaccounted for' where it says no
    data["cap_status"] = data["cap_status"].apply(lambda x: winnow_value(x, **winnow_dict))
    data["mun_plan"] = data["mun_plan"].apply(lambda x: winnow_value(x, **winnow_dict))
    data["plan_adapt"] = data["plan_adapt"].apply(lambda x: winnow_value(x, **winnow_dict))


def GetPhoneFromStaffInfo(staff_info: str):
    '''Finds the phone number from a staff_info string and returns it as a string, with the extension if available
        - Returns None if no phone number available
        - Returns only the first phone number if multiple are found
    '''
    numbers = re.compile(constants.REGEX_MATCHING_FNS["phone_number"])
    phone = numbers.findall(staff_info)
    if len(phone) == 0:
        return None
    elif len(phone)%3 == 0:
        return "".join([str(num) for num in phone[0:3]])
    elif len(phone)%4 == 0:
        return "".join([str(num) for num in phone[0:3]]) + " x" + str(phone[3])
    else:
        return None

def GetEmailFromStaffInfo(staff_info: str):
    '''Finds the email from a staff_info string and returns it as a string
        - Returns None if no email found
        - Returns only the first email address if multiple are found
    '''
    email_fn = re.compile(constants.REGEX_MATCHING_FNS["email"])
    emails = email_fn.findall(staff_info)
    if len(emails) == 0:
        return None
    else:
        return emails[0]

def GetContactNamePositionFromStaffInfo(staff_info: str):
    '''Finds the contact name and position from a staff_info string and returns it as a 3-tuple
        - Returns None if not found
        - Returns only the first if multiple are found
    '''
    find_fn = re.compile(constants.REGEX_MATCHING_FNS["contact_name_position"])
    contacts = find_fn.findall(staff_info)
    if len(contacts) == 0:
        return (None, None, None)
    else:
        return contacts[0]

def GetDocumentsFromURLs(urls_to_relevant_docs: str):
    '''Generates DocumentURLs from info found in the provided string
    
    Args:
        - urls_to_relevant_docs (str): text from a cell in Climate Resolve's "URL's to relevant documents" column

    Returns:
        - list of DocumentURL
    '''
    res = []
    if type(urls_to_relevant_docs) is not str:
        return res
    match_fn = re.compile(constants.REGEX_MATCHING_FNS["document"])
    type_year = match_fn.findall(urls_to_relevant_docs)

    url_match_fn = re.compile(constants.REGEX_MATCHING_FNS["url"])
    urls = url_match_fn.findall(urls_to_relevant_docs)

    for type_year_match, url_match in zip(type_year, urls):
        res.append(DocumentURL(str(type_year_match[0]), str(type_year_match[1]), str(url_match)))

    return res

def GetSpecificURL(doc_list: list, type_list: list):
    '''Filters the provided list of DocumentURLs based on the partial type that is listed in type_list

    Args:
        - doc_list (list of DocumentURL): a list of DocumentURLs to search through
        - type_list (list of str): a list of partial types to search with

    Returns:
        - url (str) or None

    Note:
        - If multiple documents are found, it returns the most recent one
    '''
    filtered_docs = []
    for doc in doc_list:
        if any([t in doc.type.lower() for t in type_list]):
            # if doc.type in type_list:
            filtered_docs.append(doc)
    if len(filtered_docs) == 1:
        return filtered_docs[0].link
    if len(filtered_docs) > 1:
        max_year = max([doc.year for doc in filtered_docs])
        for doc in filtered_docs:
            if doc.year == max_year:
                return doc.link
    else:
        return None

def CleanData(data: pd.DataFrame, column_map: dict):
    '''Recursively applies column.str.strip() function to mapped columns in column_map

    Args:
        - data (pd.DataFrame): a pandas DataFrame including the data to finesse
        - column_map (dict of str -> str): a map of old_column: new_column, where 
            new_column will be the cleaned version of old_column

    Returns:
        - Nothing
    '''
    for old_column, new_column in column_map.items():
        # Strip whitespace if the data type is a string
        if type(data[old_column][0]) == str:
            data[new_column] = data[old_column].str.strip()
        else:
            data[new_column] = data[old_column]

def main():
    # Load the Climate Resolve Excel file into a pandas dataframe, clean it, and parse
    data = load_climate_resolve_data()
    CleanData(data, constants.CLIMATE_RESOLVE_COLUMN_TO_OUTPUT_COLUMN_MAP)
    parse_climate_resolve_data(data)

    # Load the FEMA Excel file into a pandas dataframe, clean it, and parse
    fema_data = load_fema_data()
    CleanData(fema_data, constants.FEMA_COLUMN_TO_OUTPUT_COLUMN_MAP)
    parse_fema_data(fema_data)

    # Load the SCAG Excel file into a pandas dataframe, clean it, and parse
    scag_data = load_scag_data()
    CleanData(scag_data, constants.SCAG_COLUMN_TO_OUTPUT_COLUMN_MAP)
    parse_scag_data(scag_data)

    # Combine the Climate Resolve and FEMA data
    data = pd.merge(data, fema_data, how="left", left_on="mun_name", right_on="mun_name_f")
    parse_combined_data(data)

    # Combine the SCAG data with the rest of the data
    data = pd.merge(data, scag_data, how="left", left_on="mun_name", right_on="mun_scag_temp")
    data["mun_index"] = data["mun_index"].fillna(0).astype("Int64") # pad the blanks with 0 so that we can make the column an integer type for QGIS to be happy

    # Update the columns that won't be included in the output file
    columns = set(data.keys())
    columns.difference_update(set(list(constants.CLIMATE_RESOLVE_COLUMN_TO_OUTPUT_COLUMN_MAP.keys()) + list(constants.FEMA_COLUMN_TO_OUTPUT_COLUMN_MAP.keys())+ list(constants.SCAG_COLUMN_TO_OUTPUT_COLUMN_MAP.keys())))
    columns.difference_update(set(constants.OUTPUT_FILE_META['columns_to_exclude']))

    columns = sorted(columns) # Sort the columns alphabetically from left to right
    data.to_excel(constants.OUTPUT_FILE_META["excel_fname"], columns=columns, index=False)

if __name__ == "__main__":
    main()