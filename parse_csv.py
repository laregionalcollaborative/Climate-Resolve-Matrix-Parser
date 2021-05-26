import pandas as pd
from dataclasses import dataclass
import re

@dataclass
class Municipality:
    name: str
    county: str

@dataclass
class DocumentURL:
    municipality: Municipality
    type: str
    year: int
    link: str

def GetPhoneFromStaffInfo(staff_info):
    '''Finds the phone number from a staff_info string and returns it as an int
    '''
    numbers = re.compile(r'\d+(?:\.\d+)?')
    phone = numbers.findall(staff_info)
    if len(phone) == 3:
        return "".join([str(num) for num in phone])
    elif len(phone) == 4:
        return "".join([str(num) for num in phone[0:3]]) + " x" + phone[3]
    else:
        return None

def main():
    excel_file = "Matrix 1.1 - Status of Municipal Climate Preparedness.xlsx"
    sheet_name = "1. Summary"
    columns = [
        "County", 
        "Municipality", 
        "Name, title, affiliation, contact information of key staff",
        "Plan that includes climate action (mitigation)? ",
        "Municipality has a Local Hazard Mitigation Plan (LHMP) either created by City or from the County?",
        "Updated General Plan per SB 379 & SB1035?",
        "URL's to relevant documents",
        "Notes"
        ]
    data = pd.read_excel(excel_file, sheet_name=sheet_name, usecols=columns)

    data["county_name"] = data["County"].str.strip()
    data["city_name"] = data["Municipality"].str.strip()
    data["staff_info"] = data["Name, title, affiliation, contact information of key staff"].str.strip()
    data["phone"] = data["staff_info"].apply(lambda x: GetPhoneFromStaffInfo(x))
    data["has_plan"] = None
    data["cap_status"] = None
    data["cap_link"] = None
    data["adapt_status"] = None
    data["adapt_link"] = None
    data["sust_status"] = None
    data["sust_link"] = None
    data["lhmp_status"] = data["Municipality has a Local Hazard Mitigation Plan (LHMP) either created by City or from the County?"].str.strip()
    data["lhmp_link"] = None
    data["climate_change_ack_in_plan"] = None
    data["sb378_sb1035_compliant"] = data["Updated General Plan per SB 379 & SB1035?"].str.strip()
    print(data['phone'])

if __name__ == "__main__":
    main()