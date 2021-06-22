# Climate-Resolve-Matrix-Parser

A set of python-based tools created to parse the [Climate Resolve Matrix dataset](https://docs.google.com/spreadsheets/d/1yJ30iVVvpmSvVAM-6IfTaepsuRYGQL49b_bLHPe5J7Q/edit#gid=623180984) and merge it with other relevant data sources into a single spreadsheet that feeds into the [L.A. CAP Map](https://www.laregionalcollaborative.com/la-cap-map). Note that Release packages contain output files needed to generate the map.

---

## Installation and Usage

- Install Python 3.8 and Git
- Checkout this repository

        git clone git@github.com:laregionalcollaborative/Climate-Resolve-Matrix-Parser.git

- cd into directory

        cd Climate-Resolve-Matrix-Parser

- Create a virtual environment

        python -m venv env

- Activate virtual environment

        env\Scripts\activate

- install requirements

        pip install -r requirements.txt

- download the relevant data sources into the same folder, and update `constants.py` accordingly with their filenames, if necessary (e.g. "FEMA_bay_area_so_cal_LHMP_plan_status_10-26-20.xlsx", etc.)
  - Note: Previous data files can be downloaded from their respective Releases
- run the parsing script

        python parse_csv.py

---

## Version Control

The Climate Resolve Matrix Parser uses [Semantic Versioning](https://semver.org/) with a 3-digit version number (MAJOR.MINOR.PATCH).
- MAJOR versions are not backwards compatible
- MINOR versions are backwards compatible, but add additional functionality and could change the output data file in a meaningful way
- PATCH versions are bug fixes / documentaiton updates which are backwards compatible and do not affect the output data file in a meaningful way 

Two branches are utilized: a main branch and a staging branch. Once changes made in the staging branch are ready to release, a pull request must be made to merge into the main branch. Update the README with release notes (see below) and the `constants.py` file with the appropriate version number. For all version releases, once merged, tag the main branch with the version number prefixed by the letter `v` (i.e. 'v1.2.1').

For MINOR and MAJOR releases, create a new Release in Github with an appropriate title and description, link to the tag that was created, and ensure the following files are included in the release:

1. Output excel file (utilize `output_file_template.xlsx` format by adding additional tabs)
2. A csv file only containing the data tab from the output excel file
3. All data source files (FEMA, SCAG, Climate Resolve, etc.)
4. ZIP file containing the QGIS output files needed for Carto (see `QGIS Instructions.docx` for instructions)

It is recommended to include a reviewer for MINOR and MAJOR releases to ensure data validity.

---

## Release Notes

### Version 1.2.1, 6/21/2021
 - Updated version numbers to conform to Semantic Versioning
 - Expanded README notes and release instructions
 - Added `output_file_template.xlsx`
 - Added `QGIS Instructions.docx`

### Version 1.2.0, 6/21/2021
 - Added "action plan for climate resilience" as a search string to map to CAP plan type

### Version 1.1.0, 6/14/2021
 - Added 'name' output column, which combines first and last name into a single column
 - Added ability to import SCAG data and join into remaining data in order to include 'mun_index', which is used by QGIS to combine the output data with existing map files

### Version 1.0.0, 6/11/2021
 - Initial release of parser