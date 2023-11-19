# UK Crayfish Data Dashboard: Tackling Environmental Challenges

## Description
This interactive dashboard is dedicated to the critical analysis of crayfish data in the UK, 
with a particular focus on addressing the environmental challenges posed by the invasive signal crayfish species. 
The rapid increase in the signal crayfish population is detrimentally impacting ecosystems, biodiversity, 
and public infrastructure, as these crayfish consume surrounding aquatic life and burrow into riverbanks. 
Our tool provides a valuable resource for scientists and fishermen to locate, monitor, and manage crayfish populations, 
thereby contributing significantly to wildlife conservation and environmental protection efforts.

## Technology Stack
- Backend: Python, flask, dash, plotly
- Frontend: Jinja2, HTML, CSS
- Data Analysis: pandas, numpy
- Database: sqlite3, sqlalchemy
- Testing: pytest, Selenium

## Usage

Users can interact with the dashboard to:

- Identify high-risk areas due to large populations of signal crayfish.
- Understand the best methods for capturing female signal crayfish.
- Analyse demographic data such as average size, weight, and gender distribution of crayfish.
- Locate the best sites for specific types of signal crayfish capture.

## Design and Architecture
This project combines robust data analysis algorithms with a user-friendly presentation layer. 
The architecture is designed to facilitate easy navigation and interactive data exploration, 
enabling users to make informed decisions and analyses.

## Set Up Instruction
```shell
pip install -r requirements.txt
pip install -e .
```

## To Run the Flask App
```shell
python -m flask --app "crayfish_analysis_app:create_app('config.DevelopmentConfig')" --debug run
```
The flask app should be running on http://127.0.0.1:5000.

## Import Excel to Database
If the tables named "crayfish1" and "crayfish2" in database.db are empty or there is no data list shown in the route 
```/crayfish1``` and ```/crayfish2```, the following command should be executed once 
to import the data from the Excel file to the database. *Note that this command should not be run twice,
otherwise the data in the database will be duplicated.*
```shell
python data/excel_to_db.py
```

## Testing
- To run tests: 
```shell
pytest
```
- To generate test coverage reports:
```shell
pytest --cov
```