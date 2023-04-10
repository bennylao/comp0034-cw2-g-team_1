import pandas as pd


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
