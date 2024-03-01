# import the necessary modules and libraries
from taipy.gui import Gui, Markdown
import pandas as pd
import taipy as tp
import plotly.express as px
import taipy.gui.builder as tgb

data = pd.read_csv('data/supermarket_sales.csv')

def create_pie_fig(data, group_by: str):
    grouped_data = data.groupby(group_by)['Total'].sum().reset_index()
    grouped_data['Total'] = grouped_data['Total'].round(2)
    fig = px.pie(grouped_data, names=group_by, values='Total', title=f"Sales Performance by {group_by}", hole=0.3)
    return fig

def create_bar_figure(data, group_by: str):
    sales_over_time = data.groupby(group_by)['Total'].sum().reset_index()
    fig = px.bar(sales_over_time, x=group_by, y='Total', title='Sales Trends Over Time', color='Total')
    return fig

def create_sales_by_city_map(data):
    # No need to set mapbox access token
    city_sales = data.groupby('City').agg({'Total': 'sum', 'Latitude': 'mean', 'Longitude': 'mean'}).reset_index()
    fig = px.scatter_mapbox(city_sales, lat="Latitude", lon="Longitude", size="Total", color="Total", text="City",
                            zoom=5, center={"lat": 18.7, "lon": 98.9}, mapbox_style="open-street-map", title='Total Sales by City', size_max=50)
    fig.update_layout(title={'text': "Total Sales by City", 'y': 0.9, 'x': 0.5, 'xanchor': 'center', 'yanchor': 'top'},
                      legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01),
                      margin={"r": 0, "t": 0, "l": 0, "b": 0})
    return fig

def create_perc_fig(df, group_column):
    # Group, sum, and convert to percentage
    df = df.groupby(['Month)Year', group_column])['Total'].sum().unstack(fill_value=0)
    df = df.div(df.sum(axis=1), axis=0).reset_index().melt(id_vars='Month_Year', var_name=group_column, value_name='Percentage')
    df['Percentage'] = (df.loc[:, 'Percentage'].round(3) * 100)

    # Create and return the plot
    fig = px.bar(df, x='Month_Year', y='Percentage', color=group_column, title=f"Evolution of Sales by {group_column} over Time", labels={'Percentage': '% of Total'}, text_auto=True)
    return fig

fig_map = create_sales_by_city_map(data)

with tgb.Page() as page:
    tgb.text("Sales Insights", class_name="h1")

    with tgb.layout("1 1 1"):
        with tgb.part():
            tgb.text("Toatal Sales", class_name="h1")
            tgb.text("{int(data['Total'].sum())}", class_name="h3")
   
        with tgb.part():
            tgb.text("Average Sales", class_name="h1")
            tgb.text("{int(data['Total'].mean())}", class_name="h3")
        
        with tgb.part():
            tgb.text("Mean Rating", class_name="h1")
            tgb.text("{int(data['Rating'].mean())}", class_name="h3")

    tgb.chart(figure="{fig_map}")

    tgb.table("{data}")

if __name__ == '__main__':
    gui = Gui(page)
    gui.run(title="Sales Dashboard", port=3000)