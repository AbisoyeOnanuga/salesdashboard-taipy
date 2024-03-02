# import the necessary modules and libraries
import taipy.gui as tg
from taipy.gui import Gui, Markdown
import pandas as pd
import taipy as tp
import plotly.express as px
import taipy.gui.builder as tgb
import numpy

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
    # mapbox_access_token = ...
    # px.set_mapbox_access_token(mapbox_access_token)
    city_sales = data.groupby('City').agg({'Total': 'sum', 'Latitude': 'mean', 'Longitude': 'mean'}).reset_index()
    fig = px.scatter_mapbox(city_sales, lat="Latitude", lon="Longitude", size="Total", color="Total", text="City",
                            zoom=5, center={"lat": 18.7, "lon": 98.9}, mapbox_style="dark", title='Total Sales by City', size_max=50)
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

fig_time = create_bar_figure(data, 'Time')
fig_date = create_bar_figure(data, 'Date')

# Calculate the figures using Python
total_sales = int(data['Total'].sum())
average_sales = int(data['Total'].mean())
mean_rating = int(data['Rating'].mean())

# Define the data, marker, and layout dictionaries
data["size"] = numpy.interp(data["Total"], [data["Total"].min(), data["Total"].max()], [8, 60])

# Add a column holding the bubble hover texts
data["text"] = data.apply(lambda row: f"Location: {row['City']}<br> Branch: [{row['Branch']}]<br> Quantity: {row['Quantity']}<br> Date: {row['Month_Year']}", axis=1)

hoverlabel = {
    # Use a transparent grey color for the background
    "bgcolor": "rgba(0, 128, 128, 0.5)",
    # Use a black color for the border
    "bordercolor": "black",
    # Use a black color and a 12px size for the font
    "font": {"color": "black", "size": 12},
    # Use a left alignment for the text
    "align": "left"
}

marker = {
    # Use the "size" column to set the bubble size
    "size": "size",
    # Use the "Branch" column to set the marker color
    "color": "Branch",
    # Use a discrete color map to assign different colors to different Branch
    "color_discrete_map": {"A": "red", "B": "orange", "C": "green"},
    "text": "text",
    # Use the "hoverlabel" parameter to customize the hover text box
    "hoverlabel": "text"
}

layout = {
    "geo": {
        "showland": False,
        "showocean": False,
        "scope": "canada",
        "subunitcolor": "lightgrey",
        "subunitwidth": 2,
        "coastlinewidth": 1,
        "center": {"lat": 18.7, "lon": 98.9},
        "fitbounds": "locations",
        "projection_scale": 1,
        "showcountries": True,
        "countrycolor": "white",
        "countrywidth": 2,
        "showsubunits": True,
        "showcoastlines": True,
        "showlakes": True,
        "showrivers": True,
        "resolution": 100,
        "projection": "van der grinten"
    }
}

options = [
    # First pie chart
    {
        # Show label value on hover
        "hoverinfo": "label",
        # Leave a hole in the middle of the chart
        "hole": 0.4
    },
]

'''with tgb.Page() as page:
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
    
    tgb.chart(figure="{layout}")

    tgb.table("{data}")'''

# Define the markdown text for the page
content = """
<h1 style="vertical-align: middle; font-size: 50px; margin-left: 50px; padding-left: 5px"><img style="vertical-align: middle;" src="./image/salesdashboard-logo.png" width="100" height="100" />Sales Insights</h1>
<|toggle|theme|>

### Summary Statistics
<|layout|columns=1 1 1|gap=30px|align-columns-center|

**Total **{: .color-primary}Sales
<|{total_sales}|text|class_name=h2|>

**Average **{: .color-primary}Sales
<|{average_sales}|text|class_name=h2|>

**Mean **{: .color-primary}Rating
<|{mean_rating}|text|class_name=h2|>

|>

### Total Sales by City
<|{data}|chart|type=scattergeo|mode=markers|lat=Latitude|lon=Longitude|marker={marker}|text=text|layout={layout}|>

<|layout|columns=1 1 1|gap=30px|align-columns-center|

<|{data}|chart|type=pie|options={options}|labels=Product_line|>

<|{data}|chart|type=pie|options={options}|labels=City|>

<|{data}|chart|type=pie|options={options}|labels=Customer_type|>

|>

### Sales Data

<|{data}|table|columns=Invoice_ID;Branch;City;Customer_type;Gender;Product_line;Unit_price;Quantity;Tax_5%;Total;Date;Time;Payment;cogs;gross_margin_percentage;gross_income;Rating;Latitude;Longitude;Month_Year|group_by[Product_line]|apply[Total]=count|>
"""
# Create a markdown object
page_md = Markdown(content)

gui = tg.Gui(page_md)
gui.run(title="Sales Dashboard", port=3000)