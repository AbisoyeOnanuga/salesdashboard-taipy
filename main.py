# import the necessary modules and libraries
import pandas as pd
import taipy as tp
import plotly.express as px
import taipy.gui.builder as tgb
import taipy.gui as tg
from taipy.gui import Gui, Markdown
import numpy

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

def create_perc_fig(df, group_column):
    # Group, sum, and convert to percentage
    df = df.groupby(['Month_Year', group_column])['Total'].sum().unstack(fill_value=0)
    df = df.div(df.sum(axis=1), axis=0).reset_index().melt(id_vars='Month_Year', var_name=group_column, value_name='Percentage')
    df['Percentage'] = (df.loc[:, 'Percentage'].round(3) * 100)
    
    # Create and return the plot
    fig = px.bar(df, x='Month_Year', y='Percentage', color=group_column, title=f"Evolution of Sales by {group_column} over Time", labels={'Percentage': '% of Total'}, text_auto=True)
    return fig


fig_map = create_sales_by_city_map(data)

fig_product_line = create_pie_figure(data, 'Product_line')
fig_city = create_pie_figure(data, 'City')
fig_customer_type = create_pie_figure(data, 'Customer_type')

fig_time = create_bar_figure(data, 'Time')
fig_date = create_bar_figure(data, 'Date')


city = ["Yangon", "Naypyitaw", "Mandalay"]

filtered_data = data.loc[
    data["City"].isin(city)
]

fig_product_line_perc = create_perc_fig(filtered_data, 'Product_line')
fig_city_perc = create_perc_fig(filtered_data, 'City')
fig_gender_perc = create_perc_fig(filtered_data, 'Gender')
fig_customer_type_perc = create_perc_fig(filtered_data, 'Customer_type')

def on_selector(state):
    filtered_data = state.data.loc[
        state.data["City"].isin(state.city)
    ]

    state.fig_product_line_perc = create_perc_fig(filtered_data, 'Product_line')
    state.fig_city_perc = create_perc_fig(filtered_data, 'City')
    state.fig_gender_perc = create_perc_fig(filtered_data, 'Gender')
    state.fig_customer_type_perc = create_perc_fig(filtered_data, 'Customer_type')




with tgb.Page() as page:
    tgb.toggle(theme= True)
    tgb.text("Sales Insights", class_name="h1")

    with tgb.layout("1 1 1"):
        with tgb.part():
            tgb.text("Total Sales", class_name="h2")
            tgb.text("{int(data['Total'].sum())}", class_name="h3")

        with tgb.part():
            tgb.text("Average Sales", class_name="h2")
            tgb.text("{int(data['Total'].mean())}", class_name="h3")

        with tgb.part():
            tgb.text("Mean Rating", class_name="h2")
            tgb.text("{int(data['Rating'].mean())}", class_name="h3")

    tgb.chart(figure="{fig_map}")

    with tgb.layout("1 1 1"):
        tgb.chart(figure="{fig_product_line}")
        tgb.chart(figure="{fig_city}")
        tgb.chart(figure="{fig_customer_type}")
    
    tgb.chart(figure="{fig_time}")
    tgb.chart(figure="{fig_date}")

    tgb.text("Analysis", class_name="h2")

    tgb.selector(value="{city}", lov=["Yangon", "Naypyitaw", "Mandalay"],
                 dropdown=True,
                 multiple=True,
                 label="Select cities",
                 class_name="fullwidth",
                 on_change=on_selector)

    with tgb.layout("1 1"):
        tgb.chart(figure="{fig_product_line_perc}")
        tgb.chart(figure="{fig_city_perc}")
        tgb.chart(figure="{fig_gender_perc}")
        tgb.chart(figure="{fig_customer_type_perc}")

    tgb.table("{data}")


if __name__ == "__main__":
    gui = Gui(page)
    gui.run(title="Sales Dashboard", port=3000)