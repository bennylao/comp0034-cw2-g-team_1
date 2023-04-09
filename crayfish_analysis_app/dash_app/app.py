import pandas as pd
from pathlib import Path
from dash import dash, html, dcc, Input, Output, State, ctx
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import numpy as np


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


def count_crayfish(df, site, length_min, length_max, weight_min, weight_max, sex):
    """
    This function counts the number of male/female/both crayfish that is between a given
    lengths and weights
    Args:
        df (DataFrame): The dataframe that holds our data
        site (string): This is the site that is going to be searched through
        length_min (float): The minimum length for the search
        length_max (float): The maximum length for the search
        weight_min (float): The minimum weight for the search
        weight_max (float): The maximum weight for the search
        sex (list): Whether to search for only male, female or both
    Raises:
        NA
    Returns:
        num (int): The number of crayfish that were found that fit the conditions provided
    """
    num = sum((df[site, 'Carapace length  (mm)'] >= length_min) &
              (df[site, 'Carapace length  (mm)'] <= length_max) &
              (df[site, 'Weight (g)'] >= weight_min) &
              (df[site, 'Weight (g)'] <= weight_max) &
              (df[site, 'Gender'].isin(list(sex)))  # Finding the number of crayfish that meet the condition
              )
    return num


def find_min_and_max(df, attribute):
    """
    This function find the minimum and maximum value for an attribute of the crayfish
    Args:
        df (DataFrame): The dataframe that holds our data
        attribute (string): The size (Carapace length  (mm))
                            or the weight (Weight (g)) of the crayfish
    Raises:
        NA
    Returns:
        minimum (int): The minimum value for the attribute in the dataframe
        maximum (int): The maximum value for the attribute in the dataframe
    """
    # Finding the lowest value for the attribute for each site
    list_min = df.iloc[:, df.columns.get_level_values(1) == attribute].min()
    list_max = df.iloc[:, df.columns.get_level_values(1) == attribute].max()
    # Finding the lowest value for the attribute for all sites
    minimum = min(list(list_min))
    maximum = max(list(list_max))

    return minimum, maximum


def set_value_if_none(length_min, length_max, weight_min, weight_max):
    """
    Used give the bar chart their default search value or
    sets new search value given by user on the website
    Args:
        length_min (float): The user input form website
        length_max (float): The user input form website
        weight_min (float): The user input form website
        weight_max (float): The user input form website
    Raises:
        NA
    Returns:
        length_min (float): return the minimum length given by user
                            or the minimum length in the dataframe
                            if nothing is given
        length_max (float): return the maximum length given by user
                            or the maximum length in the dataframe
                            if nothing is given
        weight_min (float): return the minimum weight given by user
                            or the minimum weight in the dataframe
                            if nothing is given
        weight_max (float): return the maximum weight given by user
                            or the maximum weight in the dataframe
                            if nothing is given
    """
    # set default value
    if length_min is None:
        length_min = length_minimum
    if length_max is None:
        length_max = length_maximum
    if weight_min is None:
        weight_min = weight_minimum
    if weight_max is None:
        weight_max = weight_maximum

    return length_min, length_max, weight_min, weight_max


def num_m_f(df, site):
    """
    Gives the number of males and females caught in the site
    Args:
        df (DataFrame): The dataframe that holds our data
        site (string): The site where the crayfish were caught
    Raises:
        NA
    Returns:
        count_f (int): Number of female crayfish in the site
        count_m (int): Number of male crayfish in the site
    """
    count_f = list((df[site] == "F").sum())
    count_f = sum(count_f)  # Find the total number of females

    count_m = list((df[site] == "M").sum())
    count_m = sum(count_m)  # Find the total number of males

    return count_f, count_m


def normal_dist_probability(x, mu, sigma):
    prob = (np.pi * sigma) * np.exp(-0.5 * ((x - mu) / sigma) ** 2)
    return prob


