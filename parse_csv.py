import pandas as pd
from dataclasses import dataclass

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

data["County"] = data["County"].str.strip()
data["Municipality"] = data["Municipality"].str.strip()

# data["Municipality Obj"] = data.apply(lambda row: Municipality(row.Municipality, row.County), axis=1)

# documents = data["URL's to relevant documents"]
# print(documents[0].split('\n'))

# print(data.keys())
# la_data = data[data["County"] == "Los Angeles"]

municipalities = set(data["County"])
print(sorted(municipalities))
print(len(set(data["County"])))