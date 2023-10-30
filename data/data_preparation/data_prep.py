import pandas as pd
import numpy as np
from pathlib import Path


def cleaning_first_2(df_merged):
    """ Opens the mapped multiindex dataframe of the first two sheets, breaks down the columns into
    seperate lists, removes any unnecessary values and the corresponding row, then combines 
    the lists back into a dataframe for cleaned datas

    Args:
        df_merged (DataFrame): data frame containing the first two
                                                spreadsheets mapped.

    Raises:
        NA

    Returns:
        df(DataFrame): the cleaned data frame
        
    """

    # list of all the column subheadings in first three row
    row1 = list(df_merged.columns.get_level_values(0).unique())
    row2 = list(df_merged.columns.get_level_values(1).unique())
    row3 = list(df_merged.columns.get_level_values(2).unique())

    df_list = []
    # Making a for loop to seperate columns
    for i in range(len(row1)):
        for j in range(len(row2)):
            df1 = df_merged[row1[i], row2[j], row3[0]]
            df2 = df_merged[row1[i], row2[j], row3[1]]
            # merging the gender and carpace length
            df = pd.concat((df1, df2), axis=1)
            # Droping any cells which does not contain M & F
            df = df.drop(df[~df[df.columns[0]].isin(['M', 'F'])].index).reset_index(drop=True)
            # adding the new columns onto a list
            df_list.append(df)
    # turning the list back into a dataframe & adding labels for subheading
    df = pd.concat(df_list, axis=1)
    df.columns = df.columns.set_names(["Site", "Method", "Info"])
    return df


def read_excel():
    """
    All the sheets in the excel files are turned into a dataframe

     Returns:
        df1, df2, df3, df4, df5, df6 (DataFrame): The sheets as a dataframe
        sheet (list): The list of sheet names
    """
    excel = Path(__file__).parent.joinpath("Chadwick2020_JAE_Full_Data.xlsx")
    sheet = pd.ExcelFile(excel).sheet_names
    df1 = pd.read_excel(excel, sheet_name=sheet[0])
    df2 = pd.read_excel(excel, sheet_name=sheet[1])
    df3 = pd.read_excel(excel, sheet_name=sheet[2])
    df4 = pd.read_excel(excel, sheet_name=sheet[3])
    df5 = pd.read_excel(excel, sheet_name=sheet[4])
    df6 = pd.read_excel(excel, sheet_name=sheet[5])

    return df1, df2, df3, df4, df5, df6, sheet


def raw_data_check(df, sheet):
    """
    Shows the shape of the initial datafrmes
    """
    i = 0
    for data in df:
        print("\n##### {name} #####".format(name=sheet[i]))
        print("Number of Row: {num}".format(num=data.shape[0]))
        print("Number of Number of Column: {num}\n".format(num=data.shape[1]))
        i = i + 1


def get_unique_list(raw_list):
    """
    Create a list containing unique values from the existing list

     Args:
         raw_list (list): list containing all the headers in the dataframe

     Returns:
         list: contains the unique values in the exisiting list
    """
    unique_list = []
    if not raw_list:
        print("List is empty")
        return np.nan

    # write unique value into unique_list
    for i in raw_list:
        if i in unique_list:
            pass
        else:
            unique_list.append(i)

    return unique_list


def get_column_title(df):
    """
    Create a 2D list of column headers for multi-index

     Args:
         df (dataframe): dataframe containing data from the sheet

     Returns:
         2D list: contains the column headers for spreadsheet 1 and 2
    """
    # get the data in row 0 and 1 and convert it to list
    site = df.iloc[0].values.tolist()
    method = df.iloc[1].values.tolist()
    # get unique list
    method1 = get_unique_list(method)
    site1 = get_unique_list(site)
    col_title = [site1, method1, ["Gender", "Carapace length  (mm)"]]

    return col_title


def data_merge_first_2(df1, df2):
    """
    Merges the two dataframes from the first two spreadsheet and clean the dataframe

    Args:
        df1 (dataframe): dataframe containing data from the first sheet
        df2 (dataframe): dataframe containing data from the second sheet

    Returns:
        dataframe: a merged dataframe with multi-index for the first two spreadsheet
    """
    # create a 2d list for later use in multi-index
    column_title = get_column_title(df1)

    # merge two data sets
    data_merged = pd.concat([df1, df2], axis=1)

    # rearrange column by copying the merged dataframe
    order = []
    for i in range(int(len(data_merged.columns) / 2)):
        order.append(i + 12)
        order.append(i)
    df_merged = data_merged.iloc[:, order].copy()

    # set multi-index column
    df_merged.columns = pd.MultiIndex.from_product(column_title, names=["Site", "Method", "Info"])

    # drop the first two rows
    df_merged = df_merged.drop([0, 1]).reset_index(drop=True)

    # clean the dataframe
    df_merged = cleaning_first_2(df_merged)

    return df_merged