def mean_stats(df, site):
    """
    Gives the average length of the male and female crayfish in the site
    Args:
        df (DataFrame): The dataframe that holds our data
        site (string): The site that is going to be searched
    Raises:
        NA
    Returns:
        mean_f (float): The average length of the female crayfish
        mean_m (float): The average length of the male crayfish
    """
    count_f, count_m = num_m_f(df, site)

    mean_f = round((sum(df.loc[df[site, 'Drawdown', 'Gender'] == 'F', (site, 'Drawdown', 'Carapace length  (mm)')])
                    + sum(
                df.loc[df[site, 'Handsearch', 'Gender'] == 'F', (site, 'Handsearch', 'Carapace length  (mm)')])
                    + sum(df.loc[df[site, 'Trapping', 'Gender'] == 'F',
                                 (site, 'Trapping', 'Carapace length  (mm)')])) / count_f,
                   2)  # Average length for female

    mean_m = round((sum(df.loc[df[site, 'Drawdown', 'Gender'] == 'M', (site, 'Drawdown', 'Carapace length  (mm)')])
                    + sum(
                df.loc[df[site, 'Handsearch', 'Gender'] == 'M', (site, 'Handsearch', 'Carapace length  (mm)')])
                    + sum(df.loc[df[site, 'Trapping', 'Gender'] == 'M',
                                 (site, 'Trapping', 'Carapace length  (mm)')])) / count_m, 2)  # Average length for male

    return mean_f, mean_m


# function to open modal
def toggle_modal(n1, is_open):
    """
    Opens the pop-up that explains why the chart is made
    Args:
        n1 (boolean): Acts as a swtich
        is_open (string): The information that pops up
    Raises:
        NA
    Returns:
        is_open (float): The information is given when pressed
    """
    if n1:
        return not is_open
    return is_open


# import data
excel = Path(__file__).parent.joinpath("prepared_datasets.xlsx")
df1, df2 = read_excel_multi_index(excel)
site_list = list(df2.columns.get_level_values(0).unique())
length_minimum, length_maximum = find_min_and_max(df2, 'Carapace length  (mm)')
weight_minimum, weight_maximum = find_min_and_max(df2, 'Weight (g)')

