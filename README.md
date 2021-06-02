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
