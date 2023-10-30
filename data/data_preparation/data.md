# Data preparation and understanding

### Format of the original dataset:
* The original dataset is divided into six sheets
* The first two sheets contain the carapace lengths and the sex for all *methods* at each site
* The last four sheets contain the sweep no., "crayfish", gender, carapace length, and weight for each site
* All sheets have a merged cell at the top containing the title
* In the first two sheets, the column sizes vary

### "Cleanliness" of the original dataset:
* We decided to null all rows which included juvenile and hatchling data
* Any rows with all NaN values were dropped to trim the size of the dataset
* There were no missing values for any identified crayfish (gender, carapace length, and weight values)

### Usefulness of the original dataset:

Key questions:
1. Which sites are at a high risk due to large populations of signal crayfish? 
2. What is the best method to capture female signal crayfish? 
3. What is the average size and weight of these crayfish? 
4. What percentage of crayfish are female? (the demographic) 
5. Where is the best site to catch specific types of signal crayfish?

Most columns are useful in helping answer our key questions:

| Attribute/column name | What key questions can this help answer? |
| :-------------------: | :--------------------------------------: |
| Carapace length for all methods at each site | 1, 3, 5 |
| Sex for all methods at each site | 1, 2, 4, 5 |
| Sweep no. for each site	| N/A |
| “Crayfish” for each site | N/A |
| Gender for each site	| 2, 4, 5 |
| Carapace length for each site	| 3, 5 |
| Weight for each site	| 3, 5 |

However, in the last four sheets of the .xlsx file, the “SWEEP NO.” and “crayfish” columns are not useful, so we dropped them.

Furthermore, we are only interested in data for adult crayfish, so we decided to replace the juvenile and hatchling data with null values.

### Processing the first two sheets:
* Reformatted as a multi-index dataframe with the main headings being the site names
* Formatted as a multi-index as there are multiple sites that need to be looked at
* Underneath the site names, we have the three trapping methods
* And finally, underneath each trapping method we have sex and length columns
* Having these values in separate columns rather than a tuple will make the analysis easier – it will make plotting graphs easier
* In terms of cleaning, we removed any data that was not for male and female crayfish
* NaN values can still be seen at the bottom of the dataframe because the columns sizes vary

### Processing the last four sheets:
* Reformatted as a multi-index dataframe with the main headings being the site names
* Formatted as a multi-index as there are multiple sites that need to be looked at
* Underneath the site names, we have gender, carapace length, and weight columns
* Having these values in separate columns rather than a tuple will make the analysis easier – it will make plotting graphs easier
* In terms of cleaning, we removed any data that was not for male and female crayfish

### Final output:
* The final outputs are two multi-index dataframes *df1* and *df2*
* These are then merged together and exported as an *prepared_datasets.xlsx* file with two sheets
