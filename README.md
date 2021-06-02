# Climate-Resolve-Matrix-Parser

A set of tools to parse the Climate Resolve Matrix, as well as other relevant data sources.

## Usage

- Install Python 3.8 and Git
- Checkout this repository, cd into directory

        C:USER> git clone git@github.com:laregionalcollaborative/Climate-Resolve-Matrix-Parser.git
        C:USER> cd Climate-Resolve-Matrix-Parser

- Create virtual environment and activate

        C:USER\Climate-Resolve-Matrix-Parser> python -m venv env
        C:USER\Climate-Resolve-Matrix-Parser> env\Scripts\activate
        (env) C:USER\Climate-Resolve-Matrix-Parser>

- install requirements

        (env) C:USER\Climate-Resolve-Matrix-Parser> pip install -r requirements.txt

- download the relevant data sources, and update constants.py accordingly with their filenames
- run the parsing script

        (env) C:USER\Climate-Resolve-Matrix-Parser> python parse_csv.py
