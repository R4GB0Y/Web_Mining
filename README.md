# IMDb Movie Ratings Web App

This project involves scraping movie data from IMDb using Beautiful Soup (bs4) and creating a web application using Plotly and Dash. The web app allows users to explore and visualize the ratings of top box office movies released in 2023.

## Data Scraping

The project starts by scraping movie data from IMDb using Beautiful Soup. The script `scraping_script.py` fetches the top box office movies released in 2023 by following a specific link. It extracts information such as movie name, release year, rating, metascore, and votes. The scraped data is organized and stored in a Pandas DataFrame for further analysis and visualization.

## Web Application

The web application, implemented with Plotly and Dash, provides an interactive platform to explore the movie ratings. The script `web_app.py` sets up the Dash server and defines the layout and functionality of the web app.

### Dropdown Controls

The web app includes three dropdown menus that allow users to customize their viewing experience:

- **Number of Movies to Rank**: Users can select the desired number of movies to rank, choosing from options such as 10, 20, 30, 40, or 50. This determines the number of movies displayed in the plot.

- **Type of Plot**: Users can choose the type of plot to visualize the movie ratings. Options include scatter plot, bar plot, and pie chart.

- **Metric of Plot**: Users can select the metric to plot on the y-axis. The available metrics are votes, m_rating (metascore rating), and rating (IMDb rating).

### Plotly and Dash Integration

Plotly is utilized to create the interactive visualizations, while Dash provides the framework for building the web application. The selected options from the dropdown menus dynamically update the plot, allowing users to explore the ratings based on their preferences.