# Creates the Dash app
def create_dash_app(flask_app):
    """Creates Dash as a route in Flask
    :param flask_app: A confired Flask app
    :return dash_app: A configured Dash app registered to the Flask app
    """
    # Register the Dash app to a route '/dashboard/' on a Flask app
    app = dash.Dash(__name__, server=flask_app, url_base_pathname="/dashboard/", meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1",}], external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.BOOTSTRAP],)

    app.layout = dbc.Container(

        style={"backgroundColor": "white"},

        fluid=True,
        children=[

            # create garbage id to carry the output from app.clientside_callback
            dcc.Store(id='title-1'),
            dcc.Store(id='title-2'),
            dcc.Store(id='title-3'),
            dcc.Store(id='title-4'),

            # Create dashboard title
            dbc.Card([
                dbc.Row([
                    dbc.Col([
                        html.H1("Crayfish Analysis Dashboard",
                                style={"textAlign": "center",
                                    'border': '2px solid #333',
                                    "width": "50%",
                                    "margin": "0 auto",
                                    "backgroundColor": "white"},
                                )
                    ], width=12)
                ]),
            ],
                body=True,
                className="mb-3",
                style={'border-color': 'white'}
            ),

            # Create a card group for app description
            dbc.CardGroup(
                [
                    dbc.Card(
                        [
                            dbc.CardImg(
                                src="https://assets.publishing.service.gov.uk/government/uploads/system/uploads"
                                    "/image_data/file/139418/web_crayfish_2.jpg",
                                top=True),
                            dbc.CardBody(
                                [
                                    html.P(
                                        "Increasing populations of invasive signal crayfish can harm ecosystems and "
                                        "biodiversity.",
                                        className="card-text",
                                    ),

                                    dbc.Button("Pie Charts", outline=True, color="primary", className="me-1", id='btn-pie'),
                                ]
                            )
                        ],
                        body=True,
                        className="mb-3",

                    ),

                    dbc.Card(
                        [
                            dbc.CardImg(
                                src="https://upload.wikimedia.org/wikipedia/commons/thumb/7/72"
                                    "/Signal_crayfish_female_Pacifastacus_leniusculus.JPG/800px"
                                    "-Signal_crayfish_female_Pacifastacus_leniusculus.JPG",
                                top=True),
                            dbc.CardBody(
                                [
                                    html.P(
                                        "Monitoring signal crayfish populations is important for both scientists and "
                                        "fishermen.",
                                        className="card-text",
                                    ),
                                    dbc.Button("Bar Chart", outline=True, color="primary", className="me-1", id='btn-bar'),
                                ]
                            )
                        ],
                        body=True,
                        className="mb-3",

                    ),

                    dbc.Card(
                        [
                            dbc.CardImg(
                                src="https://st2.depositphotos.com/1075946/7097/i/600/depositphotos_70975345-stock-photo"
                                    "-student-taking-sample-of-water.jpg",
                                top=True),
                            dbc.CardBody(
                                [
                                    html.P(
                                        "This dashboard aims to help scientists monitor crayfish populations and help "
                                        "fishermen identify specific populations of crayfish so that they can fish more "
                                        "sustainably.",
                                        className="card-text",
                                    ),
                                    dbc.Button("Distribution Curves", outline=True, color="primary", className="me-1",
                                            id='btn-dist'),
                                ]
                            )
                        ],
                        body=True,
                        className="mb-3",

                    ),

                    dbc.Card(
                        [
                            dbc.CardImg(src="https://live.staticflickr.com/8434/7651334456_5cae4f882c_b.jpg", top=True),
                            dbc.CardBody(
                                [
                                    html.P(
                                        "User-friendly data visualisations are included which help to answer the key "
                                        "questions for crayfish research and fishermen.",
                                        className="card-text",
                                    ),
                                    dbc.Button("Line Graph", outline=True, color="primary", className="me-1",
                                            id='btn-line'),
                                ]
                            )
                        ],
                        body=True,
                        className="mb-3",

                    ),
                ], style={"width": "50%", "margin": "0 auto"},
            ),

            # Pie Chart
            dbc.Card([
                dbc.Stack([html.H4("Sex Ratio and Trapping Method Pie Charts", id='pie-title'),
                        dbc.Button(id="pie-modal-button", class_name="bi bi-question-circle", outline=True, n_clicks=0)],
                        direction="horizontal"),

                html.H6("Site:"),
                dcc.Dropdown(site_list, 'DGB2016',
                            id='pie-site-selection'),

                dcc.Graph(id='pie-chart-sex-ratio'),
                dcc.Graph(id='pie-chart-method'),
            ],
                body=True,
                className="mb-3",
                style={"width": "50%", "margin": "0 auto"},

            ),

            # Bar Chart
            dbc.Card([
                dbc.Stack([html.H4("Bar Chart for User-Selected Features", id='bar-title'),
                        dbc.Button(id="bar-modal-button", class_name="bi bi-question-circle", outline=True, n_clicks=0)],
                        direction="horizontal"),

                dbc.Card([
                    html.Div([

                        "Carapace Length: ",
                        dcc.Input(id='bar-carapace-length-min', type='number', min=0, placeholder="Minimum Length"),
                        " to ",
                        dcc.Input(id='bar-carapace-length-max', type='number', min=0, placeholder="Maximum Length")
                    ]),

                    html.Div([
                        "Weight: ",
                        dcc.Input(id='bar-weight-min', type='number', min=0, placeholder="Minimum Weight"),
                        " to ",
                        dcc.Input(id='bar-weight-max', type='number', min=0, placeholder="Maximum Weight")
                    ]),

                    dbc.Stack([
                        html.Div("Sex:"),
                        dbc.Checklist(
                            id='bar-sex',
                            options=[
                                {"label": "M", "value": 'M'},
                                {"label": "F", "value": 'F'},
                            ],
                            value=['M', 'F'],
                            label_checked_style={"color": "green"},
                            input_checked_style={
                                "backgroundColor": "green",
                                "borderColor": "green",
                            },
                            inline=True
                        ),
                    ],
                        direction="horizontal",
                        gap=3,
                    ),

                    html.Button('Apply Filters', id='bar-update-button'),
                ],
                    body=True,
                    className="mb-3",
                ),

                dcc.Graph(id='bar-chart'),
            ],
                body=True,
                className="mb-3",
                style={"width": "50%", "margin": "0 auto"},
            ),

            # Distribution Curves
            dbc.Card([
                dbc.Stack([html.H4("Carapace Length and Weight Distributions", className="card-title", id='dist-title'),
                        dbc.Button(id="dist-modal-button", class_name="bi bi-question-circle", outline=True,
                                    n_clicks=0)],
                        direction="horizontal"),
                html.H6("Sites:"),
                dcc.Dropdown(site_list, site_list, id='distribution-site', multi=True),
                dbc.Stack([
                    html.H6("Sex:"),
                    dbc.Checklist(id='dist-sex', options=[{"label": "M", "value": 'M'}, {"label": "F", "value": 'F'}],
                                value=['M', 'F'],
                                label_checked_style={"color": "green"},
                                input_checked_style={"backgroundColor": "green", "borderColor": "green", },
                                inline=True
                                ),
                ],
                    direction="horizontal",
                    gap=3,
                ),
                html.H6("Data Types:"),
                dbc.Button("Carapace Length", id='dist-length', value='Carapace length  (mm)', outline=True,
                        color="primary", size='sm'),
                dbc.Button("Weight", id='dist-weight', value='Weight (g)', outline=True, color="primary", size='sm'),
                dcc.Graph(id='normal-distribution'),

                # Create a store to memorise the previous button pressed by users
                # store will be clear once the browser is refreshed
                dcc.Store(id='dist-btn-id-prev')
            ],
                body=True,
                className="mb-3",
                style={"width": "50%", "margin": "0 auto"},
            ),

            # Population Graph
            dbc.Card([

                dbc.Stack([html.H4("Population Trend", id='line-title'),
                        dbc.Button(id="line-modal-button", class_name="bi bi-question-circle", outline=True,
                                    n_clicks=0)],
                        direction="horizontal"),
                dbc.Stack([
                    html.H6("Sex:"),
                    dbc.Checklist(
                        id='line-sex',
                        options=[
                            {"label": "M", "value": 'M'},
                            {"label": "F", "value": 'F'},
                        ],
                        value=['M', 'F'],
                        label_checked_style={"color": "green"},
                        input_checked_style={
                            "backgroundColor": "green",
                            "borderColor": "green",
                        },
                        inline=True
                    ),
                ],
                    direction="horizontal",
                    gap=3,
                ),

                dcc.Graph(id='line-graph-pop')
            ],
                body=True,
                className="mb-3",
                style={"width": "50%", "margin": "0 auto"},
            ),

            # Create modals for each graph
            # Modal is opened when the icon displaying as a question mark is clicked

            dbc.Modal(
                [
                    dbc.ModalHeader(dbc.ModalTitle("Sex Ratio and Trapping Method Pie Charts")),
                    dbc.ModalBody("These pie charts are used to answer the following key questions:"),
                    dbc.ModalBody("-What percentage of crayfish are female?"),
                    dbc.ModalBody("-Which trapping method captures the most female signal crayfish?"),
                    dbc.ModalBody(" "),
                    dbc.ModalBody("Select the site you wish to view data for from the dropdown."),
                ],
                id="pie-modal",
                size="xl",
                is_open=False,
            ),
            dbc.Modal(
                [
                    dbc.ModalHeader(dbc.ModalTitle("Bar Chart for User-Selected Features")),
                    dbc.ModalBody("This bar chart is used to answer the following key questions:"),
                    dbc.ModalBody("-Which sites have the largest populations of signal crayfish?"),
                    dbc.ModalBody("-Which site has the highest number of specific crayfish based on fishermen's needs"),
                    dbc.ModalBody(" "),
                    dbc.ModalBody(
                        "Use the carapace length range, weight range, and sex checkboxes to specify which crayfish you "
                        "would like to view data for. Press the 'Apply Filters' button to view the specific bar charts"),
                ],
                id="bar-modal",
                size="xl",
                is_open=False,
            ),
            dbc.Modal(
                [
                    dbc.ModalHeader(dbc.ModalTitle("Carapace Length and Weight Distributions")),
                    dbc.ModalBody("These distribution curves are used to answer the following key questions:"),
                    dbc.ModalBody("-How are the weights and lengths for the crayfish distributed for each site?"),
                    dbc.ModalBody("-How are the weights and lengths for the crayfish distributed for each sex?"),
                    dbc.ModalBody(" "),
                    dbc.ModalBody(
                        "Use the sites dropdown, sex checkboxes, and data types checkboxes to specify which crayfish you "
                        "would like to view data for."),
                ],
                id="dist-modal",
                size="xl",
                is_open=False,
            ),
            dbc.Modal(
                [
                    dbc.ModalHeader(dbc.ModalTitle("Population Trend")),
                    dbc.ModalBody("This line graph is used to answer the following key question:"),
                    dbc.ModalBody("-How has the population of signal crayfish changed over time?"),
                    dbc.ModalBody(" "),
                    dbc.ModalBody("Use the sex checkboxes to specify which crayfish you would like to view data for."),
                ],
                id="line-modal",
                size="xl",
                is_open=False,
            ),

        ],
    )


    @app.callback(
        Output('bar-chart', 'figure'),
        Input('bar-update-button', 'n_clicks'),
        [
            State('bar-carapace-length-min', 'value'),
            State('bar-carapace-length-max', 'value'),
            State('bar-weight-min', 'value'),
            State('bar-weight-max', 'value'),
            State('bar-sex', 'value')
        ]
    )
    def update_bar_chart(_click, length_min, length_max, weight_min, weight_max, sex):
        """
        This function is used to update the bar chart based on the selected site
        Args:
            _click: useless variable passed from callback
        length_min (float): minimum length of crayfish
        length_max (float): maximum length of crayfish
        weight_min (float): minimum weight of crayfish
        weight_max (float): maximum weight of crayfish
        sex (list): a list contains 'M' or 'F'
        Raises:
            NA
        Returns:
            fig(class): the updated bar chart  for the selection
        """
        # assigning default value when there is no selection
        # shows everything in the dataframe
        count = []

        length_min, length_max, weight_min, weight_max = set_value_if_none(length_min, length_max, weight_min, weight_max)
        # go through dataframe and find values which comply with the selection
        for site in site_list:
            count.append(count_crayfish(df2, site, length_min, length_max, weight_min, weight_max, sex))
        # generate the graph
        fig = go.Figure()
        # enabling the hover-over
        fig.add_trace(go.Bar(
            x=site_list,
            y=count,
        ))
        # customise the hoverover
        fig.update_traces(hovertemplate='Site: %{x}<br>Number of Crayfish Caught: %{y}  <extra></extra>')
        # additional customisation to the chart
        fig.update_layout(
            xaxis_title='Site',
            yaxis_title="Number of Crayfish Caught",
            font=dict(
                family="Times New Roman",
                size=18),
            yaxis_range=[0, 700],
            paper_bgcolor="white",
        ),

        return fig


    @app.callback(
        Output('pie-chart-sex-ratio', 'figure'),
        Output('pie-chart-method', 'figure'),
        Input('pie-site-selection', 'value')
    )
    def update_pie_chart(site):
        """
        This function is used to update the pie chart based on the selected site
        Args:
            site (list) : The desired site to be displayed
        Raises:
            NA
        Returns:
            fig1, fig2 (class): the updated pie charts for the chosen sites
        """
        # finding the total number of male and female crayfish at each site
        count_f, count_m = num_m_f(df1, site)
        # finding the number of crayfish based on trapping method
        count_t = [df1[site, 'Drawdown', 'Gender'].count(), df1[site, 'Handsearch', 'Gender'].count(),
                df1[site, 'Trapping', 'Gender'].count()]
        # finding the mean stats on the site
        mean_f, mean_m = mean_stats(df1, site)
        # generating the graph and customising the male/female chart
        fig1 = go.Figure(go.Pie(labels=['Female', 'Male'],
                                values=[count_f, count_m],
                                title='Sex Ratio for <br> ' + site,
                                hole=.5,
                                customdata=[mean_f, mean_m],
                                hovertemplate="Average length (mm): %{customdata}<extra></extra>"))
        # additional customisation to the chart
        fig1.update_layout(
            font=dict(
                family="Times New Roman",
                size=18,
            ),
            paper_bgcolor="white",

        )
        # generating the graph and customising the trapping chart
        fig2 = go.Figure(go.Pie(labels=['Drawdown', 'Handsearch', 'Trapping'],
                                values=count_t,
                                hole=.6,
                                title='Trapping Methods in <br>' + site,
                                customdata=[round(df1[site, 'Drawdown', 'Carapace length  (mm)'].mean(), 2),
                                            round(df1[site, 'Handsearch', 'Carapace length  (mm)'].mean(), 2),
                                            round(df1[site, 'Trapping', 'Carapace length  (mm)'].mean(), 2)],
                                hovertemplate="Average length (mm): %{customdata}<extra></extra>"))
        # additional customisation to the chart
        fig2.update_layout(
            font=dict(
                family="Times New Roman",
                size=18,
            ),
            paper_bgcolor="white",
        )

        return fig1, fig2


    @app.callback(
        Output('normal-distribution', 'figure'),
        Output('dist-btn-id-prev', 'data'),
        Input('distribution-site', 'value'),
        Input('dist-length', 'n_clicks'),
        Input('dist-weight', 'n_clicks'),
        Input('dist-sex', 'value'),
        Input('dist-btn-id-prev', 'data'),
    )
    def update_distribution(site_selection, _btn_length, _btn_weight, sex, button_id_prev):
        """
        This function is used to update the weight and length distribution chart based on filter
        Args:
            site_selection (list) : The desired site to be displayed
            _btn_length: useless variable from callback
            _btn_weight: useless variable from callback
            sex (list) : The desired sex to be displayed
            button_id_prev (str): id which store the users previous selection
        Raises:
            Exception error: neither length and weight is selected to be shown
        Returns:
            fig (class): the updated distribution graph
            button_id_prev (str): id which store the users the latest selection
        """

        button_id = ctx.triggered_id
        # avoid button id = site selection when dropdown is triggered

        # setting the default display of the chart/the latest selection
        if button_id is None:
            button_id = 'dist-length'
            button_id_prev = button_id
        elif button_id in ['dist-length', 'dist-weight']:
            button_id_prev = button_id
        else:
            button_id = button_id_prev
        # checking if weight or length has been selected
        if button_id == 'dist-length':
            info = 'Carapace length  (mm)'
        elif button_id == 'dist-weight':
            info = 'Weight (g)'
        else:
            raise Exception("Error Occurred")
        # creating a list of data to be displayed
        num_point = 1000
        dist_data_list = []
        dist_mean_list = []
        dist_sd_list = []
        # checking if site is in the list
        if isinstance(site_selection, list):
            pass
        else:
            site_selection = list(site_selection)

        # Calculate mean and standard deviation of the data set for graph output
        for site in site_selection:
            sub_df = df2[df2[site, 'Gender'].isin(list(sex))]
            mean = sub_df[site, info].mean()
            sd = sub_df[site, info].std()
            data = np.random.normal(mean, sd, num_point)
            # Adapted from code from 'Borislav Hadzhiev' on the bobbyhadz blog at
            # https://stackoverflow.com/questions/23096417/python-removing-all-negative-values-in-array
            # Accessed 01/02/22
            data = np.sort(data)
            data = data[np.searchsorted(data, 0):]
            dist_data_list.append(data)
            dist_mean_list.append(mean)
            dist_sd_list.append(sd)

        fig = go.Figure()
        i = 0
        # enabiling the hoverover feature
        for data in dist_data_list:
            fig.add_trace(go.Scatter(x=data, y=normal_dist_probability(data, dist_mean_list[i], dist_sd_list[i]),
                                    name=site_selection[i]))
            i += 1

        # customising the chart appreadence and features
        fig.update_layout(
            # title="Title",
            xaxis_title=info,
            yaxis_title="Probability Density",
            legend_title="Site",
            font=dict(
                family="Times New Roman",
                size=18),
            yaxis_range=[0, 30],
            paper_bgcolor="white",

        ),
        # customising the hover over feature
        fig.update_traces(hovertemplate=info + ': %{x} <br>Probability Density: %{y}')

        return fig, button_id_prev


    @app.callback(
        Output('line-graph-pop', 'figure'),
        [Input('line-sex', 'value')]
    )
    def update_pop_graph(option):
        """
        This function is used to update the population line chart on the app depending on the filer
        Args:
            option (list) : The desired data the users wish to see on the chart
        Raises:
            NA
        Returns:
            fig (class): the updated linegraph graph
        """
        # finding the total number of male and female crayfish at each site
        count_2016_f, count_2016_m = num_m_f(df1, 'DGB2016')
        count_2017_f, count_2017_m = num_m_f(df1, 'DGB2017')
        # updating chart to show population of both male and female
        if option == ["M", "F"] or option == ["F", "M"]:
            fig = go.Figure(data=go.Scatter(x=[2016, 2017],
                                            y=[count_2016_f + count_2016_m,
                                            count_2017_f + count_2017_m]))
        # updating chart to show population of male
        elif option == ["M"]:
            fig = go.Figure(data=go.Scatter(x=[2016, 2017],
                                            y=[count_2016_m,
                                            count_2017_m]))
        # updating chart to show population of female
        elif option == ["F"]:
            fig = go.Figure(data=go.Scatter(x=[2016, 2017],
                                            y=[count_2016_f,
                                            count_2017_f]))
        # updating chart to make it empty
        else:
            fig = go.Figure()
        # customising the chart by addint title, axis etc
        fig.update_layout(
            title={"text": 'Population Trend for Site DGB',
                'x': 0.5},

            xaxis_title="Year",
            yaxis_title="Population",
            font=dict(
                family="Times New Roman",
                size=18),
            yaxis_range=[count_2017_m - 100, count_2016_f + count_2016_m + 100],
            paper_bgcolor="white",
        ),
        # enabiling hover over feature
        fig.update_xaxes(dtick="M2")
        fig.update_traces(hovertemplate='Year: %{x} <br>Population: %{y}<extra></extra>')
        return fig


    # callback for modal
    app.callback(
        Output("pie-modal", "is_open"),
        Input("pie-modal-button", "n_clicks"),
        State("pie-modal", "is_open"),
    )(toggle_modal)

    app.callback(
        Output("bar-modal", "is_open"),
        Input("bar-modal-button", "n_clicks"),
        State("bar-modal", "is_open"),
    )(toggle_modal)

    app.callback(
        Output("dist-modal", "is_open"),
        Input("dist-modal-button", "n_clicks"),
        State("dist-modal", "is_open"),
    )(toggle_modal)

    app.callback(
        Output("line-modal", "is_open"),
        Input("line-modal-button", "n_clicks"),
        State("line-modal", "is_open"),
    )(toggle_modal)

    # callback for scrolling button
    app.clientside_callback(
        """
        function(clicks, elemid) {
            document.getElementById(elemid).scrollIntoView({
            behavior: 'smooth'
            });
        }
        """,
        Output('title-1', 'data'),
        [Input('btn-pie', 'n_clicks')],
        [State('pie-title', 'id')],
        prevent_initial_call=True,
    )

    app.clientside_callback(
        """
        function(clicks, elemid) {
            document.getElementById(elemid).scrollIntoView({
            behavior: 'smooth'
            });
        }
        """,
        Output('title-2', 'data'),
        [Input('btn-bar', 'n_clicks')],
        [State('bar-title', 'id')],
        prevent_initial_call=True,
    )

    app.clientside_callback(
        """
        function(clicks, elemid) {
            document.getElementById(elemid).scrollIntoView({
            behavior: 'smooth'
            });
        }
        """,
        Output('title-3', 'data'),
        [Input('btn-dist', 'n_clicks')],
        [State('dist-title', 'id')],
        prevent_initial_call=True,
    )

    app.clientside_callback(
        """
        function(clicks, elemid) {
            document.getElementById(elemid).scrollIntoView({
            behavior: 'smooth'
            });
        }
        """,
        Output('title-4', 'data'),
        [Input('btn-line', 'n_clicks')],
        [State('line-title', 'id')],
        prevent_initial_call=True,
    )

    if __name__ == '__main__':
        app.run_server(debug=True)

