from pathlib import Path
import pandas as pd
import sqlite3
from crayfish_analysis_app.helper_functions import read_excel_multi_index

# Define the database file name and location
db_file = Path(__file__).parent.joinpath('database.db')
excel = Path(__file__).parent.joinpath("prepared_datasets.xlsx")
print(str(db_file))

# Connect to the database
connection = sqlite3.connect(db_file)
print("Connected to database successfully")

# Create a cursor object to execute SQL queries
cursor = connection.cursor()

create_Crayfish1_table = """CREATE TABLE if not exists crayfish1(
                id INTEGER PRIMARY KEY,
                site STRING NOT NULL,
                method String NOT NULL,
                gender String NOT NULL,
                length FLOAT NOT NULL);
                """

create_Crayfish2_table = """CREATE TABLE if not exists crayfish2(
                id INTEGER PRIMARY KEY,
                site STRING NOT NULL,
                gender STRING NOT NULL,
                length FLOAT NOT NULL,
                weight FLOAT NOT NULL);
                """

# Create the tables in the database
cursor.execute(create_Crayfish1_table)
cursor.execute(create_Crayfish2_table)

# Commit the changes
connection.commit()

df1, df2 = read_excel_multi_index(excel)

site_list = list(df1.columns.get_level_values(0).unique())
site_df1 = []
site_df2 = []

for site in site_list:
    met_1 = df1[site, 'Drawdown'].dropna()
    met_1.insert(0, "Site", [site] * len(met_1.index), True)
    met_1.insert(1, "Method", ["Drawdown"] * len(met_1.index), True)

    met_2 = df1[site, 'Handsearch'].dropna(how='all')
    met_2.insert(0, "Site", [site] * len(met_2.index), True)
    met_2.insert(1, "Method", ["Handsearch"] * len(met_2.index), True)

    met_3 = df1[site, 'Trapping'].dropna(how='all')
    met_3.insert(0, "Site", [site] * len(met_3.index), True)
    met_3.insert(1, "Method", ["Trapping"] * len(met_3.index), True)
    
    site_df1.append(pd.concat([met_1, met_2, met_3]))

for site in site_list:
    sitedb = df2[site].dropna(how='all')
    sitedb.insert(0, "Site", [site] * len(sitedb.index), True)
    site_df2.append(sitedb)

Sheet_1 = pd.concat(site_df1).reset_index(drop=True)
Sheet_2 = pd.concat(site_df2).reset_index(drop=True)
Sheet_1.rename(columns={'Carapace length  (mm)': 'length'}, inplace=True)
Sheet_2.rename(columns={'Carapace length  (mm)': 'length'}, inplace=True)
Sheet_2.rename(columns={'Weight (g)': 'weight'}, inplace=True)

# Creates crayfish1 table
Sheet_1.to_sql("crayfish1", connection, if_exists="append", index=False)
Sheet_2.to_sql("crayfish2", connection, if_exists="append", index=False)

# close the database connection
connection.close()
