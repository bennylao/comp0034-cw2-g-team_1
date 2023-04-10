from pathlib import Path
import pandas as pd
from sqlalchemy import create_engine

def read_excel_multi_index(excel_file):
    """
    This function imports the newly created Excel file in the correct format
    Args:
        excel_file (xlsx): The proj Excel file
    Raises:
        NA
    Returns:
        df1_final (DataFrame): The first sheet in the proj Excel file as a dataframe
        df2_final (DataFrame): The second sheet in the proj Excel file as a dataframe
    """
    df1_final = pd.read_excel(excel_file, header=[0, 1, 2],
                              sheet_name="Sheet_name_1")  # Gets the file as a multi-index dataframe
    df1_final = df1_final.drop(df1_final.columns[:1], axis=1)  # Drops column, which is an index
    df1_final.columns = df1_final.columns.set_names(["Site", "Method", "Info"])  # Adds the names to the levels
    df1_final = df1_final.drop(0).reset_index(drop=True)  # Drops the first row which is all NaN

    df2_final = pd.read_excel(excel_file, header=[0, 1], sheet_name="Sheet_name_2")
    df2_final = df2_final.drop(df2_final.columns[:1], axis=1)
    df2_final.columns = df2_final.columns.set_names(["Site", "Info"])
    df2_final = df2_final.drop(0).reset_index(drop=True)
    return df1_final, df2_final

excel = Path(__file__).parent.joinpath("prepared_datasets.xlsx")
crayfishdb1, crayfishdb2 = read_excel_multi_index(excel)
site_list = list(crayfishdb1.columns.get_level_values(0).unique())
site_df1 = []
site_df2 = []
for site in site_list:
    met_1 = crayfishdb1[site, 'Drawdown'].dropna(how = 'all')
    met_1.insert(0, "Site", [site] * len(met_1.index), True)
    met_1.insert(1, "Method", ["Drawdown"] * len(met_1.index), True)

    met_2 = crayfishdb1[site, 'Handsearch'].dropna(how = 'all')
    met_2.insert(0, "Site", [site] * len(met_2.index), True)
    met_2.insert(1, "Method", ["Handsearch"] * len(met_2.index), True)

    met_3 = crayfishdb1[site, 'Trapping'].dropna(how = 'all')
    met_3.insert(0, "Site", [site] * len(met_3.index), True)
    met_3.insert(1, "Method", ["Trapping"] * len(met_3.index), True)
    site_df1.append(pd.concat([met_1, met_2, met_3]))

for site in site_list:
    sitedb = crayfishdb2[site].dropna(how = 'all')
    sitedb.insert(0, "Site", [site] * len(sitedb.index), True)
    site_df2.append(sitedb)

Sheet_1 = pd.concat(site_df1).reset_index(drop=True)
Sheet_2 = pd.concat(site_df2).reset_index(drop=True)

db_file = Path(__file__).parent.joinpath("../instance/database.db")
engine = create_engine("sqlite:///" + str(db_file), echo=False)

Sheet_1.to_sql("crayfish1", engine, if_exists="append", index=False)
Sheet_2.to_sql("crayfish2", engine, if_exists="append", index=False)