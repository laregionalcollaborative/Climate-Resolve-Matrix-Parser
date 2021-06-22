# Climate-Resolve-Matrix-Parser

A set of tools to parse the Climate Resolve Matrix, as well as other relevant data sources.

## Usage

- Install Python 3.8 and Git
- Checkout this repository

        git clone git@github.com:laregionalcollaborative/Climate-Resolve-Matrix-Parser.git

- cd into directory

        cd Climate-Resolve-Matrix-Parser

- Create virtual environment

        python -m venv env

- Activate virtual environment

        env\Scripts\activate

- install requirements

        pip install -r requirements.txt

- download the relevant data sources, and update constants.py accordingly with their filenames
- run the parsing script

        python parse_csv.py

## Release Notes

### Version 1.2, 6/21/2021
 - Added "action plan for climate resilience" as a search string to map to CAP plan type

### Version 1.1, 6/14/2021
 - Added 'name' output column, which combines first and last name into a single column
 - Added ability to import SCAG data and join into remaining data in order to include 'mun_index', which is used by QGIS to combine the output data with existing map files

### Version 1.0, 6/11/2021
 - Initial release of parser