def remove_columns_and_clean(df):
    """
    Drops unnecessary rows and columns

    Args:
        df3 (DataFrame): One of the last 4 data frames

    Returns:
        df (DataFrame): The cleaned dataframe
        info (List): The headings of the second layer of the multi index dataframe
    """
    df = df.drop(df.columns[:2], axis=1)  # Drops the first 2 columns
    info = df.iloc[1].values.tolist()  # List of heading names for the second layer
    i = 0
    while i < len(info):  # Adds the units to the heading while ignoring NaN units
        if df.iloc[2].values.tolist()[i] != df.iloc[2].values.tolist()[i]:
            i += 1
        else:
            info[i] = str(info[i]) + " (" + str(df.iloc[2].values.tolist()[i]) + ")"
            i += 1
    df = df.drop([0, 1, 2]).reset_index(drop=True)  # Drops the first 3 rows
    # Removes all rows that are not M or F. Thus removing the NaNs in the process
    df = df.drop(df[~df[df.columns[0]].isin(['M', 'F'])].index).reset_index(drop=True)

    return df, info


def data_merge_last_4(sheet, df3, df4, df5, df6):
    """
    Merges the last 4 dataframes

    Args:
        sheet (List): A list of the sheet names
        df3 (DataFrame): Dataframe of the 3rd sheet in the excel file
        df4 (DataFrame): Dataframe of the 4rd sheet in the excel file
        df5 (DataFrame): Dataframe of the 5rd sheet in the excel file
        df6 (DataFrame): Dataframe of the 6rd sheet in the excel file

    Returns:
        df_merged (DataFrame): The merged dataframe
    """
    df_list = [df3, df4, df5, df6]
    col_title = []
    for i in range(len(df_list)):  # Look through the dataframes
        df_list[i], info = remove_columns_and_clean(df_list[i])  # Clean the dataframe
        for k in info:
            col_title.append((sheet[i], k))
    df_merged = pd.concat(df_list, axis=1)  # Merges the cleaned dataframe
    # Creates a multi leveled dataframe
    df_merged = pd.DataFrame(df_merged.values.tolist(), columns=pd.MultiIndex.from_tuples(col_title, names=["Site",
                                                                                                            "Info"]))
    return df_merged


def data_merge(df, sheet):
    """
    Merge spreadsheet 1 and 2 together and spreadsheet 3 to 6 together

     Args:
         df (list): a list containing all the dataframes
         sheet (list): a list containing the spreadsheet names

     Returns:
         df1 (dataframe): a merged dataframe of spreadsheet 1 and 2
         df2 (dataframe): a merged dataframe of spreadsheet 3 to 6
    """
    df1 = data_merge_first_2(df[0], df[1])
    df2 = data_merge_last_4(sheet[2:], df[2], df[3], df[4], df[5])

    return df1, df2


def get_unique_value(look_up_col, df_name, df):
    """
    Get unique values in dataframe and show the unique values by list

     Args:
         look_up_col (str): header of the column looking for
         df_name (str): name of the dataframe
         df (dataframe): the interested dataframe

    """
    list_unique = []
    for info in df.columns:
        if look_up_col in info:
            value_in_column = df.loc[:, info].unique()
            for value in value_in_column:
                if value not in list_unique:
                    list_unique.append(value)
    print("\nUnique value for gender in {name}:\n{list}".format(name=df_name, list=list_unique))


def final_check(df1, df2):
    """
    Check if there is any row in dataframes containing all NaN and check the unique values in Column"Gender"

    Args:
        df1 (dataframe): dataframe1
        df2 (dataframe): dataframe2

    """
    print("\nCount of rows in {name} where all columns are empty\n{count}".format(name="dataframe1",
                                                                                  count=df1.isna().all(axis=1).sum()))
    print("\nCount of rows in {name} where all columns are empty\n{count}".format(name="dataframe2",
                                                                                  count=df2.isna().all(axis=1).sum()))
    get_unique_value("Gender", "dataframe 1", df1)
    get_unique_value("Gender", "dataframe 2", df2)


