import dash
import bs4
import pandas as pd
import time
import random as ran
import plotly.express as px
from dash import dcc
from dash import html
import requests

app = dash.Dash(__name__)

############################################ scraping functions ###################################
def scrape_mblock(movie_block):
    movieb_data ={}

    try:
        movieb_data['name'] = movie_block.find('a').get_text() # Name of the movie
    except:
        movieb_data['name'] = None

    try:
        movieb_data['year'] = str(movie_block.find('span',{'class': 'lister-item-year'}).contents[0][1:-1]) # Release year
    except:
        movieb_data['year'] = None

    try:
        movieb_data['rating'] = float(movie_block.find('div',{'class':'inline-block ratings-imdb-rating'}).get('data-value')) #rating
    except:
        movieb_data['rating'] = None

    try:
        movieb_data['m_score'] = float(movie_block.find('span',{'class':'metascore favorable'}).contents[0].strip()) #meta score
    except:
        movieb_data['m_score'] = None

    try:
        movieb_data['votes'] = int(movie_block.find('span',{'name':'nv'}).get('data-value')) # votes
    except:
        movieb_data['votes'] = None

    return movieb_data

def scrape_m_page(movie_blocks):
    page_movie_data = []
    num_blocks = len(movie_blocks)

    for block in range(num_blocks):
        page_movie_data.append(scrape_mblock(movie_blocks[block]))

    return page_movie_data

def scrape_this(link, t_count):
    #from IPython.core.debugger import set_trace

    base_url = link
    target = t_count

    current_mcount_start = 0
    current_mcount_end = 0
    remaining_mcount = target - current_mcount_end

    new_page_number = 1

    movie_data = []


    while remaining_mcount > 0:

        url = base_url + str(new_page_number)

        #set_trace()

        source = requests.get(url).text
        soup = bs4.BeautifulSoup(source,'html.parser')

        movie_blocks = soup.findAll('div',{'class':'lister-item-content'})

        movie_data.extend(scrape_m_page(movie_blocks))

        current_mcount_start = int(soup.find("div", {"class":"nav"}).find("div", {"class": "desc"}).contents[1].get_text().split("-")[0])

        current_mcount_end = int(soup.find("div", {"class":"nav"}).find("div", {"class": "desc"}).contents[1].get_text().split("-")[1].split(" ")[0])

        remaining_mcount = target - current_mcount_end

        print('\r' + "currently scraping movies from: " + str(current_mcount_start) + " - "+str(current_mcount_end), "| remaining count: " + str(remaining_mcount), flush=True, end ="")

        new_page_number = current_mcount_end + 1

        time.sleep(ran.randint(0, 10))

    return movie_data

############################################ scraping wrapper ###################################


def scrap_data(top_movies, base_scraping_link):

    films = []
    films = scrape_this(base_scraping_link,int(top_movies))
    df = pd.DataFrame(films)
    df['year'] = df['year'].str.slice(0, 4)
    valid_years = ['2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023']
    df = df[df['year'].isin(valid_years)]
    return df

############################################ scraping application ###################################

base_scraping_link = "https://www.imdb.com/search/title/?release_date=2016-01-01,2023-01-05&sort=boxoffice_gross_us,desc&start=0"
top_movies = 200
df = scrap_data(top_movies, base_scraping_link)

########################################################## web app ####################################


scatter_plot = px.scatter(df, x='votes', y='rating', color='name', title='Movie Ratings Scatter Plot')
bar_plot = px.bar(df, x='name', y='rating', title='Movie Ratings Bar Plot')
pie_chart = px.pie(df, values='rating', names='name', title='Movie Ratings Pie Chart')

app.layout = html.Div(
    children=[
        html.H1('Movie Ratings Visualization'),
        html.Div([
            html.Label('Select Plot Type:'),
            dcc.Dropdown(
                id='plot-type',
                options=[
                    {'label': 'Scatter Plot', 'value': 'scatter'},
                    {'label': 'Bar Plot', 'value': 'bar'},
                    {'label': 'Pie Chart', 'value': 'pie'}
                ],
                value='bar',
                clearable=False
            ),
            html.Label('Select Number of Movies:'),
            dcc.Dropdown(
                id='num-movies',
                options=[
                    {'label': 'Top 10 Movies', 'value': 10},
                    {'label': 'Top 20 Movies', 'value': 20},
                    {'label': 'Top 30 Movies', 'value': 30},
                    {'label': 'Top 40 Movies', 'value': 40},
                    {'label': 'Top 50 Movies', 'value': 50}
                ],
                value=10,
                clearable=False
            ),
            html.Label('Select Metric:'),
            dcc.Dropdown(
                id='metric',
                options=[
                    {'label': 'Metascore (m_score)', 'value': 'm_score'},
                    {'label': 'Votes', 'value': 'votes'},
                    {'label': 'Rating', 'value': 'rating'}
                ],
                value='rating',
                clearable=False
            ),
            html.Label('Display Pandas DataFrame:'),
            dcc.Dropdown(
                id='show-dataframe',
                options=[
                    {'label': 'Yes', 'value': 'yes'},
                    {'label': 'No', 'value': 'no'}
                ],
                value='yes',
                clearable=False
            ),
            dcc.Graph(id='plot'),
            html.Div(id='dataframe-container')
        ])
    ]
)

@app.callback(
    [dash.dependencies.Output('plot', 'figure'),
     dash.dependencies.Output('dataframe-container', 'children')],
    [dash.dependencies.Input('plot-type', 'value'),
     dash.dependencies.Input('num-movies', 'value'),
     dash.dependencies.Input('metric', 'value'),
     dash.dependencies.Input('show-dataframe', 'value')]
)
def update_plot(plot_type, num_movies, metric, show_dataframe):
    filtered_df = df.head(num_movies)
    if plot_type == 'scatter':
        plot = px.scatter(filtered_df, x=metric, y='name', color='name', title=f'Movie Ratings Scatter Plot (Top {num_movies} Movies)')
    elif plot_type == 'bar':
        plot = px.bar(filtered_df, x='name', y=metric, color='name', title=f'Movie Ratings Bar Plot (Top {num_movies} Movies)')
    else:
        plot = px.pie(filtered_df, values=metric, names='name', color='name', title=f'Movie Ratings Pie Chart (Top {num_movies} Movies)')
    if show_dataframe == 'yes':
        dataframe = html.Table(
            # Create table header
            [html.Tr([html.Th(col) for col in filtered_df.columns])] +

            # Create table rows
            [html.Tr([html.Td(filtered_df.iloc[i][col]) for col in filtered_df.columns]) for i in range(len(filtered_df))]
                              )
    else:
        dataframe = ''

    return plot, dataframe


if __name__ == '__main__':
    app.run_server(debug=True)
