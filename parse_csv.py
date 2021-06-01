import pandas as pd
from dataclasses import dataclass
import re
import constants

@dataclass
class DocumentURL:
    '''Represents a Document with a type, year, and url link'''
    type: str
    year: str
    link: str

def GetPhoneFromStaffInfo(staff_info: str):
    '''Finds the phone number from a staff_info string and returns it as a string, with the extension if available
        - Returns None if no phone number available
        - Returns only the first phone number if multiple are found
    '''
    numbers = re.compile(constants.REGEX_MATCHING_FNS["phone_number"])
    phone = numbers.findall(staff_info)
    if len(phone) == 0:
        return None
    if len(phone)%3 == 0:
        return "".join([str(num) for num in phone[0:3]])
    elif len(phone)%4 == 0:
        return "".join([str(num) for num in phone[0:3]]) + " x" + str(phone[3])
    else:
        return None

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
        data[new_column] = data[old_column].str.strip()

def main():
    # Load the Climate Resolve Excel file into a pandas dataframe
    fname = constants.CLIMATE_RESOLVE_META["excel_fname"]
    sheet_name = constants.CLIMATE_RESOLVE_META["excel_tabname"]
    usecols = list(constants.CLIMATE_RESOLVE_COLUMN_TO_OUTPUT_COLUMN_MAP.keys())
    data = pd.read_excel(fname, sheet_name=sheet_name, usecols=usecols)

    # Clean any white spaces, etc., from the data and map to the new column names
    CleanData(data, constants.CLIMATE_RESOLVE_COLUMN_TO_OUTPUT_COLUMN_MAP)

    # Extract additional information from the data
    data["phone"] = data["staff_info"].apply(lambda x: GetPhoneFromStaffInfo(x))
    data["documents"] = data["URL's to relevant documents"].apply(lambda x: GetDocumentsFromURLs(x))

    data["cap_link"] = data["documents"].apply(lambda x: GetSpecificURL(x, constants.PLAN_TYPE_MAP["cap"]))
    # data["sust_status"] = None # TODO
    data["sust_link"] = data["documents"].apply(lambda x: GetSpecificURL(x, constants.PLAN_TYPE_MAP["sust"]))
    data["lhmp_link"] = data["documents"].apply(lambda x: GetSpecificURL(x, constants.PLAN_TYPE_MAP["lhmp"]))

    columns = set(data.keys())
    columns.difference_update(set(constants.CLIMATE_RESOLVE_COLUMN_TO_OUTPUT_COLUMN_MAP.keys()))
    columns.difference_update(set(constants.OUTPUT_FILE_META['columns_to_exclude']))

    data.to_excel(constants.OUTPUT_FILE_META["excel_fname"], columns=columns, index=False)

if __name__ == "__main__":
    main()