def sex_ratio(df1, df2):
    """
    For the first dataframe: Shows the gender ratio for the site and trapping method
    For the second dataframe: Shows the gender ratio for the site
    Args:
        df1 (DataFrame): The first 2 sheets that were merged and cleaned
        df2 (DataFrame): The last 4 sheets that were merged and cleaned 
    """
    df_list = [df1, df2]
    i = 1
    for df in df_list:#Looks through the dataframes
        print("\nSex Ratios of Dataframe {num}".format(num=i))
        i = 1 + 1
        for info in df.columns:
            if "Gender" in info:#Checks the column named gender
                print(df[info].value_counts())#Prints the ratio


def average_length(df1, df2):
    """
    Shows the avarage length for each site or for each site and the trapping method
    Args:
        df1 (DataFrame): The first 2 sheets that were merged and cleaned
        df2 (DataFrame): The last 4 sheets that were merged and cleaned 
    """
    df_list = [df1, df2]
    length_method_mean = []
    i = 1
    for df in df_list:#Looks through the dataframes
        length_method_mean.clear()
        print("\naverage length for Dataframe {num}".format(num=i))
        i = 1 + 1
        for info in df.columns:
            if "Carapace length  (mm)" in info:
                length_method_mean.append(df[info].mean())#Adds the average to the list length_method_mean
        print(length_method_mean)#Shows the averages as a list


def average_weight(df):
    """
    Shows the avarage weight for each site using the second data frame
    Args:
        df (DataFrame): The last 4 sheets that were merged and cleaned 
    """
    weight_mean = []
    for info in df.columns:
        if "Weight (g)" in info:
            weight_mean.append(df[info].mean())

    print("\naverage weight of each site")
    print(weight_mean)#Shows the averages as a list


def data_summary(df1, df2):
    """
    Calls all the statistics functions
    Args:
        df1 (DataFrame): The first 2 sheets that were merged and cleaned
        df2 (DataFrame): The last 4 sheets that were merged and cleaned 
    """
    sex_ratio(df1, df2)
    average_length(df1, df2)
    average_weight(df2)


def export_excel(df1, df2):
    """Function created export the cleaned data frame back into excel

    Args:
        df1 (DataFrame): dataframe of first two sheets
        df2 (DataFrame): dataframe of last 4 sheets

    Raises:
        NA

    Returns:
        xlsx : export of the datframes to excel
        
    """
    output = Path(__file__).parent.joinpath('prepared_datasets.xlsx')
    with pd.ExcelWriter(output) as writer:
        # the row index cannot be eliminated as the column is multi index
        df1.to_excel(writer, sheet_name='Sheet_name_1')
        df2.to_excel(writer, sheet_name='Sheet_name_2')


def read_excel_multi_index(exl_file):
    """
    This function imports the newly created excel file in the correct format
    Args:
        exl_file (xlsx): The new excel file

    Raises:
        NA

    Returns:
        df1_final (DataFrame): The first sheet in the new excel file as a dataframe
        df2_final (DataFrame): The second sheet in the new excel file as a dataframe
    """
    df1_final = pd.read_excel(exl_file, header=[0, 1, 2], sheet_name="Sheet_name_1")#Gets the file as a multi-index dataframe
    df1_final = df1_final.drop(df1_final.columns[:1], axis=1)#Drops column, which is an index
    df1_final.columns = df1_final.columns.set_names(["Site", "Method", "Info"])#Adds the names to the levels
    df1_final = df1_final.drop(0).reset_index(drop=True)#Drops the first row which is all NaN

    df2_final = pd.read_excel(exl_file, header=[0, 1], sheet_name="Sheet_name_2")
    df2_final = df2_final.drop(df2_final.columns[:1], axis=1)
    df2_final.columns = df2_final.columns.set_names(["Site", "Info"])
    df2_final = df2_final.drop(0).reset_index(drop=True)

    return df1_final, df2_final


if __name__ == "__main__":
    df1_raw, df2_raw, df3_raw, df4_raw, df5_raw, df6_raw, sheet_name = read_excel()
    df_raw_all = [df1_raw, df2_raw, df3_raw, df4_raw, df5_raw, df6_raw]
    raw_data_check(df_raw_all, sheet_name)
    df1_merged, df2_merged = data_merge(df_raw_all, sheet_name)

    final_check(df1_merged, df2_merged)
    data_summary(df1_merged, df2_merged)
    # export to excel
    export_excel(df1_merged, df2_merged)
    output = Path(__file__).parent.joinpath('prepared_datasets.xlsx')
    read_excel_multi_index(output)  #This is not needed for this coursework but when we start actually using the
                                    #cleaned dataframe we need to use this function to get the dataframe in correct format
    print("\n##### Prepped DataFrame 1 #####")
    print(df1_merged)
    print("\n##### Prepped DataFrame 2 #####")
    print(df2_merged)
