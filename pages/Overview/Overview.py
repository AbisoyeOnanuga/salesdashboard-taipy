import pandas as pd
import plotly.express as px
import taipy.gui.builder as tgb
import os

data = pd.read_csv('data/supermarket_sales.csv')

def create_pie_figure(data, group_by: str):
    grouped_data = data.groupby(group_by)['Total'].sum().reset_index()
    grouped_data['Total'] = grouped_data['Total'].round(2)
    fig = px.pie(grouped_data, names=group_by, values='Total', title=f"Sales Performance by {group_by}", hole=0.3)
    return fig

def create_bar_figure(data, group_by: str):
    sales_over_time = data.groupby(group_by)['Total'].sum().reset_index()
    fig = px.bar(sales_over_time, x=group_by, y='Total', title='Sales Trends Over Time', color='Total')
    return fig

def create_sales_by_city_map(data):
    # Convert "Month_Year" to datetime format (with day set to 1)
    #data['Month_Year'] = pd.to_datetime(data['Month_Year'], format='%m-%Y', errors='coerce')  # Coerce invalid dates to NaT
    # Sort data by the "Date" column
    #data.sort_values(by='Date', inplace=True)  # Sort in ascending order
    city_sales = data.groupby('City').agg({'Total': 'sum', 'Latitude': 'mean', 'Longitude': 'mean', 'Branch': 'first', 'Quantity': 'first', 'gross_income': 'first', 'Rating': 'first'}).reset_index()
    fig = px.scatter_geo(city_sales, lat='Latitude', lon='Longitude', size="Total", color='Total', # Color-coded by total sales amounts
                    hover_name='City', hover_data=['Branch', 'Quantity', 'Total', 'gross_income', 'Rating'], # Include additional columns
                    #animation_frame='Date', # Use the appropriate column for animation
                    projection='natural earth', title='Total Sales by City', 
                    color_continuous_scale='Oranges', center={"lat": 18.7, "lon": 98.9}, size_max=50, basemap_visible=True)
    fig.update_layout(title={'text': "Total Sales by City", 'y': 0.9, 'x': 0.5, 'xanchor': 'center', 'yanchor': 'top'},
                      legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01),
                      margin={"r": 0, "t": 0, "l": 0, "b": 0})
    return fig

fig_product_line = create_pie_figure(data, 'Product_line')
fig_city = create_pie_figure(data, 'City')
fig_customer_type = create_pie_figure(data, 'Customer_type')

fig_map = create_sales_by_city_map(data)
fig_time = create_bar_figure(data, 'Time')
fig_date = create_bar_figure(data, 'Date')

with tgb.Page() as Overview:
    # Sales by City map
    tgb.chart(figure="{fig_map}", height="600px")

    with tgb.layout(columns="1 1 1"):
        tgb.chart(figure="{fig_product_line}")
        tgb.chart(figure="{fig_city}")
        tgb.chart(figure="{fig_customer_type}")
    
    tgb.chart(figure="{fig_time}")
    tgb.chart(figure="{fig_date}")