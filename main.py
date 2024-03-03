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
    # mapbox_access_token = ...
    # px.set_mapbox_access_token(mapbox_access_token)
    city_sales = data.groupby('City').agg({'Total': 'sum', 'Latitude': 'mean', 'Longitude': 'mean'}).reset_index()
    fig = px.scatter_geo(city_sales, lat="Latitude", lon="Longitude", size="Total", color="Total", text="City",
                        center={"lat": 18.7, "lon": 98.9}, title='Total Sales by City', size_max=50)
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




city = ["Yangon", "Naypyitaw","Mandalay"]

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

    tgb.selector(value="{city}", lov=["Bangkok", "Chiang Mai", "Vientiane", "Luang Prabang", "Yangon", "Naypyitaw"],
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

'''# Calculate the figures using Python
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

layout_a ={
    # Chart title
    "title": "Sales performance by Product-line",
}
layout_b ={
    # Chart title
    "title": "Sales performance by City",
}
layout_c ={
    # Chart title
    "title": "Sales performance by Customer-type",
}
layout_d ={
    # Chart title
    "title": "Sales Trends over Time",
}
layout_e ={
    # Chart title
    "title": "Evolution of Sales by Product-line over Time",
    "barmode": "stack",
}
layout_f ={
    # Chart title
    "title": "Evolution of Sales by City over Time",
    "barmode": "stack",
}
layout_g ={
    # Chart title
    "title": "Evolution of Sales by Cutomer-type over Time",
    "barmode": "stack",
}
layout_h = {
    "title": "Evolution of Sales by Gender over Time",
    "xaxis": {
        "title": "Month-Year"
    },
    "yaxis": {
        "title": "% of Total"
    },
    "legend": {
        "title": "Category"
    },
    "barmode": "stack",
}
options = [
    # First pie chart
    {
        # Show label value on hover
        "hoverinfo": "label",
        # Leave a hole in the middle of the chart
        "hole": 0.4
    },
]'''

'''# Define the markdown text for the page
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
<|{data}|chart|type=pie|options={options}|labels=Product_line|layout={layout_a}|>

<|{data}|chart|type=pie|options={options}|labels=City|layout={layout_b}|>

<|{data}|chart|type=pie|options={options}|labels=Customer_type|layout={layout_c}|>

|>

<|{data}|chart|type=bar|x=Time|y=Total|labels=Date|layout={layout_d}|color=orange|>
<|{data}|chart|type=bar|x=Date|y=Total|labels=Date|layout={layout_d}|color=green|>

### Analysis
<|layout|columns=1 1|gap=30px|align-columns-center|
<|{percentage_data}|chart|type=bar|x=Month_Year|y[1]='Health and beauty'|y[2]='Electronic accessories'|y[3]='Sports and travel'|y[4]='Home and lifestyle'|y[5]='Food and beverages'|labels=Product_line|layout={layout_e}|>

<|{percentage_data}|chart|type=bar|x=Month_Year|y=City_pct|y[1]=Yangon|y[2]=Napypyitaw|y[3]=Mandalay|labels=City|labels=City|layout={layout_f}|>

<|{percentage_data}|chart|type=bar|x=Month_Year|y=Customer_type_pct|y[1]=Member|y[2]=Normal|labels=Customer_type|layout={layout_g}|>

<|{data}|chart|type=bar|x=Month_Year|y[1]=Female_pct|y[2]=Male_pct|labels=Gender|labels=Gender|layout={layout_h}|>
|>m

### Sales Data

<|{data}|table|columns=Invoice_ID;Branch;City;Customer_type;Gender;Product_line;Unit_price;Quantity;Tax_5%;Total;Date;Time;Payment;cogs;gross_margin_percentage;gross_income;Rating;Latitude;Longitude;Month_Year|group_by[Product_line]|apply[Total]=count|>
"""
# Create a markdown object
page = Gui(page)'''

if __name__ == "__main__":
    gui = Gui(page)
    gui.run(title="Sales Dashboard", port=3000)